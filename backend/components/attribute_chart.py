import flet as ft

class AttributeChart(ft.Container):
    def __init__(self, attributes):
        super().__init__()
        self.attributes = attributes
        self.width = 320
        self.height = 200
        self.content = self.build()
        self.padding = 10
        self.bgcolor = ft.colors.with_opacity(0.3, "#1e293b")  # semi-transparent
        self.border_radius = 12
        self.border = ft.border.all(1, ft.colors.with_opacity(0.1, "white"))
        self.shadow = ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.colors.with_opacity(0.2, "black"),
            offset=ft.Offset(0, 0),
        )
        self.gradient = ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=[
                ft.colors.with_opacity(0.1, "#1e293b"),
                ft.colors.with_opacity(0.2, "#0f172a"),
            ],
        )
    
    def build(self):
        attributes = [
            ("strength", "Physical power and might"),
            ("intelligence", "Mental acuity and knowledge"),
            ("charisma", "Social influence and charm"),
            ("endurance", "Stamina and resilience"),
            ("creativity", "Imagination and innovation")
        ]
        
        max_value = max(self.attributes.values()) if self.attributes else 1
        
        return ft.Column(
            controls=[
                ft.Text("Attributes", size=16, weight="bold"),
                *[
                    ft.Column([
                        ft.Row([
                            ft.Text(name.capitalize(), width=100),
                            ft.Tooltip(
                                message=desc,
                                content=ft.Icon(ft.icons.INFO_OUTLINE, size=15)
                            )
                        ]),
                        ft.Stack([
                            ft.Container(
                                width=200,
                                height=20,
                                bgcolor="#334155",
                                border_radius=10
                            ),
                            ft.Container(
                                width=200 * (self.attributes.get(name, 0)/max_value),
                                height=20,
                                bgcolor=self._get_attribute_color(name),
                                border_radius=10,
                                animate=ft.animation.Animation(300, "easeOut")
                            ),
                            ft.Text(
                                str(self.attributes.get(name, 0)),
                                color="white",
                                left=170,
                                weight="bold"
                            )
                        ], height=20)
                    ], spacing=5)
                    for name, desc in attributes
                ]
            ],
            spacing=10
        )
    
    def _get_attribute_color(self, attribute):
        colors = {
            "strength": "#ef4444",    # red
            "intelligence": "#3b82f6", # blue
            "charisma": "#ec4899",    # pink
            "endurance": "#10b981",   # green
            "creativity": "#f59e0b"   # amber
        }
        return colors.get(attribute, "#3b82f6")