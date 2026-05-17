import flet as ft

from database import login_user
from styles.theme import C, left_panel_gradient
from utils.validators import validate_name


def build_login_view(page: ft.Page) -> ft.View:

    name_field = ft.TextField(
        hint_text="Ex: Dr. João Silva",
        border_radius=10,
        bgcolor=C.BG_INPUT,
        border_color=C.BORDER,
        focused_border_color=C.PRIMARY,
        color=C.TEXT,
        cursor_color=C.PRIMARY,
        prefix_icon=ft.Icons.PERSON_OUTLINE,
        height=52,
    )

    error_text = ft.Text("", color=C.ERR, size=12, visible=False)

    _btn_label = ft.Text("ENTRAR", color=ft.Colors.WHITE, weight=ft.FontWeight.W_600, size=14)
    login_btn = ft.Button(
        content=_btn_label,
        width=float("inf"),
        height=50,
        style=ft.ButtonStyle(
            bgcolor=C.PRIMARY,
            shape=ft.RoundedRectangleBorder(radius=10),
            elevation=4,
        ),
    )

    def show_error(msg: str) -> None:
        error_text.value = msg
        error_text.visible = True
        page.update()

    async def handle_login(_) -> None:
        name = (name_field.value or "").strip()
        error_text.visible = False
        ok, msg = validate_name(name)
        if not ok:
            show_error(msg)
            return

        login_btn.disabled = True
        _btn_label.value = "Verificando..."
        page.update()

        success, message, user = await login_user(name)

        login_btn.disabled = False
        _btn_label.value = "ENTRAR"

        if not success:
            show_error(message)
            return

        page.session.set("current_user", user)
        await page.push_route("/dashboard")

    async def go_register(_) -> None:
        await page.push_route("/register")

    async def close_app(_) -> None:
        await page.window.close()

    def minimize_app(_) -> None:
        page.window.minimized = True
        page.update()

    login_btn.on_click = handle_login
    name_field.on_submit = handle_login

    # ── Left panel (drag handle) ───────────────────────────────────────────────
    left_content = ft.Container(
        width=290,
        expand=False,
        gradient=left_panel_gradient(),
        border_radius=ft.BorderRadius(top_left=12, top_right=0, bottom_left=12, bottom_right=0),
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
            controls=[
                ft.Text("⚖️", size=64, text_align=ft.TextAlign.CENTER),
                ft.Container(height=18),
                ft.Text("LexiFlow", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ft.Container(height=8),
                ft.Container(
                    width=60, height=2,
                    bgcolor=ft.Colors.with_opacity(0.3, ft.Colors.WHITE),
                ),
                ft.Container(height=12),
                ft.Text(
                    "Tecnologia a serviço\nda Advocacia",
                    size=13,
                    color=ft.Colors.with_opacity(0.55, ft.Colors.WHITE),
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=60),
                ft.Text("v1.0.0", size=11, color=ft.Colors.with_opacity(0.35, ft.Colors.WHITE)),
            ],
        ),
    )

    left_panel = ft.WindowDragArea(content=left_content)

    # ── Right panel ────────────────────────────────────────────────────────────
    right_panel = ft.Container(
        expand=True,
        bgcolor=C.BG_PANEL,
        border_radius=ft.BorderRadius(top_left=0, top_right=12, bottom_left=0, bottom_right=12),
        padding=ft.Padding(left=48, top=24, right=48, bottom=40),
        content=ft.Column(
            expand=True,
            spacing=0,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.END,
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.REMOVE,
                            icon_color=C.TEXT3,
                            icon_size=16,
                            tooltip="Minimizar",
                            on_click=minimize_app,
                        ),
                        ft.IconButton(
                            icon=ft.Icons.CLOSE,
                            icon_color=C.TEXT3,
                            icon_size=16,
                            tooltip="Fechar",
                            on_click=close_app,
                        ),
                    ],
                ),
                ft.Container(height=24),
                ft.Text("Bem-vindo de volta", size=26, weight=ft.FontWeight.BOLD, color=C.TEXT),
                ft.Container(height=6),
                ft.Text("Entre com seu nome cadastrado para acessar", size=13, color=C.TEXT2),
                ft.Container(height=36),
                ft.Text("NOME COMPLETO", size=11, color=C.TEXT2, weight=ft.FontWeight.W_600),
                ft.Container(height=8),
                name_field,
                ft.Container(height=4),
                error_text,
                ft.Container(height=24),
                login_btn,
                ft.Container(height=28),
                ft.Row(
                    controls=[
                        ft.Container(expand=True, height=1, bgcolor=C.BORDER),
                        ft.Text("  ou  ", color=C.TEXT3, size=12),
                        ft.Container(expand=True, height=1, bgcolor=C.BORDER),
                    ],
                ),
                ft.Container(height=20),
                ft.OutlinedButton(
                    "Criar nova conta",
                    width=float("inf"),
                    height=46,
                    on_click=go_register,
                    style=ft.ButtonStyle(
                        color=C.PRIMARY,
                        side=ft.BorderSide(1.5, C.PRIMARY),
                        shape=ft.RoundedRectangleBorder(radius=10),
                    ),
                ),
            ],
        ),
    )

    return ft.View(
        route="/login",
        padding=0,
        bgcolor=C.BG_DARK,
        controls=[
            ft.Container(
                expand=True,
                bgcolor=C.BG_DARK,
                content=ft.Row(
                    expand=True,
                    spacing=0,
                    controls=[left_panel, right_panel],
                ),
            )
        ],
    )
