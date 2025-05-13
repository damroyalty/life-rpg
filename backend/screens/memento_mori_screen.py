import flet as ft
from datetime import datetime

class MementoMoriScreen(ft.Container):
    def __init__(self):
        super().__init__()
        self.expand = True
        self._initialized = False
        self.build()
        
    def build(self):
        months = [
            ("1", "January"), ("2", "February"), ("3", "March"),
            ("4", "April"), ("5", "May"), ("6", "June"),
            ("7", "July"), ("8", "August"), ("9", "September"),
            ("10", "October"), ("11", "November"), ("12", "December")
        ]
        
        today = datetime.now()
        
        self.day_dropdown = ft.Dropdown(
            width=80,
            label="Day",
            options=[ft.dropdown.Option(str(i)) for i in range(1, 32)],
            value=str(today.day),
            text_style=ft.TextStyle(color=ft.Colors.BLUE_GREY)

        )
        
        self.month_dropdown = ft.Dropdown(
            width=120,
            label="Month",
            options=[ft.dropdown.Option(num, text=name) for num, name in months],
            value=str(today.month),
            text_style=ft.TextStyle(color=ft.Colors.BLUE_GREY)
        )
        
        self.year_dropdown = ft.Dropdown(
            width=100,
            label="Year",
            options=[ft.dropdown.Option(str(i)) for i in range(today.year-100, today.year+1)],
            value=str(today.year),
            text_style=ft.TextStyle(color=ft.Colors.BLUE_GREY)
        )
        
        self.date_display = ft.Text(
            size=16,
            weight="bold",
            color=ft.Colors.BLUE_700
        )
        
        self.life_expectancy_field = ft.Slider(
            min=50,
            max=120,
            divisions=70,
            label="{value} years",
            value=80,
            width=400
        )
        
        self.grid_area = ft.Column()
    
        self.content = ft.Column(
            controls=[
                ft.Row(
                    controls=[
        ft.Text("Memento Mori Calendar", size=24, weight="bold"),
        ft.Text(
            '"Remember, O soul, thy time is finite—each breath a sacred ember in the fire of fate."\n'
            'Remember you must die. Not to be morbid, but to inspire living with purpose.\n'
            '"Let us prepare our minds as if we\'d come to the very end of life." - Seneca\n'
            'Ancient practice of reflecting on mortality to prioritize what truly matters in life',
            size=16,
            italic=True,
            color=ft.Colors.WHITE10,
            text_align=ft.TextAlign.END,
            expand=True
        ),
                ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
                
                ft.Row(
                    controls=[
                        self.day_dropdown,
                        self.month_dropdown,
                        self.year_dropdown,
                        ft.IconButton(
                            icon=ft.Icons.REFRESH,
                            tooltip="Update Date",
                            on_click=self._update_date_display
                        )
                    ],
                    spacing=10,
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                
                self.date_display,
                
                ft.Row(
                    controls=[
                        ft.Text("Life Expectancy:"),
                        self.life_expectancy_field
                    ],
                    spacing=10,
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                
                ft.ElevatedButton(
                    "Generate Life Calendar",
                    icon=ft.Icons.CALENDAR_VIEW_MONTH,
                    on_click=self.generate_calendar,
                    style=ft.ButtonStyle(
                        padding=20,
                        shape=ft.RoundedRectangleBorder(radius=10)
                    )
                ),
                
                ft.Container(
                    content=self.grid_area,
                    padding=20,
                    border_radius=10,
                    border=ft.border.all(1, ft.Colors.GREY_400),
                    expand=True
                ),
                
            ],
            spacing=20,
            expand=True,
            scroll=ft.ScrollMode.AUTO
        )
        
        self._initialized = True
        
    def did_mount(self):
        """Called when the control is added to the page"""
        self._update_date_display(None)
        
    def _update_date_display(self, e):
        """Updates the date text display"""
        if not self._initialized:
            return
            
        try:
            day = int(self.day_dropdown.value)
            month = int(self.month_dropdown.value)
            year = int(self.year_dropdown.value)
            date_str = f"{year}-{month:02d}-{day:02d}"
            self.date_display.value = f"Selected date: {date_str}"
            if self.page:
                self.update()
        except:
            self.date_display.value = "Select a valid date"
            if self.page:
                self.update()
    
    def generate_calendar(self, e):
        try:
            day = int(self.day_dropdown.value)
            month = int(self.month_dropdown.value)
            year = int(self.year_dropdown.value)
            dob = datetime(year, month, day)
            
            today = datetime.now()
            if dob > today:
                raise ValueError("Birth date cannot be in the future")
            
            life_expectancy = int(self.life_expectancy_field.value)
            
            self.grid_area.controls.clear()

            total_weeks = life_expectancy * 52
            lived_weeks = (today - dob).days // 7
            lived_weeks = max(0, min(lived_weeks, total_weeks))

            max_width = 700
            box_width = max(6, min(12, max_width // 60))
            box_height = box_width

            for year_num in range(life_expectancy):
                week_boxes = []
                for week in range(52):
                    index = year_num * 52 + week
                    color = ft.Colors.BLACK if index < lived_weeks else ft.Colors.WHITE
                    border_color = ft.Colors.GREY_400 if index < lived_weeks else ft.Colors.GREY_200
                    
                    week_boxes.append(
                        ft.Container(
                            width=box_width,
                            height=box_height,
                            bgcolor=color,
                            border=ft.border.all(0.5, border_color),
                            margin=0.5,
                            tooltip=f"Year {year_num}, Week {week+1}" if index < lived_weeks else f"Year {year_num}, Week {week+1} (Future)"
                        )
                    )

                label = f"{year_num}" if year_num % 5 == 0 else ""
                row = ft.Row(
                    controls=[
                        *week_boxes,
                        ft.Container(
                            content=ft.Text(label, size=10),
                            width=30,
                            alignment=ft.alignment.center_left
                        )
                    ],
                    spacing=0
                )
                self.grid_area.controls.append(row)

            self.grid_area.controls.append(
                ft.Row(
                    controls=[
                        ft.Container(
                            width=20,
                            height=20,
                            bgcolor=ft.Colors.BLACK,
                            border=ft.border.all(1, ft.Colors.GREY_400)
                        ),
                        ft.Text("Lived weeks", size=12),
                        ft.Container(
                            width=20,
                            height=20,
                            bgcolor=ft.Colors.WHITE,
                            border=ft.border.all(1, ft.Colors.GREY_200)
                        ),
                        ft.Text("Remaining weeks", size=12)
                    ],
                    spacing=10,
                    alignment=ft.MainAxisAlignment.CENTER
                )
            )
            

            self.update()

        except ValueError as ve:
            self.grid_area.controls.clear()
            self.grid_area.controls.append(
                ft.Text(f"Validation Error: {str(ve)}", color=ft.Colors.RED, size=16)
            )
            self.update()
        except Exception as ex:
            self.grid_area.controls.clear()
            self.grid_area.controls.append(
                ft.Text(f"Unexpected Error: {str(ex)}", color=ft.Colors.RED, size=16)
            )
            self.update()