import flet as ft

class LevelUpDialog(ft.AlertDialog):
    def __init__(self, player):
        super().__init__()
        self.player = player
        self.title = ft.Text("Level Up!", size=24, weight="bold")
        self.content = ft.Column(
            controls=[
                ft.Text(f"Congratulations! You've reached level {player.level}"),
                ft.Text("New abilities unlocked:", weight="bold"),
                ft.Text("- Increased attribute points"),
                ft.Text("- More gold rewards"),
                ft.Text("- Access to rare quests")
            ],
            spacing=10
        )
        self.actions=[
            ft.ElevatedButton(
                "Continue Adventure",
                on_click=self.close_dialog,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=10),
                    bgcolor=ft.colors.AMBER
                )
            )
        ]
        self.actions_alignment="center"
    
    def close_dialog(self, e):
        self.open = False
        self.page.update()