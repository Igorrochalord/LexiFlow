import flet as ft

from config import APP_NAME, APP_VERSION
from database import init_db
from screens.login_screen import build_login_view
from screens.register_screen import build_register_view
from screens.dashboard_screen import build_dashboard_view


async def main(page: ft.Page) -> None:
    page.title = f"{APP_NAME} {APP_VERSION}"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#07091a"
    page.padding = 0

    page.window.width = 960
    page.window.height = 620
    page.window.min_width = 860
    page.window.min_height = 560
    page.window.frameless = True
    page.window.shadow = True

    await init_db()

    async def route_change(_: ft.RouteChangeEvent) -> None:
        page.views.clear()
        match page.route:
            case "/register":
                page.views.append(build_register_view(page))
            case "/dashboard":
                if not page.session.get("current_user"):
                    await page.push_route("/login")
                    return
                page.views.append(build_dashboard_view(page))
            case _:
                page.views.append(build_login_view(page))
        page.update()

    async def view_pop(_: ft.ViewPopEvent) -> None:
        page.views.pop()
        if page.views:
            await page.push_route(page.views[-1].route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    await page.push_route("/login")


ft.run(main)
