import flet as ft
from datetime import datetime

class HabitTracker(ft.Control):
    def __init__(self, habits):
        super().__init__()
        self.habits = habits
    
    def build(self):
        return ft.Column(
            controls=[
                ft.Text("Daily Habits", size=20, weight=ft.FontWeight.BOLD),
                *[self._build_habit_card(habit) for habit in self.habits]
            ]
        )
    
    def _build_habit_card(self, habit):
        return ft.Card(
            content=ft.ListTile(
                title=ft.Text(habit['name']),
                subtitle=ft.Text(f"Streak: {habit['streak']} days"),
                trailing=ft.Checkbox(
                    on_change=lambda e: self._complete_habit(habit)
                )
            )
        )
    
    def _complete_habit(self, habit):
        habit['last_completed'] = datetime.now()
        habit['streak'] += 1
        self.update()