import flet as ft

from config import STATES, PLANS
from database import create_user
from styles.theme import C, all_border, left_panel_gradient, field_kwargs, dropdown_kwargs
from utils.validators import validate_name, validate_age, validate_email


def _label(text: str) -> ft.Text:
    return ft.Text(text, size=11, color=C.TEXT2, weight=ft.FontWeight.W_600)


def _section(text: str) -> ft.Text:
    return ft.Text(text, size=13, color=C.ACCENT, weight=ft.FontWeight.BOLD)


def _gap(h: int = 12) -> ft.Container:
    return ft.Container(height=h)


def build_register_view(page: ft.Page) -> ft.View:

    # ── Form fields ────────────────────────────────────────────────────────────
    nome_field = ft.TextField(hint_text="Ex: Dr. João Silva", **field_kwargs())
    oab_field = ft.TextField(hint_text="Ex: SP123456 (opcional)", **field_kwargs())
    idade_field = ft.TextField(
        hint_text="Ex: 35",
        keyboard_type=ft.KeyboardType.NUMBER,
        **field_kwargs(),
    )
    estado_drop = ft.Dropdown(
        hint_text="UF",
        options=[ft.dropdown.Option(s) for s in STATES],
        **dropdown_kwargs(),
    )
    cidade_field = ft.TextField(hint_text="Sua cidade", **field_kwargs())

    esc_nome_field = ft.TextField(hint_text="Ex: Silva & Associados (opcional)", **field_kwargs())
    esc_estado_drop = ft.Dropdown(
        hint_text="UF (opcional)",
        options=[ft.dropdown.Option(s) for s in STATES],
        **dropdown_kwargs(),
    )
    esc_cidade_field = ft.TextField(hint_text="Cidade do escritório (opcional)", **field_kwargs())

    email_field = ft.TextField(
        hint_text="seu@escritorio.com.br",
        keyboard_type=ft.KeyboardType.EMAIL,
        **field_kwargs(),
    )

    # ── State ──────────────────────────────────────────────────────────────────
    state = {"plan": "Teste"}

    email_row = ft.Column(
        visible=False,
        spacing=0,
        controls=[
            _gap(20),
            _label("EMAIL CORPORATIVO *"),
            _gap(8),
            email_field,
        ],
    )

    error_text = ft.Text("", color=C.ERR, size=13, visible=False)

    _submit_label = ft.Text("CRIAR CONTA", color=ft.Colors.WHITE, weight=ft.FontWeight.W_600, size=14)
    submit_btn = ft.Button(
        content=_submit_label,
        width=float("inf"),
        height=52,
        style=ft.ButtonStyle(
            bgcolor=C.PRIMARY,
            shape=ft.RoundedRectangleBorder(radius=10),
            elevation=4,
        ),
    )

    # ── Plan cards ─────────────────────────────────────────────────────────────
    plan_cards: dict[str, ft.Container] = {}

    def _refresh_cards() -> None:
        for key, card in plan_cards.items():
            selected = state["plan"] == key
            plan_color = PLANS[key]["color"]
            card.border = all_border(2 if selected else 1, plan_color if selected else C.BORDER)
            card.bgcolor = f"{plan_color}28" if selected else C.BG_CARD

    def _make_plan_card(key: str) -> ft.GestureDetector:
        p = PLANS[key]

        card = ft.Container(
            expand=True,
            border_radius=10,
            border=all_border(1, C.BORDER),
            bgcolor=C.BG_CARD,
            padding=ft.Padding(left=10, top=14, right=10, bottom=14),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=4,
                controls=[
                    ft.Text(p["icon"], size=26, text_align=ft.TextAlign.CENTER),
                    ft.Text(
                        key,
                        size=13,
                        weight=ft.FontWeight.BOLD,
                        color=C.TEXT,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        p["price"],
                        size=10,
                        color=C.TEXT2,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        p["description"],
                        size=9,
                        color=C.TEXT3,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
            ),
        )
        plan_cards[key] = card

        def on_tap(e, k=key):
            state["plan"] = k
            _refresh_cards()
            email_row.visible = PLANS[k]["requires_email"]
            page.update()

        return ft.GestureDetector(
            content=card,
            on_tap=on_tap,
            mouse_cursor=ft.MouseCursor.CLICK,
            expand=True,
        )

    plans_row = ft.Row(
        spacing=8,
        controls=[_make_plan_card(k) for k in PLANS],
    )
    # pre-select "Teste"
    _refresh_cards()

    # ── Handlers ───────────────────────────────────────────────────────────────
    def show_error(msg: str) -> None:
        error_text.value = msg
        error_text.visible = True
        page.update()

    async def handle_submit(_) -> None:
        error_text.visible = False

        nome = (nome_field.value or "").strip()
        oab = (oab_field.value or "").strip()
        idade_str = (idade_field.value or "").strip()
        estado = estado_drop.value
        cidade = (cidade_field.value or "").strip()
        esc_nome = (esc_nome_field.value or "").strip()
        esc_estado = esc_estado_drop.value
        esc_cidade = (esc_cidade_field.value or "").strip()
        plano = state["plan"]
        email = (email_field.value or "").strip()

        ok, msg = validate_name(nome)
        if not ok:
            show_error(msg)
            return
        ok, msg = validate_age(idade_str)
        if not ok:
            show_error(msg)
            return
        if not estado:
            show_error("Selecione seu estado.")
            return
        if not cidade:
            show_error("Cidade é obrigatória.")
            return
        if PLANS[plano]["requires_email"]:
            ok, msg = validate_email(email)
            if not ok:
                show_error(msg)
                return

        submit_btn.disabled = True
        _submit_label.value = "Criando conta..."
        page.update()

        success, message = await create_user({
            "nome": nome,
            "oab": oab or None,
            "idade": int(idade_str),
            "estado": estado,
            "cidade": cidade,
            "escritorio_nome": esc_nome or None,
            "escritorio_estado": esc_estado or None,
            "escritorio_cidade": esc_cidade or None,
            "plano": plano,
            "email": email or None,
        })

        submit_btn.disabled = False
        _submit_label.value = "CRIAR CONTA"

        if not success:
            show_error(message)
            return

        # Success → navigate back to login with snackbar
        sb = ft.SnackBar(
            content=ft.Text("✅ Conta criada! Faça login.", color=ft.Colors.WHITE),
            bgcolor=C.OK,
            duration=3000,
        )
        sb.open = True
        page.overlay.append(sb)
        await page.push_route("/login")

    submit_btn.on_click = handle_submit

    async def go_back(_) -> None:
        await page.push_route("/login")

    async def close_app(_) -> None:
        await page.window.close()

    def minimize_app(_) -> None:
        page.window.minimized = True
        page.update()

    # ── Form content (scrollable) ───────────────────────────────────────────────
    form = ft.Column(
        scroll=ft.ScrollMode.AUTO,
        spacing=0,
        expand=True,
        controls=[
            _section("📋 DADOS PESSOAIS"),
            _gap(16),
            _label("NOME COMPLETO *"),
            _gap(8),
            nome_field,
            _gap(16),
            ft.Row(
                spacing=12,
                controls=[
                    ft.Column(
                        expand=True,
                        spacing=0,
                        controls=[_label("NÚMERO OAB"), _gap(8), oab_field],
                    ),
                    ft.Column(
                        expand=True,
                        spacing=0,
                        controls=[_label("IDADE *"), _gap(8), idade_field],
                    ),
                ],
            ),
            _gap(16),
            ft.Row(
                spacing=12,
                controls=[
                    ft.Column(
                        expand=1,
                        spacing=0,
                        controls=[_label("ESTADO *"), _gap(8), estado_drop],
                    ),
                    ft.Column(
                        expand=2,
                        spacing=0,
                        controls=[_label("CIDADE *"), _gap(8), cidade_field],
                    ),
                ],
            ),
            _gap(28),
            _section("🏢 DADOS DO ESCRITÓRIO"),
            _gap(16),
            _label("NOME DO ESCRITÓRIO"),
            _gap(8),
            esc_nome_field,
            _gap(16),
            ft.Row(
                spacing=12,
                controls=[
                    ft.Column(
                        expand=1,
                        spacing=0,
                        controls=[_label("ESTADO"), _gap(8), esc_estado_drop],
                    ),
                    ft.Column(
                        expand=2,
                        spacing=0,
                        controls=[_label("CIDADE"), _gap(8), esc_cidade_field],
                    ),
                ],
            ),
            _gap(28),
            _section("💎 ESCOLHA SEU PLANO"),
            _gap(16),
            plans_row,
            email_row,
            _gap(28),
            error_text,
            _gap(8),
            submit_btn,
            _gap(16),
            ft.Text(
                "Ao criar sua conta você concorda com os Termos de Uso e Política de Privacidade.",
                size=11,
                color=C.TEXT3,
                text_align=ft.TextAlign.CENTER,
            ),
            _gap(20),
        ],
    )

    # ── Left panel ─────────────────────────────────────────────────────────────
    left_content = ft.Container(
        width=240,
        gradient=left_panel_gradient(),
        border_radius=ft.BorderRadius(top_left=12, top_right=0, bottom_left=12, bottom_right=0),
        padding=ft.Padding(left=28, top=0, right=28, bottom=0),
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
            controls=[
                ft.Text("⚖️", size=52, text_align=ft.TextAlign.CENTER),
                _gap(14),
                ft.Text(
                    "LexiFlow",
                    size=26,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE,
                ),
                _gap(8),
                ft.Container(
                    width=50,
                    height=2,
                    bgcolor=ft.Colors.with_opacity(0.3, ft.Colors.WHITE),
                ),
                _gap(12),
                ft.Text(
                    "Crie sua conta\ne comece hoje",
                    size=12,
                    color=ft.Colors.with_opacity(0.55, ft.Colors.WHITE),
                    text_align=ft.TextAlign.CENTER,
                ),
                _gap(40),
                ft.Container(
                    bgcolor=ft.Colors.with_opacity(0.12, ft.Colors.WHITE),
                    border_radius=10,
                    padding=ft.Padding(left=16, top=14, right=16, bottom=14),
                    content=ft.Column(
                        spacing=8,
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                        controls=[
                            ft.Text("✅ 7 dias grátis", size=12, color=ft.Colors.with_opacity(0.75, ft.Colors.WHITE)),
                            ft.Text("✅ Sem cartão", size=12, color=ft.Colors.with_opacity(0.75, ft.Colors.WHITE)),
                            ft.Text("✅ Cancele quando quiser", size=12, color=ft.Colors.with_opacity(0.75, ft.Colors.WHITE)),
                        ],
                    ),
                ),
            ],
        ),
    )

    left_panel = ft.WindowDragArea(content=left_content)

    # ── Right panel ─────────────────────────────────────────────────────────────
    right_panel = ft.Container(
        expand=True,
        bgcolor=C.BG_PANEL,
        border_radius=ft.BorderRadius(top_left=0, top_right=12, bottom_left=0, bottom_right=12),
        padding=ft.Padding(left=40, top=20, right=40, bottom=24),
        content=ft.Column(
            expand=True,
            spacing=0,
            controls=[
                # Top bar
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.TextButton(
                            content=ft.Row(
                                spacing=4,
                                controls=[
                                    ft.Icon(ft.Icons.ARROW_BACK, size=15, color=C.TEXT2),
                                    ft.Text("Voltar", size=13, color=C.TEXT2),
                                ],
                            ),
                            on_click=go_back,
                        ),
                        ft.Row(
                            spacing=0,
                            controls=[
                                ft.IconButton(
                                    icon=ft.Icons.REMOVE,
                                    icon_color=C.TEXT3,
                                    icon_size=16,
                                    on_click=minimize_app,
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.CLOSE,
                                    icon_color=C.TEXT3,
                                    icon_size=16,
                                    on_click=close_app,
                                ),
                            ],
                        ),
                    ],
                ),
                _gap(10),
                ft.Text(
                    "Criar sua conta",
                    size=22,
                    weight=ft.FontWeight.BOLD,
                    color=C.TEXT,
                ),
                ft.Text(
                    "Preencha os dados abaixo para começar",
                    size=13,
                    color=C.TEXT2,
                ),
                _gap(16),
                ft.Divider(color=C.BORDER, height=1),
                _gap(16),
                ft.Container(expand=True, content=form),
            ],
        ),
    )

    main_content = ft.Container(
        expand=True,
        bgcolor=C.BG_DARK,
        content=ft.Row(
            expand=True,
            spacing=0,
            controls=[left_panel, right_panel],
        ),
    )

    return ft.View(
        route="/register",
        padding=0,
        bgcolor=C.BG_DARK,
        controls=[main_content],
    )
