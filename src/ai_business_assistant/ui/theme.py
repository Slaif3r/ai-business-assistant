"""
UI Theme and Design System
Purpose: Consistent colors, typography, spacing across all screens
Author: [Your Name]
Date: Day 3
"""

import flet as ft


class AppTheme:
    """
    Design system for AI Business Assistant.
    Inspired by pitch deck purple gradient theme.
    """
    
    # Color Palette (matching pitch deck)
    PRIMARY = "#667eea"      # Purple
    SECONDARY = "#764ba2"    # Darker purple
    SUCCESS = "#28a745"      # Green
    WARNING = "#ffc107"      # Yellow
    ERROR = "#dc3545"        # Red
    INFO = "#17a2b8"         # Cyan
    
    BACKGROUND = "#f8f9fa"   # Light gray
    SURFACE = "#ffffff"      # White
    TEXT_PRIMARY = "#333333"
    TEXT_SECONDARY = "#666666"
    
    # Typography
    FONT_SIZE_LARGE = 32
    FONT_SIZE_MEDIUM = 20
    FONT_SIZE_NORMAL = 16
    FONT_SIZE_SMALL = 14
    
    # Spacing
    PADDING_SMALL = 10
    PADDING_MEDIUM = 20
    PADDING_LARGE = 40
    
    # Border Radius
    RADIUS_SMALL = 8
    RADIUS_MEDIUM = 12
    RADIUS_LARGE = 16
    
    @staticmethod
    def get_gradient():
        """Get brand gradient for headers"""
        return ft.LinearGradient(
            colors=[AppTheme.PRIMARY, AppTheme.SECONDARY]
        )
    
    @staticmethod
    def configure_page(page: ft.Page):
        """Configure page with consistent theme"""
        page.title = "AI Business Assistant"
        page.padding = 0
        page.bgcolor = AppTheme.BACKGROUND