APP_NAME = "LexiFlow"
APP_VERSION = "1.0.0"
DB_PATH = "lexiflow.db"

STATES = [
    "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO",
    "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI",
    "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO",
]

PLANS: dict[str, dict] = {
    "Teste": {
        "price": "Grátis",
        "duration_days": 7,
        "color": "#546e7a",
        "requires_email": False,
        "icon": "🧪",
        "description": "7 dias grátis",
    },
    "Essencial": {
        "price": "R$ 49,90/mês",
        "duration_days": 30,
        "color": "#1565c0",
        "requires_email": False,
        "icon": "⭐",
        "description": "Básico",
    },
    "Profissional": {
        "price": "R$ 99,90/mês",
        "duration_days": 30,
        "color": "#6a1b9a",
        "requires_email": True,
        "icon": "💼",
        "description": "OCR + Scraping",
    },
    "Elite": {
        "price": "R$ 199,90/mês",
        "duration_days": 30,
        "color": "#bf360c",
        "requires_email": True,
        "icon": "👑",
        "description": "Acesso total",
    },
}
