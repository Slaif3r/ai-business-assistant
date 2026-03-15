"""
Reusable UI Components
Purpose: Build-once, use-everywhere widgets
"""

import flet as ft

from ai_business_assistant.ui.theme import AppTheme


def create_app_header(title: str = "AI Business Assistant"):
    """Reusable app header with logo and title"""
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Text("🤖", size=32, color="white"),
                ft.Text(
                    title,
                    size=AppTheme.FONT_SIZE_LARGE,
                    weight=ft.FontWeight.BOLD,
                    color="white",
                ),
            ],
            spacing=15,
        ),
        gradient=AppTheme.get_gradient(),
        padding=AppTheme.PADDING_MEDIUM,
        border_radius=0,
    )


def create_stats_card(label: str, value: str, icon: str = None, color: str = None):
    """Reusable stat display card"""
    color = color or AppTheme.PRIMARY
    icon_widget = (
        ft.Icon(icon, color=color, size=40) if icon else ft.Container(height=0)
    )

    return ft.Container(
        content=ft.Column(
            controls=[
                icon_widget,
                ft.Text(
                    value,
                    size=AppTheme.FONT_SIZE_LARGE,
                    weight=ft.FontWeight.BOLD,
                    color=color,
                ),
                ft.Text(
                    label, size=AppTheme.FONT_SIZE_SMALL, color=AppTheme.TEXT_SECONDARY
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=5,
        ),
        bgcolor=AppTheme.SURFACE,
        padding=AppTheme.PADDING_MEDIUM,
        border_radius=AppTheme.RADIUS_MEDIUM,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color="#33333310"),
        expand=True,
    )


def create_action_button(text: str, on_click, icon: str = None):
    """Reusable primary action button"""
    # Build button content (text + optional icon)
    if icon:
        button_content = ft.Row(
            controls=[
                ft.Text("📤", size=20),  # Use emoji for icon
                ft.Text(text, size=16, weight=ft.FontWeight.BOLD, color="white"),
            ],
            spacing=8,
            tight=True,
        )
    else:
        button_content = ft.Text(
            text, size=16, weight=ft.FontWeight.BOLD, color="white"
        )

    return ft.ElevatedButton(
        content=button_content,  # ✅ FIXED: Use content instead of text
        on_click=on_click,
        style=ft.ButtonStyle(
            bgcolor=AppTheme.PRIMARY,
            padding=ft.padding.symmetric(horizontal=30, vertical=15),
            shape=ft.RoundedRectangleBorder(radius=AppTheme.RADIUS_SMALL),
        ),
    )


def create_info_card(title: str, message: str, card_type: str = "info"):
    """Reusable information card with icon and text"""
    # Use text emojis instead of Flet icons for compatibility
    icons_map = {
        "info": (AppTheme.INFO, "ℹ️"),
        "success": (AppTheme.SUCCESS, "✅"),
        "warning": (AppTheme.WARNING, "⚠️"),
        "error": (AppTheme.ERROR, "❌"),
    }

    color, emoji = icons_map.get(card_type, icons_map["info"])
    bg_color = f"{color}20"

    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Text(emoji, size=30),
                ft.Column(
                    controls=[
                        ft.Text(
                            title,
                            size=AppTheme.FONT_SIZE_MEDIUM,
                            weight=ft.FontWeight.BOLD,
                            color=color,
                        ),
                        ft.Text(
                            message,
                            size=AppTheme.FONT_SIZE_NORMAL,
                            color=AppTheme.TEXT_PRIMARY,
                        ),
                    ],
                    spacing=5,
                    expand=True,
                ),
            ],
            spacing=15,
        ),
        bgcolor=bg_color,
        padding=AppTheme.PADDING_MEDIUM,
        border_radius=AppTheme.RADIUS_MEDIUM,
        border=ft.border.all(2, color),
    )
