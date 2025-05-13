import flet as ft
from datetime import datetime, timedelta
from enum import Enum, auto

class HabitType(Enum):
    PHYSICAL = auto()
    MENTAL = auto()
    SOCIAL = auto()
    CREATIVE = auto()
    PRODUCTIVE = auto()
    OTHER = auto()

    @classmethod
    def get_icon(cls, habit_type):
        icons = {
            cls.PHYSICAL: ft.Icons.DIRECTIONS_RUN,
            cls.MENTAL: ft.Icons.PSYCHOLOGY,
            cls.SOCIAL: ft.Icons.GROUP,
            cls.CREATIVE: ft.Icons.COLOR_LENS,
            cls.PRODUCTIVE: ft.Icons.WORK,
            cls.OTHER: ft.Icons.CHECK_CIRCLE_OUTLINE
        }
        return icons.get(habit_type, ft.Icons.CHECK_CIRCLE_OUTLINE)

    @classmethod
    def get_color(cls, habit_type):
        colors = {
            cls.PHYSICAL: ft.Colors.GREEN,
            cls.MENTAL: ft.Colors.BLUE,
            cls.SOCIAL: ft.Colors.PURPLE,
            cls.CREATIVE: ft.Colors.ORANGE,
            cls.PRODUCTIVE: ft.Colors.RED,
            cls.OTHER: ft.Colors.AMBER
        }
        return colors.get(habit_type, ft.Colors.AMBER)

class HabitsScreen(ft.Container):
    def __init__(self, player, page):
        super().__init__()
        self.player = player
        self.page = page
        
        if not hasattr(self.player, 'habits'):
            self.player.habits = []
        
        self.expand = True
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
        
        self.build_ui()

    def build_ui(self):
        """Build the UI components"""
        self.habit_name_input = ft.TextField(
            label="Habit Name",
            hint_text="Enter habit name...",
            expand=True
        )
        
        self.habit_type_dropdown = ft.Dropdown(
            label="Habit Type",
            options=[ft.dropdown.Option(h_type.name) for h_type in HabitType],
            value=HabitType.OTHER.name,
            expand=True
        )
        
        self.habit_frequency = ft.Dropdown(
            label="Frequency",
            options=[
                ft.dropdown.Option("Daily"),
                ft.dropdown.Option("Weekly"),
                ft.dropdown.Option("Monthly")
            ],
            value="Daily",
            expand=True
        )
        
        self.add_button = ft.ElevatedButton(
            text="Add Habit",
            icon=ft.Icons.ADD,
            on_click=self.add_habit,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                padding=20
            )
        )
        
        self.habits_list = ft.ListView(
            spacing=10,
            divider_thickness=1,
            expand=True
        )
        
        self.content = ft.Column(
            controls=[
                ft.Text("Habits Tracker", size=24, weight="bold"),
                ft.Row([
                    self.habit_name_input,
                    self.habit_type_dropdown,
                    self.habit_frequency,
                    self.add_button
                ], spacing=10),
                ft.Divider(),
                self.habits_list
            ],
            spacing=20
        )
        
        self.load_habits()

    def load_habits(self):
        """Load habits from player data"""
        self.habits_list.controls.clear()
        
        for habit in self.player.habits:
            habit_item = self.create_habit_item(habit)
            self.habits_list.controls.append(habit_item)
        
        self.update()

    def create_habit_item(self, habit):
        """Create a habit list item with interactive controls"""
        def toggle_completed(e):
            today = datetime.now().date()
            last_completed = datetime.strptime(habit['last_completed'], "%Y-%m-%d").date() if habit['last_completed'] else None
            
            if not last_completed or today > last_completed:
                habit['completed_today'] = not habit['completed_today']
                if habit['completed_today']:
                    habit['streak'] += 1
                    habit['last_completed'] = today.strftime("%Y-%m-%d")
                    self.player.add_xp(10)
                else:
                    habit['streak'] = max(0, habit['streak'] - 1)
                
                self.player.save()
                self.update()
                self.page.update()
        
        def edit_habit(e):
            self.show_edit_dialog(habit)
        
        def delete_habit(e):
            self.show_delete_confirmation(habit)
        
        habit_type = HabitType[habit['type']]
        
        return ft.Card(
            content=ft.Container(
                content=ft.ListTile(
                    leading=ft.Icon(
                        HabitType.get_icon(habit_type),
                        color=HabitType.get_color(habit_type),
                        size=40
                    ),
                    title=ft.Text(
                        habit['name'],
                        size=18,
                        weight=ft.FontWeight.BOLD
                    ),
                    subtitle=ft.Column([
                        ft.Text(f"Streak: {habit['streak']} days", size=14),
                        ft.Text(f"Frequency: {habit['frequency']}", size=12),
                    ], spacing=2),
                    trailing=ft.Row([
                        ft.Checkbox(
                            value=habit.get('completed_today', False),
                            on_change=toggle_completed,
                            fill_color=HabitType.get_color(habit_type)
                        ),
                        ft.IconButton(
                            icon=ft.Icons.EDIT,
                            on_click=edit_habit,
                            tooltip="Edit habit",
                            icon_color=ft.Colors.BLUE_300
                        ),
                        ft.IconButton(
                            icon=ft.Icons.DELETE,
                            on_click=lambda e, h=habit: self.show_delete_confirmation(h),
                            tooltip="Delete habit",
                            icon_color=ft.Colors.RED_300
                        ),
                    ], spacing=5, width=150),
                ),
                padding=10,
                border_radius=10,
                bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.WHITE)
            ),
            elevation=2,
            margin=5
        )

    def add_habit(self, e):
        """Add a new habit"""
        name = self.habit_name_input.value.strip()
        if not name:
            return
        
        new_habit = {
            'id': str(len(self.player.habits) + 1),
            'name': name,
            'type': self.habit_type_dropdown.value,
            'frequency': self.habit_frequency.value,
            'streak': 0,
            'xp': 10,
            'completed_today': False,
            'last_completed': None,
            'created_at': datetime.now().strftime("%Y-%m-%d")
        }
        
        self.player.habits.append(new_habit)
        self.player.save()
        self.habit_name_input.value = ""
        self.habits_list.controls.append(self.create_habit_item(new_habit))
        self.update()

    def show_edit_dialog(self, habit):
        """Show dialog to edit habit"""
        name_field = ft.TextField(
            label="Habit Name",
            value=habit['name'],
            expand=True
        )
        
        type_dropdown = ft.Dropdown(
            label="Habit Type",
            options=[ft.dropdown.Option(h_type.name) for h_type in HabitType],
            value=habit['type'],
            expand=True
        )
        
        frequency_dropdown = ft.Dropdown(
            label="Frequency",
            options=[
                ft.dropdown.Option("Daily"),
                ft.dropdown.Option("Weekly"),
                ft.dropdown.Option("Monthly")
            ],
            value=habit['frequency'],
            expand=True
        )
        
        def save_changes(e):
            habit['name'] = name_field.value.strip()
            habit['type'] = type_dropdown.value
            habit['frequency'] = frequency_dropdown.value
            self.player.save()
            self.load_habits()
            dlg.open = False
            self.page.update()
        
        dlg = ft.AlertDialog(
            title=ft.Text("Edit Habit"),
            content=ft.Column(
                controls=[
                    name_field,
                    type_dropdown,
                    frequency_dropdown
                ],
                spacing=10
            ),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: (setattr(dlg, "open", False), self.page.update())),
                ft.TextButton("Save", on_click=save_changes),
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def show_delete_confirmation(self, habit):
        """Show confirmation dialog before deleting habit"""
        def confirm_delete(e):
            print(f"Deleting habit with ID: {habit['id']}")
            print(f"Current habits before deletion: {[h['id'] for h in self.player.habits]}")
            
            self.player.habits = [h for h in self.player.habits if str(h['id']) != str(habit['id'])]
            
            print(f"Current habits after deletion: {[h['id'] for h in self.player.habits]}")
            
            self.player.save()
            self.load_habits()
            dlg.open = False
            self.page.update()
        
        dlg = ft.AlertDialog(
            title=ft.Text("Confirm Delete"),
            content=ft.Text(f"Are you sure you want to delete '{habit['name']}'?"),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: (setattr(dlg, "open", False), self.page.update())),
                ft.TextButton("Delete", on_click=confirm_delete, style=ft.ButtonStyle(color=ft.Colors.RED)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            modal=True
        )
        
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def update(self):
        if self.page:
            self.page.update()