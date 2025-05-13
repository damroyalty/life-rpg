import flet as ft
from datetime import datetime, timedelta

class HabitTracker(ft.Container):
    def __init__(self, habits):
        super().__init__()
        self.habits = habits
    
    def build(self):
        return ft.Column(
            controls=[ 
                *[self._build_habit_card(habit) for habit in self.habits]
            ],
            spacing=10
        )

    def _get_control_name(self):
        return "habit_tracker"
    
    def _build_habit_card(self, habit):
        streak_color = ft.Colors.AMBER if habit.get("streak", 0) >= 3 else ft.Colors.GREY_500
        last_completed = habit.get("last_completed")
        
        return ft.Card(
            content=ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Checkbox(
                            value=habit.get("completed", False),
                            on_change=lambda e, h=habit: self._toggle_habit(h)
                        ),
                        ft.Column(
                            controls=[
                                ft.Text(habit["name"], weight="bold"),
                                ft.Row([
                                    ft.Text(f"Streak: {habit.get('streak', 0)} days", 
                                           color=streak_color),
                                    ft.Text(
                                        f"Last: {last_completed.strftime('%m/%d')}" if last_completed 
                                        else "Never completed",
                                        size=12
                                    )
                                ], spacing=10)
                            ],
                            expand=True
                        ),
                        ft.IconButton(
                            icon=ft.Icons.DELETE,
                            on_click=lambda e, h=habit: self._remove_habit(h),
                            tooltip="Delete habit"
                        )
                    ],
                    alignment="spaceBetween"
                ),
                padding=10
            )
        )
    
    def _toggle_habit(self, habit):
        today = datetime.now().date()
        last_completed = habit.get("last_completed")
        
        if last_completed and last_completed.date() == today:
            return
        
        if last_completed and last_completed.date() == today - timedelta(days=1):
            habit["streak"] = habit.get("streak", 0) + 1
        else:
            habit["streak"] = 1
        
        habit["last_completed"] = datetime.now()
        habit["completed"] = True
        self.update()
    
    def _remove_habit(self, habit):
        self.habits.remove(habit)
        self.update()
