import flet as ft
from datetime import datetime, timedelta
from components.xp_bar import XPBar
from components.attribute_chart import AttributeChart
from components.daily_login import DailyLoginBonus
from models.quest import Quest

class HomeScreen(ft.Container):
    def __init__(self, player):
        super().__init__()
        self.player = player
        self.expand = True
        self.content = self.build()
        self.padding = 10
        self._check_daily_login()
    
    def _check_daily_login(self):
        today = datetime.now().date()
        last_login = self.player.last_login.date()
        
        if today > last_login:
            if today - last_login == timedelta(days=1):
                self.player.daily_streak += 1
            else:
                self.player.daily_streak = 1
            
            self.player.last_login = datetime.now()
            self.player.save()
    
    def build(self):
        # daily quests
        daily_quests = Quest.daily_quests() if hasattr(Quest, 'daily_quests') else []
        
        return ft.Column(
            controls=[
                ft.Text("Adventurer's Dashboard", size=24, weight="bold"),
                DailyLoginBonus(self.player.daily_streak),
                XPBar(self.player),
                ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Stats", size=18, weight="bold"),
                                ft.Text(f"Level: {self.player.level}"),
                                ft.Text(f"Gold: {self.player.gold}"),
                                ft.Text(f"XP: {self.player.xp}/{self.player.xp_to_next_level()}"),
                                ft.Text(f"Daily Streak: {self.player.daily_streak} days"),
                            ]),
                            padding=10,
                            bgcolor="#1e293b",
                            border_radius=10,
                            width=200
                        ),
                        AttributeChart(self.player.attributes)
                    ],
                    spacing=20,
                    alignment="spaceEvenly"
                ),
                ft.Text("Today's Quests", size=18, weight="bold"),
                ft.ListView(
                    controls=[
                        ft.ListTile(
                            title=ft.Text(q.name),
                            subtitle=ft.Text(q.description),
                            trailing=ft.Checkbox(
                                on_change=lambda e, q=q: self._complete_quest(q)
                            )
                        ) for q in daily_quests
                    ] if daily_quests else [
                        ft.Text("No quests available today", color="grey")
                    ],
                    height=150
                )
            ],
            spacing=20,
            scroll="auto"
        )
    
    def _complete_quest(self, quest):
        if hasattr(self.player, 'complete_quest'):
            self.player.complete_quest(quest)
            self.player.save()
            self.content = self.build()
            self.update()