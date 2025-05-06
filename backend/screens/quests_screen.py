
import flet as ft
from models.quest import Quest, QuestType

class QuestsScreen(ft.Container):
    def __init__(self, player):
        super().__init__()
        self.player = player
        self.expand = True
        self.content = self.build()
    
    def build(self):
        return ft.Column(
            controls=[
                ft.Text("Quest Log", size=28, weight="bold"),
                ft.Tabs(
                    tabs=[
                        ft.Tab(
                            text="Active",
                            content=self._build_quest_list(self.player.active_quests)
                        ),
                        ft.Tab(
                            text="Completed",
                            content=self._build_quest_list(self.player.completed_quests)
                        ),
                        ft.Tab(
                            text="Available",
                            content=self._build_available_quests()
                        )
                    ],
                    expand=True
                )
            ],
            spacing=20
        )
    
    def _build_quest_list(self, quests):
        return ft.ListView(
            controls=[self._build_quest_card(q) for q in quests],
            spacing=10,
            expand=True
        )
    
    def _build_available_quests(self):
        available_quests = Quest.daily_quests()  # Using the basic daily quests
        return ft.ListView(
            controls=[self._build_quest_card(q, is_available=True) for q in available_quests],
            spacing=10,
            expand=True
        )
    
    def _build_quest_card(self, quest, is_available=False):
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text(quest.name, size=18, weight="bold"),
                    ft.Text(quest.description),
                    ft.Text(f"XP Reward: {quest.xp_reward}", color=ft.colors.AMBER),
                    ft.Text(f"Gold Reward: {quest.gold_reward}", color=ft.colors.AMBER),
                    ft.ElevatedButton(
                        "Begin Quest" if is_available else "Complete Quest",
                        on_click=lambda e: self._handle_quest(quest, is_available),
                        icon=ft.icons.PLAY_ARROW if is_available else ft.icons.CHECK
                    )
                ]),
                padding=15
            )
        )
    
    def _handle_quest(self, quest, is_available):
        if is_available:
            self.player.active_quests.append(quest)
        else:
            self.player.complete_quest(quest)
        self.content = self.build()
        self.update()