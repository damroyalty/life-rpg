import flet as ft

class ProfileScreen(ft.Container):
    def __init__(self, player):
        super().__init__()
        self.player = player
        self.expand = True
        self.content = self.build()
    
    def build(self):
        return ft.Column(
            controls=[
                ft.Text("Character Profile", size=28, weight="bold"),
                ft.Row(
                    controls=[
                        ft.CircleAvatar(
                            radius=50,
                            bgcolor="blue",
                            content=ft.Text(self.player.name[0].upper())
                        ),
                        ft.Column(
                            controls=[
                                ft.TextField(
                                    label="Character Name",
                                    value=self.player.name,
                                    on_change=self.update_name
                                ),
                                ft.Text(f"Level {self.player.level} Adventurer"),
                                ft.Text(f"{self.player.gold} Gold")
                            ],
                            spacing=10
                        )
                    ],
                    spacing=20
                ),
                ft.Text("Attributes", size=20, weight="bold"),
                ft.Text("Strength: {}".format(self.player.attributes['strength'])),
                ft.Text("Intelligence: {}".format(self.player.attributes['intelligence'])),
                ft.Text("Charisma: {}".format(self.player.attributes['charisma'])),
                ft.ElevatedButton(
                    "Level Up",
                    on_click=self.level_up,
                    icon=ft.Icons.STAR
                )
            ],
            spacing=20,
            scroll="auto"
        )
    
    def update_name(self, e):
        self.player.name = e.control.value
    
    def level_up(self, e):
        self.player.level_up()
        self.content = self.build()
        self.update()