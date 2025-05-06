import flet as ft
import uuid

class MapScreen(ft.UserControl):
    def __init__(self, player, page):
        super().__init__()
        self.player = player
        self.page = page
        self.dialog_open = False


        self.base_width = 800
        self.base_height = 500
        self.map_image_url = "https://images.photowall.com/products/84032/world-map-lotr-style-blue.jpg?h=699&q=85"

        if not hasattr(player, "visited_locations"):
            self.player.visited_locations = []

        self.visited_locations = player.visited_locations
        self.location_markers = ft.Stack()
        self.visited_locations_column = ft.Column(spacing=6, scroll=ft.ScrollMode.AUTO, expand=True)
        self.current_location_name = ft.Text("Click on the map to mark a location", italic=True, color=ft.colors.GREY_500)

        # zoom and pan state
        self.map_scale = 1.0
        self.pan_offset_x = 0
        self.pan_offset_y = 0
        self.is_panning = False
        self.start_drag = None

        # pin types
        self.pin_types = {
            "city": {"icon": ft.icons.LOCATION_CITY, "color": ft.colors.BLUE},
            "landmark": {"icon": ft.icons.LANDSCAPE, "color": ft.colors.GREEN},
            "danger": {"icon": ft.icons.WARNING, "color": ft.colors.RED},
            "mystery": {"icon": ft.icons.QUESTION_MARK, "color": ft.colors.PURPLE},
            "treasure": {"icon": ft.icons.ATTACH_MONEY, "color": ft.colors.AMBER},
            "home": {"icon": ft.icons.HOME, "color": ft.colors.PINK},
            "work": {"icon": ft.icons.WORK, "color": ft.colors.ORANGE},
        }
        self.default_pin_type = "city"

    def build(self):
        self.map_image = ft.Image(
            src=self.map_image_url,
            width=self.base_width * self.map_scale,
            height=self.base_height * self.map_scale,
            fit=ft.ImageFit.CONTAIN,
        )

        self.map_container = ft.Container(
            content=self.map_image,
            left=self.pan_offset_x,
            top=self.pan_offset_y,
        )

        # map and markers
        self.main_stack = ft.Stack(
            controls=[
                self.map_container,
                self.location_markers
            ],
            width=self.base_width,
            height=self.base_height,
        )

        # gesture detector for the entire map area
        self.gesture_detector = ft.GestureDetector(
            mouse_cursor=ft.MouseCursor.MOVE,
            on_pan_start=self.start_panning,
            on_pan_update=self.do_panning,
            on_pan_end=self.stop_panning,
            on_tap_down=self.on_map_click,
            content=self.main_stack,
        )

        # clip container for the map area
        self.map_clip_container = ft.Container(
            content=self.gesture_detector,
            width=self.base_width,
            height=self.base_height,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            border_radius=ft.border_radius.all(10),
            bgcolor=ft.colors.BLACK,
        )

        # visited locations panel
        visited_container = ft.Container(
            content=ft.Column([
                ft.Text("Visited Locations", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.CYAN_200),
                self.visited_locations_column,
                ft.ElevatedButton(
                    text="Clear All Locations",
                    icon=ft.icons.DELETE,
                    icon_color=ft.colors.RED_400,
                    color=ft.colors.RED_400,
                    on_click=self.clear_all_locations,
                ) if self.visited_locations else None,
            ], spacing=10),
            width=300,
            padding=10,
            bgcolor=ft.colors.with_opacity(0.04, ft.colors.GREY_900),
            border_radius=ft.border_radius.all(8),
            border=ft.border.all(1, ft.colors.with_opacity(0.15, ft.colors.GREY_700)),
        )

        # zoom controls
        zoom_controls = ft.Row(
            spacing=8,
            controls=[
                ft.IconButton(icon=ft.icons.ZOOM_IN, on_click=self.zoom_in, tooltip="Zoom In"),
                ft.IconButton(icon=ft.icons.ZOOM_OUT, on_click=self.zoom_out, tooltip="Zoom Out"),
                ft.IconButton(icon=ft.icons.CROP_FREE, on_click=self.reset_zoom, tooltip="Reset Zoom"),
            ]
        )

        return ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        ft.Text("🗺️ Places Traveled", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.CYAN_100),
                        zoom_controls,
                        self.map_clip_container,
                        self.current_location_name,
                    ],
                    spacing=16,
                    expand=True
                ),
                visited_container
            ],
            spacing=20,
            expand=True
        )

    def did_mount(self):
        # migrate old locations to include absolute coordinates if missing
        for loc in self.visited_locations:
            if "absolute_x" not in loc:
                loc["absolute_x"] = loc["x_pct"] * self.base_width / 100
                loc["absolute_y"] = loc["y_pct"] * self.base_height / 100
            if "pin_type" not in loc:
                loc["pin_type"] = self.default_pin_type
            if "id" not in loc:
                loc["id"] = str(uuid.uuid4())
        self.update_ui()

    def on_map_click(self, e):
        if self.dialog_open or self.is_panning:
            return

        if e.control != self.gesture_detector:
            return

        true_x = (e.local_x - self.pan_offset_x) / self.map_scale
        true_y = (e.local_y - self.pan_offset_y) / self.map_scale
        
        if not (0 <= true_x <= self.base_width and 0 <= true_y <= self.base_height):
            return
        
        self.open_location_dialog(true_x, true_y)

    def open_location_dialog(self, true_x, true_y):
        x_pct = (true_x / self.base_width) * 100
        y_pct = (true_y / self.base_height) * 100

        name_field = ft.TextField(label="Location Name", autofocus=True)
        notes_field = ft.TextField(label="Notes (optional)", multiline=True)
        
        pin_type_dropdown = ft.Dropdown(
            label="Pin Type",
            options=[ft.dropdown.Option(text=f"{config['icon']} {key.capitalize()}", key=key) 
                    for key, config in self.pin_types.items()],
            value=self.default_pin_type,
            width=200
        )

        def save_location(_):
            name = name_field.value.strip()
            notes = notes_field.value.strip()
            if name:
                new_location = {
                    "id": str(uuid.uuid4()),
                    "name": name, 
                    "x_pct": x_pct, 
                    "y_pct": y_pct, 
                    "notes": notes,
                    "absolute_x": true_x,
                    "absolute_y": true_y,
                    "pin_type": pin_type_dropdown.value
                }
                self.visited_locations.append(new_location)
                self.close_dialog()
                self.update_ui()

        self.dialog_open = True
        self.page.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("New Location"),
            content=ft.Column([
                name_field,
                notes_field,
                pin_type_dropdown
            ], tight=True),
            actions=[ 
                ft.TextButton("Save", on_click=save_location),
                ft.TextButton("Cancel", on_click=lambda _: self.close_dialog()),
            ],
        )
        self.page.dialog.open = True
        self.page.update()

    def close_dialog(self):
        self.dialog_open = False
        self.page.dialog.open = False
        self.page.update()

    def update_ui(self):
        # diff pins
        self.location_markers.controls = []
        for loc in self.visited_locations:
            pin_type = loc.get("pin_type", self.default_pin_type)
            pin_config = self.pin_types.get(pin_type, self.pin_types[self.default_pin_type])
            
            marker = ft.Container(
                left=loc.get("absolute_x", loc["x_pct"] * self.base_width / 100) * self.map_scale + self.pan_offset_x - 12,
                top=loc.get("absolute_y", loc["y_pct"] * self.base_height / 100) * self.map_scale + self.pan_offset_y - 12,
                content=ft.Icon(
                    pin_config["icon"],
                    size=26,
                    color=pin_config["color"],
                    tooltip=f"{loc['name']}\nType: {pin_type.capitalize()}\n{loc.get('notes', '')}"
                ),
                on_click=lambda e, loc=loc: self.show_location_popup(loc),
                data="marker",
            )
            self.location_markers.controls.append(marker)

        # icon colors
        self.visited_locations_column.controls = []
        for loc in self.visited_locations:
            pin_type = loc.get("pin_type", self.default_pin_type)
            pin_config = self.pin_types.get(pin_type, self.pin_types[self.default_pin_type])
            
            btn = ft.TextButton(
                content=ft.Row([
                    ft.Icon(pin_config["icon"], color=pin_config["color"]),
                    ft.Column([
                        ft.Text(loc["name"], weight=ft.FontWeight.BOLD, color=ft.colors.CYAN_100),
                        ft.Text(loc.get("notes", ""), size=12, italic=True, color=ft.colors.GREY_400),
                    ], spacing=2),
                ], spacing=10),
                style=ft.ButtonStyle(
                    padding=10,
                    shape=ft.RoundedRectangleBorder(radius=6),
                    overlay_color=ft.colors.with_opacity(0.1, ft.colors.CYAN),
                ),
                on_click=lambda e, loc=loc: self.show_location_popup(loc),
            )
            self.visited_locations_column.controls.append(btn)

        self.update()

    def show_location_popup(self, location):
        note_field = ft.TextField(
            label="Notes", 
            multiline=True, 
            value=location.get("notes", ""),
        )
        
        # pin type selector
        pin_type = location.get("pin_type", self.default_pin_type)
        pin_type_dropdown = ft.Dropdown(
            label="Pin Type",
            options=[ft.dropdown.Option(text=f"{config['icon']} {key.capitalize()}", key=key) 
                    for key, config in self.pin_types.items()],
            value=pin_type,
            width=200
        )

        def save_location(_):
            location["notes"] = note_field.value
            location["pin_type"] = pin_type_dropdown.value
            self.close_dialog()
            self.update_ui()

        def delete_location(_):
            self.visited_locations.remove(location)
            self.close_dialog()
            self.update_ui()

        def center_on_location(_):
            self.pan_offset_x = -location["absolute_x"] * self.map_scale + self.base_width / 2
            self.pan_offset_y = -location["absolute_y"] * self.map_scale + self.base_height / 2
            self.update_zoom_and_pan()
            self.close_dialog()

        self.page.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Row([
                ft.Icon(self.pin_types[pin_type]["icon"], color=self.pin_types[pin_type]["color"]),
                ft.Text(location["name"]),
            ], spacing=10),
            content=ft.Column([
                ft.Text(f"Coordinates: {location['x_pct']:.1f}%, {location['y_pct']:.1f}%"),
                note_field,
                pin_type_dropdown
            ], tight=True),
            actions=[
                ft.TextButton("Center", on_click=center_on_location),
                ft.TextButton("Delete", on_click=delete_location, style=ft.ButtonStyle(color=ft.colors.RED)),
                ft.TextButton("Save", on_click=save_location),
                ft.TextButton("Close", on_click=lambda _: self.close_dialog()),
            ],
        )
        self.page.dialog.open = True
        self.page.update()

    def show_pin_filter(self, e):
        # pin checkboxes
        pin_filters = []
        for pin_type, config in self.pin_types.items():
            pin_filters.append(
                ft.Checkbox(
                    label=f"{config['icon']} {pin_type.capitalize()}",
                    value=True,
                    data=pin_type,
                    on_change=self.update_pin_filters
                )
            )

        self.page.dialog = ft.AlertDialog(
            title=ft.Text("Filter Pin Types"),
            content=ft.Column(pin_filters, scroll=ft.ScrollMode.AUTO),
            actions=[
                ft.TextButton("Close", on_click=lambda _: self.close_dialog()),
            ]
        )
        self.page.dialog.open = True
        self.page.update()

    def update_pin_filters(self, e):
        # filter pins
        pass

    def clear_all_locations(self, e):
        self.visited_locations.clear()
        self.update_ui()

    def update_zoom_and_pan(self):
        """Update the map display based on current zoom and pan"""
        max_pan_x = max(0, (self.base_width * self.map_scale - self.base_width) / 2)
        max_pan_y = max(0, (self.base_height * self.map_scale - self.base_height) / 2)
        
        self.pan_offset_x = max(-max_pan_x, min(max_pan_x, self.pan_offset_x))
        self.pan_offset_y = max(-max_pan_y, min(max_pan_y, self.pan_offset_y))

        self.map_image.width = self.base_width * self.map_scale
        self.map_image.height = self.base_height * self.map_scale
        self.map_container.left = self.pan_offset_x
        self.map_container.top = self.pan_offset_y
        
        self.update_ui()

    def zoom_in(self, _):
        old_scale = self.map_scale
        self.map_scale = min(3.0, self.map_scale + 0.2)
        zoom_factor = self.map_scale / old_scale
        self.pan_offset_x *= zoom_factor
        self.pan_offset_y *= zoom_factor
        self.update_zoom_and_pan()

    def zoom_out(self, _):
        old_scale = self.map_scale
        self.map_scale = max(0.5, self.map_scale - 0.2)
        zoom_factor = self.map_scale / old_scale
        self.pan_offset_x *= zoom_factor
        self.pan_offset_y *= zoom_factor
        self.update_zoom_and_pan()

    def reset_zoom(self, _):
        self.map_scale = 1.0
        self.pan_offset_x = 0
        self.pan_offset_y = 0
        self.update_zoom_and_pan()

    def start_panning(self, e):
        self.is_panning = True
        self.start_drag = (e.local_x, e.local_y)

    def do_panning(self, e):
        if self.is_panning and self.start_drag:
            dx = e.local_x - self.start_drag[0]
            dy = e.local_y - self.start_drag[1]  
            self.pan_offset_x += dx
            self.pan_offset_y += dy
            self.start_drag = (e.local_x, e.local_y)
            self.update_zoom_and_pan()

    def stop_panning(self, e):
        self.is_panning = False
        self.start_drag = None
        