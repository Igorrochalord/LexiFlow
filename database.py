from datetime import datetime, timedelta

import motor.motor_asyncio
from pymongo.errors import DuplicateKeyError

from config import PLANS

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "lexiflow"

_client: motor.motor_asyncio.AsyncIOMotorClient | None = None


def _get_col():
    global _client
    if _client is None:
        _client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
    return _client[DB_NAME]["usuarios"]


async def init_db() -> None:
    col = _get_col()
    await col.create_index("nome", unique=True)


async def create_user(data: dict) -> tuple[bool, str]:
    col = _get_col()
    plan = PLANS[data["plano"]]
    now = datetime.now()
    expiry = now + timedelta(days=plan["duration_days"])

    doc = {
        "nome": data["nome"],
        "oab": data.get("oab"),
        "idade": data["idade"],
        "estado": data["estado"],
        "cidade": data["cidade"],
        "escritorio_nome": data.get("escritorio_nome"),
        "escritorio_estado": data.get("escritorio_estado"),
        "escritorio_cidade": data.get("escritorio_cidade"),
        "plano": data["plano"],
        "email": data.get("email"),
        "data_cadastro": now.isoformat(timespec="seconds"),
        "data_expiracao": expiry.isoformat(timespec="seconds"),
        "ativo": True,
    }

    try:
        await col.insert_one(doc)
        return True, "Conta criada com sucesso!"
    except DuplicateKeyError:
        return False, "Já existe uma conta com este nome."
    except Exception as exc:
        return False, f"Erro ao criar conta: {exc}"


async def login_user(nome: str) -> tuple[bool, str, dict | None]:
    col = _get_col()
    user = await col.find_one({"nome": nome.strip()})
    if not user:
        return False, "Usuário não encontrado.", None
    if not user.get("ativo", True):
        return False, "Conta inativa. Contate o suporte.", None
    if datetime.now() > datetime.fromisoformat(user["data_expiracao"]):
        return False, "Assinatura expirada. Renove para continuar.", None
    user["_id"] = str(user["_id"])
    return True, "Login realizado!", user
