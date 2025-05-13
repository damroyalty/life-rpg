import flet as ft
from models.player import Player

class RewardsScreen(ft.Container):
    def __init__(self, player: Player):
        super().__init__()
        self.player = player
        self.expand = True
        self.content = self.build()
    
    def build(self):
        rewards = [
            {"name": "Health Potion", "cost": 50, "effect": "Restores 10 HP"},
            {"name": "Mana Elixir", "cost": 75, "effect": "Restores 15 MP"},
            {"name": "Golden Key", "cost": 200, "effect": "Unlocks special quests"}
        ]
        
        return ft.Column(
            controls=[
                ft.Text("Rewards Shop", size=24, weight="bold"),
                ft.Text(f"Your Gold: {self.player.gold}", size=18),
                ft.GridView(
                    controls=[
                        ft.Card(
                            ft.Container(
    content=ft.Column(
        [
            ft.Text(reward["name"], weight="bold"),
            ft.Text(reward["effect"]),
            ft.Text(f"{reward['cost']} Gold", color="amber"),
            ft.Container(
                content=ft.ElevatedButton(
                    "Purchase",
                    on_click=lambda e, r=reward: self._purchase(r),
                    disabled=self.player.gold < reward["cost"]
                ),
                alignment=ft.alignment.center
            )
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER
    ),
    padding=15,
    width=180,
    height=180
)

                        ) for reward in rewards
                    ],
                    runs_count=2,
                    max_extent=200,
                    spacing=20,
                    run_spacing=20
                )
            ],
            spacing=20,
            scroll="auto"
        )
    
    def _purchase(self, reward):
        if self.player.gold >= reward["cost"]:
            self.player.gold -= reward["cost"]
            self.content = self.build()
            self.update()