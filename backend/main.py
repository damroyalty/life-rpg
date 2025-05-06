import flet as ft
from models.player import Player
from screens.home_screen import HomeScreen
from screens.quests_screen import QuestsScreen
from screens.map_screen import MapScreen
from screens.profile_screen import ProfileScreen
from screens.rewards_screen import RewardsScreen
from screens.settings_screen import SettingsScreen
from screens.habits_screen import HabitsScreen
import traceback

def get_theme(theme_mode=ft.ThemeMode.DARK):
    is_dark = theme_mode == ft.ThemeMode.DARK
    return ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=ft.colors.AMBER,
            secondary=ft.colors.DEEP_PURPLE,
            surface=ft.colors.GREY_900 if is_dark else ft.colors.GREY_100,
            on_surface=ft.colors.WHITE if is_dark else ft.colors.BLACK,
            background=ft.colors.GREY_900 if is_dark else ft.colors.GREY_50,
            surface_variant=ft.colors.GREY_800 if is_dark else ft.colors.GREY_200,
        ),
        text_theme=ft.TextTheme(
            body_large=ft.TextStyle(font_family="Cinzel"),
            title_large=ft.TextStyle(font_family="Cinzel", weight="bold")
        ),
    )

def main(page: ft.Page):
    try:
        page.theme = get_theme(page.theme_mode)
        page.fonts = {
            "Cinzel": "https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&display=swap"
        }
        
        page.title = "Life-RPG"
        page.theme_mode = ft.ThemeMode.DARK
        page.padding = 20
        
        player = Player()
        
        # pass page to MapScreen
        home_screen = HomeScreen(player)
        quests_screen = QuestsScreen(player)
        map_screen = MapScreen(player, page)  # pass page here
        profile_screen = ProfileScreen(player)
        rewards_screen = RewardsScreen(player)
        habits_screen = HabitsScreen(player) 
        settings_screen = SettingsScreen(player, page)
        
        screens = [
            home_screen,
            quests_screen,
            map_screen,
            profile_screen,
            rewards_screen,
            habits_screen,
            settings_screen
        ]
        
        # set the initial screen
        current_screen = ft.AnimatedSwitcher(
            transition=ft.AnimatedSwitcherTransition.FADE,
            duration=200,
            switch_in_curve=ft.AnimationCurve.EASE_IN,
            switch_out_curve=ft.AnimationCurve.EASE_OUT,
            content=home_screen,
            expand=True
        )
        
        # changing tabs
        def change_tab(e):
            selected_index = e.control.selected_index
            if selected_index < len(screens):
                new_screen = screens[selected_index]
                current_screen.content = new_screen
                current_screen.update()
                  
        
        # navigation rail
        rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=200,
        bgcolor=ft.colors.SURFACE_VARIANT,
        indicator_color=ft.colors.AMBER,
        destinations=[
        ft.NavigationRailDestination(
            icon=ft.icons.HOME_OUTLINED, 
            selected_icon=ft.icons.HOME, 
            label="Home"
        ),
        ft.NavigationRailDestination(
            icon=ft.icons.TASK,
            selected_icon=ft.icons.TASK_OUTLINED,
            label="Quests"
        ),
        ft.NavigationRailDestination(
            icon=ft.icons.MAP,
            selected_icon=ft.icons.MAP_OUTLINED,
            label="Map"
        ),
        ft.NavigationRailDestination(
            icon=ft.icons.PERSON,
            selected_icon=ft.icons.PERSON_OUTLINED,
            label="Profile"
        ),
        ft.NavigationRailDestination(
            icon=ft.icons.SHOP,
            selected_icon=ft.icons.SHOP_OUTLINED,
            label="Rewards"
        ),
        ft.NavigationRailDestination(
            icon=ft.icons.CHECK_CIRCLE,
            selected_icon=ft.icons.CHECK_CIRCLE_OUTLINE,
            label="Habits"
        ),
        ft.NavigationRailDestination(
            icon=ft.icons.SETTINGS,
            selected_icon=ft.icons.SETTINGS_OUTLINED,
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

ft.app(target=main)