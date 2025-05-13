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
        self.claimed_today = self._check_claimed_today()
        self.padding = 20
        self.margin = 10
        self.bgcolor = "#1e293b"
        self.border_radius = 16
        self.border = ft.border.all(1, ft.Colors.with_opacity(0.1, "white"))
        self.shadow = ft.BoxShadow(
            spread_radius=1,
            blur_radius=20,
            color=ft.Colors.with_opacity(0.3, "black"),
            offset=ft.Offset(0, 4),
        )
        self.content = self.build()

    def _check_claimed_today(self):
        if not hasattr(self.player, 'last_login') or self.player.last_login is None:
            return False
        return self.player.last_login.date() == datetime.now().date()

    def _handle_redeem(self, e):
        if not self.claimed_today:
            self.player.gold += 50
            self.player.xp += 20
            self.player.last_login = datetime.now()
            self.player.daily_streak += 1
            self.player.save()
            self.claimed_today = True
            self.content = self.build()
            self.update()

    
    def build(self):
        habits_section = ft.Column([
            ft.Text("Today's Habits", size=18, weight="bold"),
            ft.ListView(
                controls=self.get_todays_habits(),
                height=150,
                spacing=10
            )
        ]) if hasattr(self.player, 'habits') and self.player.habits else ft.Container()
        
        return ft.Column(
            controls=[
                ft.Text("Adventurer's Dashboard", size=24, weight="bold"),
                DailyLoginBonus(
                    streak=self.player.daily_streak,
                    claimed_today=self.claimed_today,
                    on_redeem=self._handle_redeem
                ),
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
                                ft.Text(f"Habit Streaks: {self.get_longest_habit_streak()} days"),
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
                habits_section,
                ft.Text("Today's Quests", size=18, weight="bold"),
                ft.ListView(
                    controls=[
                        ft.ListTile(
                            title=ft.Text(q.name),
                            subtitle=ft.Text(q.description),
                            trailing=ft.Checkbox(
                                on_change=lambda e, q=q: self._complete_quest(q)
                            )
                        ) for q in (Quest.daily_quests() if hasattr(Quest, 'daily_quests') else [])
                    ] if hasattr(Quest, 'daily_quests') and Quest.daily_quests() else [
                        ft.Text("No quests available today", color="grey")
                    ],
                    height=150
                )
            ],
            spacing=20,
            scroll="auto"
        )
    
    def get_todays_habits(self):
        """Get habits to display on home screen"""
        if not hasattr(self.player, 'habits'):
            return []
            
        today = datetime.now().date()
        habit_tiles = []
        
        for habit in self.player.habits:
            last_completed = datetime.strptime(habit['last_completed'], "%Y-%m-%d").date() if habit['last_completed'] else None
            completed_today = last_completed == today if last_completed else False
            
            habit_tiles.append(
                ft.ListTile(
                    leading=ft.Icon(
                        HabitType.get_icon(HabitType[habit['type']]),
                        color=HabitType.get_color(HabitType[habit['type']])
                    ),
                    title=ft.Text(habit['name']),
                    subtitle=ft.Text(f"Streak: {habit['streak']} days"),
                    trailing=ft.Checkbox(
                        value=completed_today,
                        on_change=lambda e, h=habit: self._toggle_habit_completion(h)
                    )
                )
            )
            
        return habit_tiles if habit_tiles else [ft.Text("No habits to track today", color="grey")]
    
    def get_longest_habit_streak(self):
        """Get the longest current habit streak"""
        if not hasattr(self.player, 'habits') or not self.player.habits:
            return 0
        return max(habit['streak'] for habit in self.player.habits)
    
    def _toggle_habit_completion(self, habit):
        """Toggle habit completion status"""
        today = datetime.now().date()
        last_completed = datetime.strptime(habit['last_completed'], "%Y-%m-%d").date() if habit['last_completed'] else None
        
        if not last_completed or today > last_completed:
            habit['completed_today'] = not habit.get('completed_today', False)
            if habit['completed_today']:
                habit['streak'] += 1
                habit['last_completed'] = today.strftime("%Y-%m-%d")
                self.player.add_xp(habit['xp'])
            else:
                habit['streak'] = max(0, habit['streak'] - 1)
            
            self.player.save()
            self.content = self.build()
            self.update()