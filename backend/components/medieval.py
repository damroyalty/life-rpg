import flet as ft

class MedievalButton(ft.ElevatedButton):
    def __init__(self, text, on_click=None, icon=None):
        super().__init__(
            text=text,
            on_click=on_click,
            icon=icon,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=5),
                side=ft.BorderSide(2, ft.colors.AMBER_700),
                bgcolor=ft.colors.BLUE_GREY_800,
                overlay_color=ft.colors.AMBER.with_opacity(0.1),
                elevation=4,
                padding=ft.padding.symmetric(horizontal=20, vertical=10)
            ),
            color=ft.colors.AMBER_200
        )

class MedievalCard(ft.Card):
    def __init__(self, content=None):
        super().__init__(
            elevation=8,
            content=ft.Container(
                content=content,
                padding=15,
                border=ft.border.all(1, ft.colors.AMBER_800),
                bgcolor=ft.colors.BLUE_GREY_900,
                border_radius=10
            ),
            elevation=8,
            shadow_color=ft.colors.AMBER_800,
            surface_tint_color=ft.colors.BLUE_GREY_900
        )

class MedievalProgressBar(ft.ProgressBar):
    def __init__(self, value=0, **kwargs):
        super().__init__(
            value=value,
            color=ft.colors.AMBER,
            bgcolor=ft.colors.BLUE_GREY_800,
            height=20,
            bar_height=20,
            border_radius=10,
            **kwargs
        )