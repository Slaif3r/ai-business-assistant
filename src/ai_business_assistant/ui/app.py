"""
AI Business Assistant - Main UI Application
Flet-based cross-platform interface
Author: [Your Name]
Date: Day 3
"""

import flet as ft
from ai_business_assistant.ui.theme import AppTheme
from ai_business_assistant.ui.screens.upload_screen import UploadScreen


def run():
    """
    Main application entry point.
    Called from src/main.py
    """
    def main(page: ft.Page):
        # Configure page with theme
        AppTheme.configure_page(page)
        
        # Set window properties
        page.window_width = 1200
        page.window_height = 800
        page.window_resizable = True
        page.window_min_width = 800
        page.window_min_height = 600
        
        # Create upload screen
        upload_screen = UploadScreen(page)
        
        # Add the UI controls to page
        page.add(upload_screen.build())
        
        # Update page
        page.update()
    
    # ✅ BEST: Run as native desktop app (no port conflicts!)
    ft.app(target=main)


if __name__ == "__main__":
    # Allow running directly for testing
    run()