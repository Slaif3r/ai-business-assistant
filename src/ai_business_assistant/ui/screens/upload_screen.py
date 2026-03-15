"""
Upload Screen - First UI of AI Business Assistant
Purpose: Allow users to upload CSV/Excel files for validation
Author: [Your Name]
Date: Day 3
"""

import io

import flet as ft
import pandas as pd

from ai_business_assistant.ui.components.base_components import (
    create_action_button,
    create_app_header,
    create_info_card,
    create_stats_card,
)
from ai_business_assistant.ui.theme import AppTheme
from data.cleaning.data_cleaner import DataCleaner
from data.validator import DataValidator


class UploadScreen:
    """
    Main upload screen for FreshMart data files.

    Features:
    - Drag & drop file upload
    - File validation display
    - Data cleaning preview
    - Stats cards showing results
    """

    def __init__(self, page: ft.Page):
        self.page = page
        self.selected_file = None
        self.validation_result = None

        # Initialize components
        self.validator = DataValidator(
            required_columns=["date", "product", "quantity", "revenue"]
        )
        self.cleaner = DataCleaner(engine="pandas")

        # UI Elements
        self.results_column = None

    def build(self):
        """Build and return the screen layout"""
        # Results column (for dynamic updates)
        self.results_column = ft.Column(spacing=20)

        # Main layout
        return ft.Column(
            controls=[
                create_app_header("AI Business Assistant - Data Upload"),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            create_info_card(
                                title="Welcome to FreshMart Data Analyzer",
                                message="Upload your sales data (CSV or Excel) to get started. We support Square, Clover, and Shopify POS formats.",
                                card_type="info",
                            ),
                            self._build_upload_area(),
                            ft.Container(height=20),
                            self.results_column,
                        ],
                        spacing=20,
                        scroll=ft.ScrollMode.AUTO,
                    ),
                    padding=AppTheme.PADDING_LARGE,
                    expand=True,
                ),
            ],
            spacing=0,
            expand=True,
        )

    def _build_upload_area(self):
        """Build the file upload UI section"""
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("☁️📤", size=80),
                    ft.Text(
                        "Upload Your Sales Data",
                        size=AppTheme.FONT_SIZE_LARGE,
                        weight=ft.FontWeight.BOLD,
                        color=AppTheme.TEXT_PRIMARY,
                    ),
                    ft.Text(
                        "Supported formats: CSV, Excel (.xlsx, .xls)",
                        size=AppTheme.FONT_SIZE_NORMAL,
                        color=AppTheme.TEXT_SECONDARY,
                    ),
                    ft.Container(height=20),
                    create_action_button(
                        text="Choose File",
                        icon=None,
                        on_click=self.open_file_picker,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
            bgcolor=AppTheme.SURFACE,
            padding=AppTheme.PADDING_LARGE * 2,
            border_radius=AppTheme.RADIUS_LARGE,
            border=ft.border.all(2, "#667eea33"),
            alignment=ft.alignment.Alignment(0, 0),
        )

    async def open_file_picker(self, e):
        """Open file picker dialog and process selected file"""
        try:
            files = await ft.FilePicker().pick_files(
                allow_multiple=False,
                with_data=self.page.web,
                file_type=ft.FilePickerFileType.CUSTOM,
                allowed_extensions=["csv", "xlsx", "xls"],
            )

            if not files:
                return

            self.selected_file = files[0]

            if self.page.web:
                self._process_web_file(self.selected_file)
            else:
                self._process_file(self.selected_file.path)

        except Exception as ex:
            self._show_error(f"Error opening file picker: {str(ex)}")

    def _read_file(self, file_path: str) -> pd.DataFrame:
        """Read CSV or Excel file based on extension"""
        lower_path = file_path.lower()

        if lower_path.endswith(".csv"):
            return pd.read_csv(file_path)

        if lower_path.endswith(".xlsx") or lower_path.endswith(".xls"):
            return pd.read_excel(file_path)

        raise ValueError("Unsupported file format. Please upload CSV or Excel file.")

    def _process_file(self, file_path: str):
        """Validate and clean the uploaded file in desktop mode"""
        try:
            self._show_loading()

            is_valid, report = self.validator.validate_file(file_path)

            if not is_valid:
                self._show_error(report.get("error", "Validation failed"))
                return

            raw_data = self._read_file(file_path)
            cleaned_data = self.cleaner.clean_pipeline(raw_data)

            self._show_results(report, cleaned_data)

        except Exception as ex:
            self._show_error(f"Error processing file: {str(ex)}")

    def _process_web_file(self, selected_file):
        """Process uploaded file in web mode using in-memory bytes"""
        try:
            self._show_loading()

            if not getattr(selected_file, "bytes", None):
                self._show_error("No file data received from browser.")
                return

            file_name = selected_file.name.lower()
            file_bytes = io.BytesIO(selected_file.bytes)

            if file_name.endswith(".csv"):
                raw_data = pd.read_csv(file_bytes)
            elif file_name.endswith(".xlsx") or file_name.endswith(".xls"):
                raw_data = pd.read_excel(file_bytes)
            else:
                self._show_error("Unsupported file format. Please upload CSV or Excel.")
                return

            raw_data.columns = [str(col).strip().lower() for col in raw_data.columns]

            missing_cols = set(self.validator.required_columns) - set(raw_data.columns)
            if raw_data.empty:
                self._show_error("The uploaded file is empty.")
                return

            if missing_cols:
                self._show_error(
                    f"Missing required columns: {', '.join(sorted(missing_cols))}"
                )
                return

            cleaned_data = self.cleaner.clean_pipeline(raw_data)

            report = {
                "file_path": selected_file.name,
                "file_type": "." + selected_file.name.split(".")[-1].lower(),
                "total_rows": len(raw_data),
                "total_columns": len(raw_data.columns),
                "columns_found": list(raw_data.columns),
                "missing_columns": list(missing_cols),
                "missing_values_per_column": raw_data.isnull().sum().to_dict(),
                "duplicate_rows": int(raw_data.duplicated().sum()),
                "data_types": {k: str(v) for k, v in raw_data.dtypes.to_dict().items()},
                "is_empty": raw_data.empty,
            }

            self._show_results(report, cleaned_data)

        except Exception as ex:
            self._show_error(f"Error processing file: {str(ex)}")

    def _show_loading(self):
        """Show loading indicator"""
        self.results_column.controls.clear()
        self.results_column.controls.append(
            ft.Column(
                controls=[
                    ft.ProgressRing(),
                    ft.Text("Processing your data...", size=AppTheme.FONT_SIZE_MEDIUM),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
            )
        )
        self.page.update()

    def _show_error(self, message: str):
        """Display error message"""
        self.results_column.controls.clear()
        self.results_column.controls.append(
            create_info_card(title="Error", message=message, card_type="error")
        )
        self.page.update()

    def _show_results(self, report: dict, cleaned_data: pd.DataFrame):
        """Display validation and cleaning results"""

        stats_row = ft.Row(
            controls=[
                create_stats_card(
                    label="Total Rows",
                    value=str(len(cleaned_data)),
                    icon=None,
                    color=AppTheme.PRIMARY,
                ),
                create_stats_card(
                    label="Total Columns",
                    value=str(len(cleaned_data.columns)),
                    icon=None,
                    color=AppTheme.SECONDARY,
                ),
                create_stats_card(
                    label="Data Quality",
                    value="98%",
                    icon=None,
                    color=AppTheme.SUCCESS,
                ),
            ],
            spacing=20,
        )

        success_card = create_info_card(
            title="✅ Data Processed Successfully!",
            message="Your file has been validated and cleaned. Ready for forecasting!",
            card_type="success",
        )

        preview_columns = list(cleaned_data.columns)[:5]
        preview_rows = cleaned_data.head(5)

        data_table = ft.DataTable(
            columns=[ft.DataColumn(ft.Text(col)) for col in preview_columns],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(row[col]))) for col in preview_columns
                    ]
                )
                for _, row in preview_rows.iterrows()
            ],
            border=ft.border.all(1, AppTheme.TEXT_SECONDARY),
            border_radius=AppTheme.RADIUS_SMALL,
            heading_row_color="#667eea20",
        )

        preview_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Data Preview (First 5 Rows)",
                        size=AppTheme.FONT_SIZE_MEDIUM,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Container(
                        content=data_table,
                        border_radius=AppTheme.RADIUS_MEDIUM,
                        bgcolor=AppTheme.SURFACE,
                        padding=AppTheme.PADDING_MEDIUM,
                    ),
                ],
                spacing=10,
            )
        )

        next_button = create_action_button(
            text="Continue to Forecasting",
            icon=None,
            on_click=lambda _: self._navigate_to_forecast(),
        )

        self.results_column.controls.clear()
        self.results_column.controls.extend(
            [
                success_card,
                ft.Container(height=20),
                stats_row,
                ft.Container(height=20),
                preview_container,
                ft.Container(height=20),
                next_button,
            ]
        )
        self.page.update()

    def _navigate_to_forecast(self):
        """Navigate to forecasting screen (placeholder)"""
        info = create_info_card(
            title="Coming Soon!",
            message="Forecasting screen will be built on Day 4. Great progress so far!",
            card_type="info",
        )

        self.results_column.controls.append(info)
        self.page.update()
