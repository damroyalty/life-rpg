import flet as ft
from datetime import datetime, timedelta

class DailyLoginBonus(ft.Container):
    def __init__(self, streak):
        super().__init__()
        self.streak = streak
        self.padding = 20
        self.margin = 10
        self.bgcolor = ft.colors.with_opacity(0.2, "#1e293b")
        self.border_radius = 16
        self.border = ft.border.all(1, ft.colors.with_opacity(0.1, "white"))
        self.shadow = ft.BoxShadow(
            spread_radius=1,
            blur_radius=20,
            color=ft.colors.with_opacity(0.3, "black"),
            offset=ft.Offset(0, 4),
        )
        self.content = self.build()
    
    def build(self):
        streak_color = ft.colors.AMBER if self.streak >= 3 else ft.colors.GREY_400
        return ft.Row(
            controls=[
                ft.Icon(ft.icons.CALENDAR_TODAY, color=streak_color, size=32),
                ft.Column([
                    ft.Text("Daily Login Bonus", size=16, weight="bold", color="white"),
                    ft.Text(f"{self.streak} day streak!", color=streak_color),
                    ft.Text("Claim your reward tomorrow!", color="white70", size=12)
                ], spacing=4)
            ],
            spacing=20
        )