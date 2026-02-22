"""
Reusable UI Components
Purpose: Build-once, use-everywhere widgets
Author: Aristides A. Morcillo

"""

import flet as ft
from src.ui.theme import AppTheme


class AppHeader(ft.UserControl):
    """
    Reusable app header with logo and title.
    Used on all screens for consistency.
    """
    
    def __init__(self, title: str = "AI Business Assistant"):
        super().__init__()
        self.title = title
    
    def build(self):
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.icons.SMART_TOY, color=ft.colors.WHITE, size=32),
                    ft.Text(
                        self.title,
                        size=AppTheme.FONT_SIZE_LARGE,
                        weight=ft.FontWeight.BOLD,
                        color=ft.colors.WHITE
                    )
                ],
                spacing=15
            ),
            gradient=AppTheme.get_gradient(),
            padding=AppTheme.PADDING_MEDIUM,
            border_radius=0
        )


class StatsCard(ft.UserControl):
    """
    Reusable stat display card.
    Used for showing metrics like "10 rows validated"
    """
    
    def __init__(self, label: str, value: str, icon: str = None, color: str = None):
        super().__init__()
        self.label = label
        self.value = value
        self.icon = icon
        self.color = color or AppTheme.PRIMARY
    
    def build(self):
        icon_widget = None
        if self.icon:
            icon_widget = ft.Icon(self.icon, color=self.color, size=40)
        
        return ft.Container(
            content=ft.Column(
                controls=[
                    icon_widget if icon_widget else ft.Container(height=0),
                    ft.Text(
                        self.value,
                        size=AppTheme.FONT_SIZE_LARGE,
                        weight=ft.FontWeight.BOLD,
                        color=self.color
                    ),
                    ft.Text(
                        self.label,
                        size=AppTheme.FONT_SIZE_SMALL,
                        color=AppTheme.TEXT_SECONDARY
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=5
            ),
            bgcolor=AppTheme.SURFACE,
            padding=AppTheme.PADDING_MEDIUM,
            border_radius=AppTheme.RADIUS_MEDIUM,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=10,
                color=ft.colors.with_opacity(0.1, AppTheme.TEXT_PRIMARY)
            ),
            expand=True
        )


class ActionButton(ft.ElevatedButton):
    """
    Reusable primary action button.
    Consistent styling across all screens.
    """
    
    def __init__(self, text: str, on_click, icon: str = None, **kwargs):
        super().__init__(
            text=text,
            icon=icon,
            on_click=on_click,
            style=ft.ButtonStyle(
                color=ft.colors.WHITE,
                bgcolor=AppTheme.PRIMARY,
                padding=ft.padding.symmetric(horizontal=30, vertical=15),
                shape=ft.RoundedRectangleBorder(radius=AppTheme.RADIUS_SMALL)
            ),
            **kwargs
        )


class InfoCard(ft.UserControl):
    """
    Reusable information card with icon and text.
    Used for instructions, tips, alerts.
    """
    
    def __init__(self, title: str, message: str, card_type: str = "info"):
        super().__init__()
        self.title = title
        self.message = message
        self.card_type = card_type
        
        # Set colors based on type
        self.colors = {
            "info": (AppTheme.INFO, ft.icons.INFO_OUTLINED),
            "success": (AppTheme.SUCCESS, ft.icons.CHECK_CIRCLE_OUTLINE),
            "warning": (AppTheme.WARNING, ft.icons.WARNING_AMBER_OUTLINED),
            "error": (AppTheme.ERROR, ft.icons.ERROR_OUTLINE)
        }
    
    def build(self):
        color, icon = self.colors.get(self.card_type, self.colors["info"])
        
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(icon, color=color, size=30),
                    ft.Column(
                        controls=[
                            ft.Text(
                                self.title,
                                size=AppTheme.FONT_SIZE_MEDIUM,
                                weight=ft.FontWeight.BOLD,
                                color=color
                            ),
                            ft.Text(
                                self.message,
                                size=AppTheme.FONT_SIZE_NORMAL,
                                color=AppTheme.TEXT_PRIMARY
                            )
                        ],
                        spacing=5,
                        expand=True
                    )
                ],
                spacing=15
            ),
            bgcolor=ft.colors.with_opacity(0.1, color),
            padding=AppTheme.PADDING_MEDIUM,
            border_radius=AppTheme.RADIUS_MEDIUM,
            border=ft.border.all(2, color)
        )