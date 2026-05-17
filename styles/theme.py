import flet as ft


class C:
    """Color palette — dark navy/blue professional theme."""

    # Backgrounds
    BG_DARK = "#07091a"
    BG_PANEL = "#0c1226"
    BG_CARD = "#121c38"
    BG_INPUT = "#080d1f"

    # Borders
    BORDER = "#1d2b52"
    BORDER_FOCUS = "#3b6fd4"

    # Brand
    PRIMARY = "#3b6fd4"
    GRAD_A = "#060f3a"
    GRAD_B = "#0e1e6b"
    GRAD_C = "#152c9e"
    ACCENT = "#5f92f5"

    # Text
    TEXT = "#dde5ff"
    TEXT2 = "#6d82b8"
    TEXT3 = "#3d4f7c"

    # Status
    OK = "#41c98c"
    ERR = "#e85d5d"

    # Per-plan accent colors
    PLAN = {
        "Teste": "#546e7a",
        "Essencial": "#1565c0",
        "Profissional": "#6a1b9a",
        "Elite": "#bf360c",
    }


def all_border(width: float, color: str) -> ft.Border:
    """Create a uniform border on all sides."""
    side = ft.BorderSide(width, color)
    return ft.Border(top=side, right=side, bottom=side, left=side)


def pad(left: float = 0, top: float = 0, right: float = 0, bottom: float = 0) -> ft.Padding:
    return ft.Padding(left=left, top=top, right=right, bottom=bottom)


def pad_all(v: float) -> ft.Padding:
    return ft.Padding(left=v, top=v, right=v, bottom=v)


def pad_sym(h: float = 0, v: float = 0) -> ft.Padding:
    return ft.Padding(left=h, top=v, right=h, bottom=v)


def left_panel_gradient() -> ft.LinearGradient:
    return ft.LinearGradient(
        begin=ft.Alignment(-1, -1),
        end=ft.Alignment(1, 1),
        colors=[C.GRAD_A, C.GRAD_B, C.GRAD_C],
    )


def field_kwargs() -> dict:
    return dict(
        border_radius=10,
        bgcolor=C.BG_INPUT,
        border_color=C.BORDER,
        focused_border_color=C.PRIMARY,
        color=C.TEXT,
        cursor_color=C.PRIMARY,
        height=50,
    )


def dropdown_kwargs() -> dict:
    return dict(
        border_radius=10,
        bgcolor=C.BG_INPUT,
        border_color=C.BORDER,
        focused_border_color=C.PRIMARY,
        color=C.TEXT,
    )
