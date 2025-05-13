import flet as ft
import asyncio

class NotificationManager:
    def __init__(self, page):
        self.page = page
        self.notification_stack = ft.Stack()
        self.page.overlay.append(self.notification_stack)
        self.page.update()
    
    async def show_notification(self, message, icon=ft.icons.INFO, duration=3):
        notification = ft.Container(
            content=ft.Row([
                ft.Icon(icon, color="white"),
                ft.Text(message, color="white")
            ]),
            bgcolor=ft.colors.BLUE_GREY_800,
            padding=15,
            border_radius=10,
            opacity=0,
            animate_opacity=300,
            top=20,
            right=20
        )
        
        self.notification_stack.controls.append(notification)
        self.page.update()
        
        notification.opacity = 1
        await self.page.update_async()
        
        await asyncio.sleep(duration)
        
        notification.opacity = 0
        await self.page.update_async()
        
        self.notification_stack.controls.remove(notification)
        await self.page.update_async()