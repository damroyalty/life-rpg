import flet as ft
from models.player import Player
from components.habit_tracker import HabitTracker

class HabitsScreen(ft.Container):
    def __init__(self, player: Player):
        super().__init__()
        self.player = player
        self.expand = True
        self.padding = 20
        self.content = self.build()
    
    def build(self):
        # show empty habits if none exist
        if not hasattr(self.player, 'habits'):
            self.player.habits = []
        
        return ft.Column(
            controls=[
                ft.Text("Habit Tracker", size=24, weight="bold"),
                HabitTracker(self.player.habits),
                ft.ElevatedButton(
                    "Add New Habit",
                    icon=ft.icons.ADD,
                    on_click=self._add_new_habit,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=10),
                        padding=20
                    )
                )
            ],
            spacing=20,
            scroll="auto"
        )
    
    def _add_new_habit(self, e):
        # create dialog to add habit
        new_habit_name = ft.TextField(label="Habit Name")
        
        def close_dlg(e):
            if new_habit_name.value:
                self.player.habits.append({
                    "name": new_habit_name.value,
                    "streak": 0,
                    "completed": False,
                    "last_completed": None
                })
                self.content = self.build()
                self.update()
            dlg_modal.open = False
            self.page.update()
        
        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Add New Habit"),
            content=new_habit_name,
            actions=[
                ft.TextButton("Add", on_click=close_dlg),
                ft.TextButton("Cancel", on_click=lambda e: (setattr(dlg_modal, "open", False), self.page.update()))
            ],
            actions_alignment="end"
        )
        
        self.page.dialog = dlg_modal
        dlg_modal.open = True
        self.page.update()