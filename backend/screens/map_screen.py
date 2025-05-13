import flet as ft
import uuid
import time
from dataclasses import dataclass
from typing import Optional, List, Dict, Tuple
from enum import Enum, auto

class VisitType(Enum):
    VACATION = auto()
    HOME = auto()
    WORK = auto()
    ADVENTURE = auto()
    FAMILY = auto()
    EDUCATION = auto()
    OTHER = auto()

    @classmethod
    def get_icon(cls, visit_type: 'VisitType') -> str:
        icons = {
            cls.VACATION: ft.Icons.UMBRELLA,
            cls.HOME: ft.Icons.HOME,
            cls.WORK: ft.Icons.WORK,
            cls.ADVENTURE: ft.Icons.HIKING,
            cls.FAMILY: ft.Icons.FAMILY_RESTROOM,
            cls.EDUCATION: ft.Icons.SCHOOL,
        }
        return icons.get(visit_type, ft.Icons.PLACE)

    @classmethod
    def get_color(cls, visit_type: 'VisitType') -> str:
        colors = {
            cls.VACATION: ft.Colors.CYAN,
            cls.HOME: ft.Colors.GREEN,
            cls.WORK: ft.Colors.BLUE,
            cls.ADVENTURE: ft.Colors.ORANGE,
            cls.FAMILY: ft.Colors.PINK,
            cls.EDUCATION: ft.Colors.PURPLE,
        }
        return colors.get(visit_type, ft.Colors.AMBER)

    @classmethod
    def from_string(cls, value: str) -> 'VisitType':
        try:
            return cls[value.upper()]
        except KeyError:
            return cls.OTHER

@dataclass
class Location:
    id: str
    name: str
    description: str
    x: float  # relative position (0-1)
    y: float  # relative position (0-1)
    visit_type: VisitType
    visited: bool = False
    created_at: float = 0.0  # timestamp for sorting
    updated_at: float = 0.0  # timestamp for sorting

class MapScreen(ft.Container):
    MIN_SCALE = 0.5
    MAX_SCALE = 3.0
    DEFAULT_SCALE = 1.0
    DEFAULT_MAP_WIDTH = 1000
    DEFAULT_MAP_HEIGHT = 700
    
    def __init__(self, player, page):
        super().__init__()
        self.player = player
        self.page = page
        self.locations: Dict[str, Location] = {}
        self.selected_location: Optional[Location] = None
        self.scale = self.DEFAULT_SCALE
        self.offset_x = 0.0
        self.offset_y = 0.0
        self.drag_start: Optional[Tuple[float, float]] = None
        self.map_width = self.DEFAULT_MAP_WIDTH
        self.map_height = self.DEFAULT_MAP_HEIGHT
        self.initialized = False
        self.pending_location_add = False
        self.last_click_x = 0.5
        self.last_click_y = 0.5

        if not hasattr(self.player, 'visited_locations'):
            self.player.visited_locations = []
        
        self.build_ui()

    def did_mount(self):
        self.initialized = True
        self.load_locations()
        self.page.on_resize = self.handle_page_resize

    def will_unmount(self):
        self.page.on_resize = None

    def handle_page_resize(self, e):
        self.update_map_size()

    def build_ui(self):
        """Build the UI components of the map screen"""
        self.create_map_components()
        self.create_edit_components()
        self.create_locations_list()
        self.assemble_main_layout()

    def create_map_components(self):
        """Create all map-related UI components"""
        self.map_image = ft.Image(
            src="https://images.photowall.com/products/84032/world-map-lotr-style-blue.jpg?h=699&q=85",
            fit=ft.ImageFit.CONTAIN,
            repeat=ft.ImageRepeat.NO_REPEAT,
        )
        
        self.map_container = ft.GestureDetector(
            content=self.map_image,
            on_scale_start=self.handle_scale_start,
            on_scale_update=self.handle_scale_update,
            on_pan_start=self.handle_pan_start,
            on_pan_update=self.handle_pan_update,
            on_tap=self.handle_map_tap,
            on_double_tap=self.handle_double_tap,
            on_long_press_end=self.handle_long_press,
        )
        
        self.map_stack = ft.Stack(
            controls=[self.map_container],
            expand=True,
        )
        
        self.map_wrapper = ft.Container(
            content=self.map_stack,
            expand=7,
            padding=10,
            border=ft.border.all(1, ft.Colors.BLUE_200),
            on_hover=self.handle_map_hover,
        )

    def create_edit_components(self):
        self.location_name = ft.TextField(
            label="Location Name",
            expand=True,
        )
    
        self.location_desc = ft.TextField(
            label="Description",
            multiline=True,
            min_lines=3,
            max_lines=5,
            expand=True,
        )
    
        self.visit_type = ft.Dropdown(
            label="Visit Type",
            options=[
                ft.dropdown.Option(key=vt.name, text=vt.name.capitalize())
                for vt in VisitType
            ],
            value=VisitType.VACATION.name,
            expand=True,
        )
    
        self.visited_check = ft.Checkbox(label="Visited", value=True)
    
        self.save_button = ft.ElevatedButton(
            "Save Location",
            icon=ft.Icons.SAVE,
            on_click=self.add_location_from_input,
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.BLUE_700,
        )
    
        self.delete_button = ft.ElevatedButton(
            "Delete Location",
            icon=ft.Icons.DELETE,
            on_click=self.confirm_delete,
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.RED_700,
        )
    
        self.edit_panel = ft.Column(
            controls=[
                ft.Row([self.location_name, self.visit_type]),
                self.location_desc,
                ft.Row([
                    self.visited_check,
                    ft.Container(expand=True),
                    self.save_button,
                    self.delete_button,
                ]),
            ],
            visible=False,
            spacing=10,
        )

    def create_locations_list(self):
        """Create the locations list view"""
        self.locations_list = ft.ListView(
            expand=True,
            spacing=10,
            divider_thickness=1,
        )
        
        self.search_field = ft.TextField(
            label="Search locations",
            on_change=self.update_locations_list,
            prefix_icon=ft.Icons.SEARCH,
            expand=True,
        )
        
        self.sort_dropdown = ft.Dropdown(
            label="Sort by",
            options=[
                ft.dropdown.Option("name"),
                ft.dropdown.Option("visit_type"),
                ft.dropdown.Option("visited"),
                ft.dropdown.Option("recently_added"),
            ],
            value="name",
            on_change=self.update_locations_list,
            width=150,
        )

    def assemble_main_layout(self):
        """Assemble all components into the main layout"""
        self.content = ft.Row(
            controls=[
                self.map_wrapper,
                ft.Column(
                    controls=[
                        ft.Text("Visited Locations", style=ft.TextThemeStyle.HEADLINE_MEDIUM),
                        ft.Row([self.search_field, self.sort_dropdown]),
                        ft.Divider(),
                        self.locations_list,
                        ft.Divider(),
                        self.edit_panel,
                    ],
                    expand=3,
                    scroll=ft.ScrollMode.AUTO,
                    spacing=15,
                ),
            ],
            expand=True,
            spacing=15,
        )

    def update_map_size(self):
        """Update the map dimensions based on current container size"""
        if self.page and self.initialized:
            self.map_width = self.map_wrapper.width or self.DEFAULT_MAP_WIDTH
            self.map_height = self.map_wrapper.height or self.DEFAULT_MAP_HEIGHT
            self.update_pin_positions()

    def load_locations(self):
        """Load sample locations or from persistent storage"""
        self.update_map_size()
        
        sample_locations = [
            Location(
                id=str(uuid.uuid4()),
                name="Home City",
                description="Where I was born and raised",
                x=0.5,
                y=0.5,
                visit_type=VisitType.HOME,
                visited=True,
                created_at=0.0,
                updated_at=0.0,
            ),
            Location(
                id=str(uuid.uuid4()),
                name="Grand Canyon",
                description="Amazing hiking vacation spot",
                x=0.3,
                y=0.4,
                visit_type=VisitType.VACATION,
                visited=True,
                created_at=0.0,
                updated_at=0.0,
            ),
        ]
        
        for loc in sample_locations:
            self.add_location(loc)
        
        self.update_locations_list()

    def add_location(self, location: Location):
        """Add a location to the map and data store"""
        self.locations[location.id] = location
        self.add_pin_to_map(location)
        
        if location.visited and location.id not in self.player.visited_locations:
            self.player.visited_locations.append(location.id)
        self.update_locations_list()

    def add_pin_to_map(self, location: Location):
        if not all([self.map_width, self.map_height]):
            return

        existing_pin = next(
            (c for c in self.map_stack.controls
             if hasattr(c, 'data') and c.data == location.id),
            None
        )

        if existing_pin:
            existing_pin.content.name = VisitType.get_icon(location.visit_type)
            existing_pin.content.color = VisitType.get_color(location.visit_type)
            existing_pin.tooltip = f"{location.name}\n{location.description[:50]}..."
        else:
            pin = ft.Container(
                content=ft.Icon(
                    name=VisitType.get_icon(location.visit_type),
                    color=VisitType.get_color(location.visit_type),
                    size=24,
                ),
                left=location.x * self.map_width * self.scale + self.offset_x,
                top=location.y * self.map_height * self.scale + self.offset_y,
                on_click=lambda e, loc=location: self.select_location(loc),
                tooltip=f"{location.name}\n{location.description[:50]}...",
                data=location.id,
            )
            self.map_stack.controls.append(pin)

        if self.page:
            self.map_stack.update()

    def update_pin_positions(self):
        """Update all pin positions based on current scale and offset"""
        if not all([self.map_width, self.map_height]):
            return
        
        for control in self.map_stack.controls:
            if hasattr(control, 'data') and control.data in self.locations:
                loc = self.locations[control.data]
                control.left = loc.x * self.map_width * self.scale + self.offset_x
                control.top = loc.y * self.map_height * self.scale + self.offset_y
        
        if self.page:
            self.map_stack.update()

    def select_location(self, location: Location):
        """Select a location and update the edit panel"""
        self.selected_location = location
        self.location_name.value = location.name
        self.location_desc.value = location.description
        self.visit_type.value = location.visit_type.name
        self.visited_check.value = location.visited
        self.edit_panel.visible = True
        self.update_locations_list()
        self.page.update()

    def update_locations_list(self, e=None):
        """Update the locations list based on current filter and sort"""
        self.locations_list.controls.clear()
    
        search_term = self.search_field.value.lower() if self.search_field.value else ""
        sort_key = self.sort_dropdown.value
    
        
        filtered_locations = [
            loc for loc in self.locations.values()
            if (search_term in loc.name.lower() or 
                search_term in loc.description.lower())
        ]
    
        if sort_key == "name":
            filtered_locations.sort(key=lambda x: x.name)
        elif sort_key == "visit_type":
            filtered_locations.sort(key=lambda x: x.visit_type.name)
        elif sort_key == "visited":
            filtered_locations.sort(key=lambda x: not x.visited)
        elif sort_key == "recently_added":
            filtered_locations.sort(key=lambda x: x.created_at, reverse=True)
    
        for loc in filtered_locations:
            item = ft.ListTile(
                leading=ft.Icon(
                    VisitType.get_icon(loc.visit_type),
                    color=VisitType.get_color(loc.visit_type),
                ),
                title=ft.Text(loc.name),
                subtitle=ft.Text(loc.description[:50] + "..." if len(loc.description) > 50 else loc.description),
                on_click=lambda e, loc=loc: self.select_location(loc),
                bgcolor=ft.Colors.GREY_800 if loc == self.selected_location else None,
                trailing=ft.Icon(ft.Icons.CHECK_CIRCLE if loc.visited else ft.Icons.RADIO_BUTTON_UNCHECKED),
            )
            self.locations_list.controls.append(item)
    
        self.locations_list.update()

    def add_location_from_input(self, e=None):
        """Add a new location from the input fields"""
        name = self.location_name.value
        desc = self.location_desc.value
        visit_type = VisitType.from_string(self.visit_type.value)
        visited = self.visited_check.value

        if not name.strip():
            return

        location = Location(
            id=str(uuid.uuid4()),
            name=name,
            description=desc,
            x=self.last_click_x,
            y=self.last_click_y,
            visit_type=visit_type,
            visited=visited,
            created_at=time.time(),
            updated_at=time.time(),
        )

        self.add_location(location)
        self.edit_panel.visible = False
        self.update()

    def confirm_delete(self, e=None):
        """Show confirmation dialog for deletion"""
        if not self.selected_location:
            return
            
        def perform_delete(e):
            self._perform_delete()
            confirm_dialog.open = False
            self.page.update()
            
        def cancel_delete(e):
            confirm_dialog.open = False
            self.page.update()
    
        confirm_dialog = ft.AlertDialog(
            title=ft.Text("Confirm Delete"),
            content=ft.Text(f"Are you sure you want to delete '{self.selected_location.name}'?"),
            actions=[
                ft.TextButton("Cancel", on_click=cancel_delete),
                ft.TextButton("Delete", on_click=perform_delete, style=ft.ButtonStyle(color=ft.Colors.RED)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
    
        self.page.dialog = confirm_dialog
        confirm_dialog.open = True
        self.page.update()

    def _perform_delete(self):
        """Actually perform the location deletion"""
        if not self.selected_location:
            return
            
        self.map_stack.controls = [
            c for c in self.map_stack.controls 
            if not hasattr(c, 'data') or c.data != self.selected_location.id
        ]
        
        if self.selected_location.id in self.locations:
            del self.locations[self.selected_location.id]
        
        if self.selected_location.id in self.player.visited_locations:
            self.player.visited_locations.remove(self.selected_location.id)
        
        self.selected_location = None
        self.edit_panel.visible = False
        self.update_locations_list()
        self.map_stack.update()
        self.page.update()

    def handle_scale_start(self, e: ft.ScaleStartEvent):
        """Handle the start of a scaling gesture"""
        self.drag_start = self._get_event_coordinates(e)

    def handle_scale_update(self, e: ft.ScaleUpdateEvent):
        """Handle scaling (pinch zoom) updates"""
        new_scale = max(self.MIN_SCALE, min(self.MAX_SCALE, self.scale * e.scale))
        
        if self.scale != new_scale:
            x, y = self._get_event_coordinates(e)
            focus_x = x - self.offset_x
            focus_y = y - self.offset_y
            self.offset_x -= focus_x * (new_scale / self.scale - 1)
            self.offset_y -= focus_y * (new_scale / self.scale - 1)
            self.scale = new_scale
        
        self.update_pin_positions()

    def handle_pan_start(self, e: ft.DragStartEvent):
        """Handle the start of a pan/drag gesture"""
        self.drag_start = self._get_event_coordinates(e)

    def handle_pan_update(self, e: ft.DragUpdateEvent):
        """Handle pan/drag updates"""
        if self.drag_start:
            x, y = self._get_event_coordinates(e)
            dx = x - self.drag_start[0]
            dy = y - self.drag_start[1]
            self.offset_x += dx
            self.offset_y += dy
            self.drag_start = (x, y)
            self.update_pin_positions()

    def handle_map_tap(self, e: ft.TapEvent):
        """Handle map tap events"""
        local_x = (e.local_x - self.offset_x) / (self.map_width * self.scale)
        local_y = (e.local_y - self.offset_y) / (self.map_height * self.scale)

        self.last_click_x = max(0, min(1, local_x))
        self.last_click_y = max(0, min(1, local_y))

        self.location_name.value = ""
        self.location_desc.value = ""
        self.visit_type.value = VisitType.VACATION.name
        self.visited_check.value = False
        self.edit_panel.visible = True
        self.update()

    def handle_double_tap(self, e: ft.TapEvent):
        """Handle double tap (reset zoom)"""
        self.scale = self.DEFAULT_SCALE
        self.offset_x = 0.0
        self.offset_y = 0.0
        self.update_pin_positions()

    def handle_long_press(self, e: ft.LongPressEndEvent):
        """Handle long press (context menu)"""
        pass

    def handle_map_hover(self, e: ft.HoverEvent):
        """Handle map hover events (tooltip positioning)"""
        pass

    def _get_event_coordinates(self, e) -> Tuple[float, float]:
        """Extract coordinates from an event"""
        return (
            getattr(e, 'local_x', getattr(e, 'x', 0)),
            getattr(e, 'local_y', getattr(e, 'y', 0)),
        )

    def _get_relative_coordinates(self, e) -> Tuple[float, float]:
        """Convert event coordinates to relative map coordinates (0-1)"""
        x, y = self._get_event_coordinates(e)
        
        adjusted_x = (x - self.offset_x) / self.scale
        adjusted_y = (y - self.offset_y) / self.scale
        
        if self.map_width > 0 and self.map_height > 0:
            rel_x = adjusted_x / self.map_width
            rel_y = adjusted_y / self.map_height
            
            return max(0, min(1, rel_x)), max(0, min(1, rel_y))
        
        return 0.5, 0.5

    def update(self):
        """Update the UI"""
        if self.page:
            self.page.update()