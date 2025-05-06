import flet as ft
from models.player import Player

class SettingsScreen(ft.Container):
    def __init__(self, player: Player, page: ft.Page):
        super().__init__()
        self.page = page
        self.player = player
        self.expand = True
        self.content = self.build()

    def build(self):
        self.dark_mode_switch = ft.Switch(
            value=self.page.theme_mode == ft.ThemeMode.DARK,
            on_change=self.toggle_theme_mode
        )

        return ft.Column(
            controls=[
                ft.Text("Settings", size=24, weight="bold"),
                ft.Container(
                    content=ft.ListTile(
                        title=ft.Text("Dark Mode"),
                        trailing=self.dark_mode_switch,
                    ),
                    bgcolor=ft.colors.SURFACE_VARIANT,
                    border_radius=8,
                    padding=5
                ),
                ft.Container(
                    content=ft.ListTile(
                        title=ft.Text("Notifications"),
                        trailing=ft.Switch(value=True),
                    ),
                    bgcolor=ft.colors.SURFACE_VARIANT,
                    border_radius=8,
                    padding=5
                ),
                ft.Container(
                    content=ft.ListTile(
                        title=ft.Text("Sound Effects"),
                        trailing=ft.Switch(value=True),
                    ),
                    bgcolor=ft.colors.SURFACE_VARIANT,
                    border_radius=8,
                    padding=5
                ),
                ft.Divider(),
                ft.ElevatedButton(
                    "Reset Progress",
                    icon=ft.icons.WARNING,
                    color="red",
                    on_click=self._confirm_reset,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                        padding=20
                    )
                )
            ],
            spacing=20,
            scroll="auto"
        )

    def _confirm_reset(self, e):
        # implement a confirmation dialog here
        pass

    def toggle_theme_mode(self, e):
        new_theme_mode = (
            ft.ThemeMode.DARK 
            if self.page.theme_mode == ft.ThemeMode.LIGHT 
            else ft.ThemeMode.LIGHT
        )
        self.page.theme_mode = new_theme_mode
        self.dark_mode_switch.value = new_theme_mode == ft.ThemeMode.DARK
        self.page.update()