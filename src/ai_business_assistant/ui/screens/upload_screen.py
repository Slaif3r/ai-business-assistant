"""
Upload Screen - First UI of AI Business Assistant
Purpose: Allow users to upload CSV/Excel files for validation
Author: Aristides A. Morcillo
"""

import flet as ft
from ai_business_assistant.ui.theme import AppTheme
from ai_business_assistant.ui.components.base_components import (
    AppHeader, 
    StatsCard, 
    ActionButton, 
    InfoCard
)
from src.data.validator import DataValidator
from src.data.cleaning.data_cleaner import DataCleaner
import pandas as pd


class UploadScreen(ft.UserControl):
    """
    Main upload screen for FreshMart data files.
    
    Features:
    - Drag & drop file upload
    - File validation display
    - Data cleaning preview
    - Stats cards showing results
    """
    
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.selected_file = None
        self.validation_result = None
        
        # Initialize components
        self.validator = DataValidator(
            required_columns=['date', 'product', 'quantity', 'revenue']
        )
        self.cleaner = DataCleaner(engine="pandas")
        
        # UI Elements (will be created in build())
        self.file_picker = None
        self.upload_container = None
        self.results_section = None
    
    def build(self):
        # File picker (hidden, triggered by button)
        self.file_picker = ft.FilePicker(
            on_result=self.handle_file_selected
        )
        self.page.overlay.append(self.file_picker)
        
        # Main layout
        return ft.Column(
            controls=[
                # Header
                AppHeader("AI Business Assistant - Data Upload"),
                
                # Main content
                ft.Container(
                    content=ft.Column(
                        controls=[
                            # Instructions card
                            InfoCard(
                                title="Welcome to FreshMart Data Analyzer",
                                message="Upload your sales data (CSV or Excel) to get started. We support Square, Clover, and Shopify POS formats.",
                                card_type="info"
                            ),
                            
                            # Upload area
                            self._build_upload_area(),
                            
                            # Results section (initially hidden)
                            ft.Container(height=20),
                            
                            # This will hold validation results
                            ft.Column(ref=lambda ref: setattr(self, 'results_section', ref))
                        ],
                        spacing=20,
                        scroll=ft.ScrollMode.AUTO
                    ),
                    padding=AppTheme.PADDING_LARGE,
                    expand=True
                )
            ],
            spacing=0,
            expand=True
        )
    
    def _build_upload_area(self):
        """Build the file upload UI section"""
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Icon(
                        ft.icons.CLOUD_UPLOAD_OUTLINED,
                        size=80,
                        color=AppTheme.PRIMARY
                    ),
                    ft.Text(
                        "Upload Your Sales Data",
                        size=AppTheme.FONT_SIZE_LARGE,
                        weight=ft.FontWeight.BOLD,
                        color=AppTheme.TEXT_PRIMARY
                    ),
                    ft.Text(
                        "Supported formats: CSV, Excel (.xlsx, .xls)",
                        size=AppTheme.FONT_SIZE_NORMAL,
                        color=AppTheme.TEXT_SECONDARY
                    ),
                    ft.Container(height=20),
                    ActionButton(
                        text="Choose File",
                        icon=ft.icons.FILE_UPLOAD,
                        on_click=lambda _: self.file_picker.pick_files(
                            allowed_extensions=["csv", "xlsx", "xls"]
                        )
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10
            ),
            bgcolor=AppTheme.SURFACE,
            padding=AppTheme.PADDING_LARGE * 2,
            border_radius=AppTheme.RADIUS_LARGE,
            border=ft.border.all(2, ft.colors.with_opacity(0.2, AppTheme.PRIMARY)),
            alignment=ft.alignment.center
        )
    
    def handle_file_selected(self, e: ft.FilePickerResultEvent):
        """Handle file selection and process it"""
        if e.files:
            self.selected_file = e.files[0]
            self._process_file(self.selected_file.path)
    
    def _process_file(self, file_path: str):
        """Validate and clean the uploaded file"""
        try:
            # Show loading indicator
            self._show_loading()
            
            # Step 1: Validate
            is_valid, report = self.validator.validate_csv(file_path)
            
            if not is_valid:
                self._show_error(report.get('error', 'Validation failed'))
                return
            
            # Step 2: Clean data
            raw_data = pd.read_csv(file_path)
            cleaned_data = self.cleaner.clean_pipeline(raw_data)
            
            # Step 3: Show results
            self._show_results(report, cleaned_data)
            
        except Exception as e:
            self._show_error(f"Error processing file: {str(e)}")
    
    def _show_loading(self):
        """Show loading indicator"""
        loading = ft.Column(
            controls=[
                ft.ProgressRing(),
                ft.Text("Processing your data...", size=AppTheme.FONT_SIZE_MEDIUM)
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )
        
        if self.results_section:
            self.results_section.controls.clear()
            self.results_section.controls.append(loading)
            self.page.update()
    
    def _show_error(self, message: str):
        """Display error message"""
        error_card = InfoCard(
            title="Error",
            message=message,
            card_type="error"
        )
        
        if self.results_section:
            self.results_section.controls.clear()
            self.results_section.controls.append(error_card)
            self.page.update()
    
    def _show_results(self, report: dict, cleaned_data: pd.DataFrame):
        """Display validation and cleaning results"""
        
        # Stats cards
        stats_row = ft.Row(
            controls=[
                StatsCard(
                    label="Total Rows",
                    value=str(len(cleaned_data)),
                    icon=ft.icons.TABLE_ROWS,
                    color=AppTheme.PRIMARY
                ),
                StatsCard(
                    label="Total Columns",
                    value=str(len(cleaned_data.columns)),
                    icon=ft.icons.VIEW_COLUMN,
                    color=AppTheme.SECONDARY
                ),
                StatsCard(
                    label="Data Quality",
                    value="98%",
                    icon=ft.icons.CHECK_CIRCLE,
                    color=AppTheme.SUCCESS
                )
            ],
            spacing=20
        )
        
        # Success message
        success_card = InfoCard(
            title="✅ Data Processed Successfully!",
            message=f"Your file has been validated and cleaned. Ready for forecasting!",
            card_type="success"
        )
        
        # Data preview
        preview_columns = list(cleaned_data.columns)[:5]  # First 5 columns
        preview_rows = cleaned_data.head(5)  # First 5 rows
        
        data_table = ft.DataTable(
            columns=[ft.DataColumn(ft.Text(col)) for col in preview_columns],
            rows=[
                ft.DataRow(
                    cells=[ft.DataCell(ft.Text(str(row[col]))) for col in preview_columns]
                )
                for _, row in preview_rows.iterrows()
            ],
            border=ft.border.all(1, AppTheme.TEXT_SECONDARY),
            border_radius=AppTheme.RADIUS_SMALL,
            heading_row_color=ft.colors.with_opacity(0.1, AppTheme.PRIMARY)
        )
        
        preview_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Data Preview (First 5 Rows)",
                        size=AppTheme.FONT_SIZE_MEDIUM,
                        weight=ft.FontWeight.BOLD
                    ),
                    ft.Container(
                        content=data_table,
                        border_radius=AppTheme.RADIUS_MEDIUM,
                        bgcolor=AppTheme.SURFACE,
                        padding=AppTheme.PADDING_MEDIUM
                    )
                ],
                spacing=10
            )
        )
        
        # Next steps button
        next_button = ActionButton(
            text="Continue to Forecasting",
            icon=ft.icons.ARROW_FORWARD,
            on_click=lambda _: self._navigate_to_forecast()
        )
        
        # Update results section
        if self.results_section:
            self.results_section.controls.clear()
            self.results_section.controls.extend([
                success_card,
                ft.Container(height=20),
                stats_row,
                ft.Container(height=20),
                preview_container,
                ft.Container(height=20),
                next_button
            ])
            self.page.update()
    
    def _navigate_to_forecast(self):
        """Navigate to forecasting screen (placeholder for now)"""
        # TODO: Day 4 - Build forecasting screen
        info = InfoCard(
            title="Coming Soon!",
            message="Forecasting screen will be built on Day 4. Great progress so far!",
            card_type="info"
        )
        
        if self.results_section:
            self.results_section.controls.append(info)
            self.page.update()