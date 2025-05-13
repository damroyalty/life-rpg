import flet as ft
from datetime import datetime, timedelta

class XPBar(ft.Container):
    def __init__(self, player):
        super().__init__()
        self.player = player
        self.padding = 20
        self.margin = 10
        self.bgcolor = ft.Colors.with_opacity(0.2, "#1e293b")
        self.border_radius = 16
        self.border = ft.border.all(1, ft.Colors.with_opacity(0.1, "white"))
        self.shadow = ft.BoxShadow(
            spread_radius=1,
            blur_radius=20,
            color=ft.Colors.with_opacity(0.3, "black"),
            offset=ft.Offset(0, 4),
        )
        self.content = self.build()

    def build(self):
        progress = self.player.xp / self.player.xp_to_next_level() if self.player.xp_to_next_level() > 0 else 0
        return ft.Column(
            controls=[
                ft.Text(f"Level {self.player.level}", size=16, weight="bold", color="white"),
                ft.Divider(height=10, color="transparent"),
                ft.Stack(
                    controls=[
                        ft.Container(
                            width=400,
                            height=24,
                            bgcolor=ft.Colors.with_opacity(0.3, "#334155"),
                            border_radius=12
                        ),
                        ft.Container(
                            width=400 * progress,
                            height=24,
                            gradient=ft.LinearGradient(
                                begin=ft.alignment.center_left,
                                end=ft.alignment.center_right,
                                colors=["#f59e0b", "#f97316"]  # amber gradient
                            ),
                            border_radius=12
                            # removed animate cause it's causing a error
                        ),
                        ft.Text(
                            f"{self.player.xp}/{self.player.xp_to_next_level()} XP",
                            color="white",
                            weight="bold",
                            text_align="center",
                            width=400
                        )
                    ],
                    height=24
                )
            ],
            spacing=8
        )
