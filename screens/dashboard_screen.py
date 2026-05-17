import flet as ft

from config import APP_NAME, APP_VERSION, PLANS
from styles.theme import C, all_border, left_panel_gradient


def build_dashboard_view(page: ft.Page) -> ft.View:

    user: dict = page.session.get("current_user") or {}
    plan_info = PLANS.get(user.get("plano", ""), {})
    first_name = user.get("nome", "Usuário").split()[0]
    expiry = user.get("data_expiracao", "")[:10]

    async def handle_logout(_) -> None:
        page.session.clear()
        await page.push_route("/login")

    async def close_app(_) -> None:
        await page.window.close()

    def minimize_app(_) -> None:
        page.window.minimized = True
        page.update()

    # ── Sidebar nav ────────────────────────────────────────────────────────────
    def _nav_item(icon: str, label: str, active: bool = False) -> ft.Container:
        return ft.Container(
            bgcolor=ft.Colors.with_opacity(0.12, ft.Colors.WHITE) if active else "transparent",
            border_radius=8,
            margin=ft.Margin(left=12, top=0, right=12, bottom=0),
            padding=ft.Padding(left=12, top=10, right=12, bottom=10),
            content=ft.Row(
                spacing=10,
                controls=[
                    ft.Text(icon, size=16),
                    ft.Text(
                        label,
                        size=13,
                        color=ft.Colors.WHITE if active else ft.Colors.with_opacity(0.6, ft.Colors.WHITE),
                        weight=ft.FontWeight.W_500 if active else ft.FontWeight.NORMAL,
                    ),
                ],
            ),
        )

    sidebar_content = ft.Container(
        width=220,
        gradient=left_panel_gradient(),
        border_radius=ft.BorderRadius(top_left=12, top_right=0, bottom_left=12, bottom_right=0),
        content=ft.Column(
            expand=True,
            spacing=0,
            controls=[
                ft.Container(height=28),
                ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=4,
                    controls=[
                        ft.Text("⚖️", size=38, text_align=ft.TextAlign.CENTER),
                        ft.Text(
                            APP_NAME,
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.WHITE,
                        ),
                    ],
                ),
                ft.Container(height=24),
                ft.Divider(color=ft.Colors.with_opacity(0.12, ft.Colors.WHITE)),
                ft.Container(height=14),
                _nav_item("🏠", "Início", active=True),
                _nav_item("📊", "Dashboard"),
                _nav_item("📄", "Contratos"),
                _nav_item("📁", "Documentos"),
                _nav_item("⚙️", "Configurações"),
                ft.Container(expand=True),
                ft.TextButton(
                    content=ft.Row(
                        spacing=8,
                        controls=[
                            ft.Icon(ft.Icons.LOGOUT, size=15, color=ft.Colors.with_opacity(0.5, ft.Colors.WHITE)),
                            ft.Text("Sair", color=ft.Colors.with_opacity(0.5, ft.Colors.WHITE), size=13),
                        ],
                    ),
                    on_click=handle_logout,
                ),
                ft.Container(height=20),
            ],
        ),
    )

    sidebar = ft.WindowDragArea(content=sidebar_content)

    # ── Feature cards ──────────────────────────────────────────────────────────
    def _feature_card(icon: str, title: str, phase: str) -> ft.Container:
        return ft.Container(
            expand=True,
            bgcolor=C.BG_CARD,
            border_radius=12,
            border=all_border(1, C.BORDER),
            padding=ft.Padding(left=20, top=20, right=20, bottom=20),
            content=ft.Column(
                spacing=0,
                controls=[
                    ft.Text(icon, size=32),
                    ft.Container(height=12),
                    ft.Text(title, size=14, weight=ft.FontWeight.BOLD, color=C.TEXT),
                    ft.Container(height=4),
                    ft.Text(phase, size=12, color=C.TEXT3),
                ],
            ),
        )

    # ── Main area ──────────────────────────────────────────────────────────────
    main_area = ft.Container(
        expand=True,
        bgcolor=C.BG_DARK,
        border_radius=ft.BorderRadius(top_left=0, top_right=12, bottom_left=0, bottom_right=12),
        content=ft.Column(
            expand=True,
            spacing=0,
            controls=[
                # Top bar
                ft.Container(
                    bgcolor=C.BG_PANEL,
                    border_radius=ft.BorderRadius(top_left=0, top_right=12, bottom_left=0, bottom_right=0),
                    padding=ft.Padding(left=28, top=14, right=16, bottom=14),
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(
                                f"Olá, {first_name}! 👋",
                                size=15,
                                color=C.TEXT,
                                weight=ft.FontWeight.W_500,
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
                ),
                ft.Divider(color=C.BORDER, height=1),
                # Scrollable content
                ft.Container(
                    expand=True,
                    padding=ft.Padding(left=28, top=24, right=28, bottom=24),
                    content=ft.Column(
                        scroll=ft.ScrollMode.AUTO,
                        spacing=0,
                        expand=True,
                        controls=[
                            # Welcome banner
                            ft.Container(
                                bgcolor=C.BG_CARD,
                                border_radius=12,
                                border=all_border(1, C.BORDER),
                                padding=ft.Padding(left=24, top=20, right=24, bottom=20),
                                content=ft.Row(
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    controls=[
                                        ft.Column(
                                            spacing=4,
                                            controls=[
                                                ft.Text(
                                                    f"Bem-vindo ao LexiFlow, {first_name}!",
                                                    size=18,
                                                    weight=ft.FontWeight.BOLD,
                                                    color=C.TEXT,
                                                ),
                                                ft.Text(
                                                    f"Plano: {user.get('plano', '')}  •  Expira em: {expiry}",
                                                    size=13,
                                                    color=C.TEXT2,
                                                ),
                                            ],
                                        ),
                                        ft.Container(
                                            bgcolor=plan_info.get("color", C.PRIMARY),
                                            border_radius=20,
                                            padding=ft.Padding(left=16, top=8, right=16, bottom=8),
                                            content=ft.Text(
                                                f"{plan_info.get('icon', '')} {user.get('plano', '')}",
                                                color=ft.Colors.WHITE,
                                                size=13,
                                                weight=ft.FontWeight.BOLD,
                                            ),
                                        ),
                                    ],
                                ),
                            ),
                            ft.Container(height=20),
                            # Feature cards
                            ft.Row(
                                spacing=16,
                                controls=[
                                    _feature_card("⏱️", "Calculadora de Prazos", "Em breve — Fase 2"),
                                    _feature_card("📝", "Gerador de Contratos", "Em breve — Fase 3"),
                                    _feature_card("🔍", "Busca Processual", "Em breve — Fase 6"),
                                ],
                            ),
                            ft.Container(height=20),
                            # Status
                            ft.Container(
                                bgcolor=C.BG_CARD,
                                border_radius=12,
                                border=all_border(1, C.BORDER),
                                padding=ft.Padding(left=24, top=20, right=24, bottom=20),
                                content=ft.Column(
                                    spacing=0,
                                    controls=[
                                        ft.Text(
                                            "🚧 Em Desenvolvimento — Fase 1 Concluída",
                                            size=14,
                                            weight=ft.FontWeight.BOLD,
                                            color=C.ACCENT,
                                        ),
                                        ft.Container(height=10),
                                        ft.Text(
                                            "O módulo de autenticação está funcionando. As demais funcionalidades serão liberadas nas próximas atualizações.",
                                            size=13,
                                            color=C.TEXT2,
                                        ),
                                        ft.Container(height=16),
                                        ft.ProgressBar(
                                            value=0.14,
                                            bgcolor=C.BG_INPUT,
                                            color=C.PRIMARY,
                                            border_radius=4,
                                        ),
                                        ft.Container(height=8),
                                        ft.Text(
                                            f"{APP_NAME} {APP_VERSION}  •  14% concluído",
                                            size=11,
                                            color=C.TEXT3,
                                        ),
                                    ],
                                ),
                            ),
                        ],
                    ),
                ),
            ],
        ),
    )

    main_content = ft.Container(
        expand=True,
        bgcolor=C.BG_DARK,
        content=ft.Row(
            expand=True,
            spacing=0,
            controls=[sidebar, main_area],
        ),
    )

    return ft.View(
        route="/dashboard",
        padding=0,
        bgcolor=C.BG_DARK,
        controls=[main_content],
    )
