import flet as ft
from models.player import Player
from screens.home_screen import HomeScreen
from screens.quests_screen import QuestsScreen
from screens.map_screen import MapScreen
from screens.profile_screen import ProfileScreen
from screens.rewards_screen import RewardsScreen
from screens.settings_screen import SettingsScreen
from screens.habits_screen import HabitsScreen
from screens.memento_mori_screen import MementoMoriScreen
import traceback

def get_theme(theme_mode=ft.ThemeMode.DARK):
    is_dark = theme_mode == ft.ThemeMode.DARK
    return ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=ft.Colors.BLUE_200,
            secondary=ft.Colors.DEEP_PURPLE,
            surface=ft.Colors.GREY_900 if is_dark else ft.Colors.GREY_100,
            on_surface=ft.Colors.WHITE if is_dark else ft.Colors.BLACK,
            background=ft.Colors.GREY_900 if is_dark else ft.Colors.GREY_50,
            surface_variant=ft.Colors.GREY_800 if is_dark else ft.Colors.GREY_200,
            on_primary_container=ft.Colors.BLUE_200,
            primary_container=ft.Colors.BLUE_200,
        ),
    )

def main(page: ft.Page):
    try:
        page.window.width = 1400
        page.window.height = 1000
        page.window.resizable = True
        page.window.center()
        page.theme = get_theme(page.theme_mode)
        page.fonts = {
            "Cinzel": "https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&display=swap"
        }
        
        page.title = "Life-RPG"
        page.theme_mode = ft.ThemeMode.DARK
        page.padding = 20
        
        player = Player()
        
        home_screen = HomeScreen(player)
        quests_screen = QuestsScreen(player)
        map_screen = MapScreen(player, page)
        profile_screen = ProfileScreen(player)
        rewards_screen = RewardsScreen(player)
        habits_screen = HabitsScreen(player, page)  
        settings_screen = SettingsScreen(player, page)
        memento_mori_screen = MementoMoriScreen()

        
        screens = [
            home_screen,
            quests_screen,
            map_screen,
            profile_screen,
            rewards_screen,
            habits_screen,
            memento_mori_screen,
            settings_screen
        ]
        
        current_screen = ft.AnimatedSwitcher(
            transition=ft.AnimatedSwitcherTransition.FADE,
            duration=50,
            switch_in_curve=ft.AnimationCurve.EASE_IN,
            switch_out_curve=ft.AnimationCurve.EASE_OUT,
            content=home_screen,
            expand=True
        )
        
        def change_tab(e):
            selected_index = e.control.selected_index
            if selected_index < len(screens):
                new_screen = screens[selected_index]
                current_screen.content = new_screen
                current_screen.update()
                  
        
        rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=200,
        bgcolor=ft.Colors.ON_SURFACE_VARIANT,
        indicator_color=ft.Colors.AMBER,
        destinations=[
    ft.NavigationRailDestination(
        icon=ft.Icon(name=ft.Icons.HOME_OUTLINED, color=ft.Colors.WHITE),
        selected_icon=ft.Icon(name=ft.Icons.HOME, color=ft.Colors.AMBER_300),
        label="Home"
    ),
    ft.NavigationRailDestination(
        icon=ft.Icon(name=ft.Icons.TASK_OUTLINED, color=ft.Colors.WHITE),
        selected_icon=ft.Icon(name=ft.Icons.TASK, color=ft.Colors.AMBER_300),
        label="Quests"
    ),
    ft.NavigationRailDestination(
        icon=ft.Icon(name=ft.Icons.MAP_OUTLINED, color=ft.Colors.WHITE),
        selected_icon=ft.Icon(name=ft.Icons.MAP, color=ft.Colors.AMBER_300),
        label="Map"
    ),
    ft.NavigationRailDestination(
        icon=ft.Icon(name=ft.Icons.PERSON_OUTLINED, color=ft.Colors.WHITE),
        selected_icon=ft.Icon(name=ft.Icons.PERSON, color=ft.Colors.AMBER_300),
        label="Profile"
    ),
    ft.NavigationRailDestination(
        icon=ft.Icon(name=ft.Icons.SHOP_OUTLINED, color=ft.Colors.WHITE),
        selected_icon=ft.Icon(name=ft.Icons.SHOP, color=ft.Colors.AMBER_300),
        label="Rewards"
    ),
    ft.NavigationRailDestination(
        icon=ft.Icon(name=ft.Icons.CHECK_CIRCLE_OUTLINE, color=ft.Colors.WHITE),
        selected_icon=ft.Icon(name=ft.Icons.CHECK_CIRCLE, color=ft.Colors.AMBER_300),
        label="Habits"
    ),
    ft.NavigationRailDestination(
        icon=ft.Icon(name=ft.Icons.CALENDAR_MONTH_OUTLINED, color=ft.Colors.WHITE),
        selected_icon=ft.Icon(name=ft.Icons.CALENDAR_MONTH, color=ft.Colors.AMBER_300),
        label="Memento Mori"
    ),
    ft.NavigationRailDestination(
        icon=ft.Icon(name=ft.Icons.SETTINGS_OUTLINED, color=ft.Colors.WHITE),
        selected_icon=ft.Icon(name=ft.Icons.SETTINGS, color=ft.Colors.AMBER_300),
        label="Settings"
        ),
    ],
    on_change=change_tab
)
        
        page.add(
            ft.Row(
                [
                    rail,
                    ft.VerticalDivider(width=1),
                    current_screen,
                ],
                expand=True,
            )
        )

    except Exception as e:
        page.add(
            ft.Text("Error initializing app:", color="grey"),
            ft.Text(str(e)),
            ft.Text("Please check the console for details")
        )
        page.update()
        print(f"Error: {e}\n{traceback.format_exc()}")

ft.app(target=main, view=ft.AppView.FLET_APP)
