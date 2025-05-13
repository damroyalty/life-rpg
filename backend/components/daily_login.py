import flet as ft
from datetime import datetime

def DailyLoginBonus(streak, claimed_today, on_redeem):
    streak_color = ft.Colors.AMBER if streak >= 3 else ft.Colors.GREY_400

    redeem_button = ft.ElevatedButton(
        text="🎁 Redeem",
        bgcolor=ft.Colors.LIME_600,
        color="white",
        on_click=on_redeem,
        animate_opacity=300,
        visible=not claimed_today,
        scale=1.05
    )

    return ft.Container(
        padding=20,
        margin=10,
        bgcolor="rgba(30, 41, 59, 0.2)",
        border_radius=16,
        border=ft.border.all(1, "rgba(255, 255, 255, 0.1)"),
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=20,
            color="rgba(0, 0, 0, 0.3)",
            offset=ft.Offset(0, 4),
        ),
        content=ft.Row(
            controls=[
                ft.Icon(ft.Icons.CALENDAR_TODAY, color=streak_color, size=32),
                ft.Column([
                    ft.Text("Daily Login Bonus", size=16, weight="bold", color="white"),
                    ft.Text(f"{streak} day streak!", color=streak_color),
                    redeem_button if not claimed_today else ft.Text("Already claimed today!", color="white70", size=12)
                ], spacing=4)
            ],
            spacing=20
        )
    )
