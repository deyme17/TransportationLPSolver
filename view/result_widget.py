from typing import List
from PyQt6.QtWidgets import (
    QGroupBox, QVBoxLayout, QLabel,
    QScrollArea, QWidget, QGridLayout, QTextEdit
)
from PyQt6.QtCore import Qt
from utils import UIHelper, ResultWidgetConstants, ResultFormatter, TLPResult


class ResultSection(QGroupBox):
    """Widget for displaying Transportation LP optimization results"""
    def __init__(self) -> None:
        super().__init__("Results")
        self._init_ui()
    
    def _init_ui(self) -> None:
        """Initialize the results section UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # status section
        self.status_label = self._create_status_label()
        layout.addWidget(self.status_label)
        
        # optimal value section
        self.optimal_value_label = self._create_optimal_value_label()
        layout.addWidget(self.optimal_value_label)
        
        layout.addSpacing(10)
        
        # allocation matrix section
        layout.addWidget(self._create_section_label("Allocation Matrix (X):"))
        self.allocation_scroll = self._create_allocation_scroll()
        layout.addWidget(self.allocation_scroll)
        
        layout.addSpacing(10)
        
        # summary section
        layout.addWidget(self._create_section_label("Summary:"))
        self.summary_text = self._create_summary_text()
        layout.addWidget(self.summary_text)
        
        layout.addStretch()
    
    def _create_status_label(self) -> QLabel:
        """Create status label"""
        label = QLabel("No results yet")
        label.setStyleSheet(
            "font-size: 14pt; font-weight: bold; padding: 10px; "
            "background-color: #3a3a3a; border-radius: 5px;"
        )
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return label
    
    def _create_optimal_value_label(self) -> QLabel:
        """Create optimal value label"""
        label = QLabel("")
        label.setStyleSheet(
            "font-size: 13pt; padding: 8px; "
            "background-color: #2d2d2d; border-radius: 5px;"
        )
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return label
    
    @staticmethod
    def _create_section_label(text: str) -> QLabel:
        """Create section label"""
        return UIHelper.create_label(
            text,
            style="font-size: 11pt; font-weight: bold; color: #ffffff;"
        )
    
    def _create_allocation_scroll(self) -> QScrollArea:
        """Create scrollable allocation matrix area"""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setMinimumHeight(ResultWidgetConstants.MIN_MATRIX_HEIGHT)
        
        self.allocation_container = QWidget()
        self.allocation_layout = QVBoxLayout(self.allocation_container)
        self.allocation_layout.setSpacing(5)
        self.allocation_layout.setContentsMargins(5, 5, 5, 5)
        
        scroll.setWidget(self.allocation_container)
        return scroll
    
    def _create_summary_text(self) -> QTextEdit:
        """Create summary text area"""
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setMaximumHeight(ResultWidgetConstants.SUMMARY_HEIGHT)
        text_edit.setStyleSheet(
            "background-color: #2d2d2d; border: 1px solid #555555; "
            "border-radius: 5px; padding: 5px; font-family: monospace;"
        )
        return text_edit
    
    def display_results(self, result: TLPResult) -> None:
        """
        Display optimization results.
        
        Args:
            result: TLPResult object containing solution data
        """
        self._update_status(result)
        self._update_optimal_value(result)
        
        if result.is_optimal and result.solution is not None:
            self._display_allocation_matrix(result.solution)
            self._display_summary(result)
        else:
            self._clear_allocation_matrix()
            self._display_error_summary(result)
    
    def _update_status(self, result: TLPResult) -> None:
        """Update status label"""
        status_text, status_color = ResultFormatter.format_status(result.status)
        self.status_label.setText(f"Status: {status_text}")
        self.status_label.setStyleSheet(
            f"font-size: 14pt; font-weight: bold; padding: 10px; "
            f"background-color: {status_color}; border-radius: 5px; color: #ffffff;"
        )
    
    def _update_optimal_value(self, result: TLPResult) -> None:
        """Update optimal value label"""
        if result.optimal_value is not None:
            value_text = ResultFormatter.format_optimal_value(result.optimal_value)
            self.optimal_value_label.setText(value_text)
            self.optimal_value_label.show()
        else:
            self.optimal_value_label.hide()
    
    def _display_allocation_matrix(self, solution: List[List[float]]) -> None:
        """Display allocation matrix"""
        UIHelper.clear_layout(self.allocation_layout)
        if not solution: 
            return
        num_suppliers = len(solution)
        num_consumers = len(solution[0]) if solution else 0
        
        grid = QGridLayout()
        grid.setSpacing(3)
        
        # header (consumers)
        grid.addWidget(self._create_header_label(""), 0, 0)
        for j in range(num_consumers):
            header = self._create_header_label(f"B{j+1}")
            grid.addWidget(header, 0, j + 1)
        # supply column header
        grid.addWidget(self._create_header_label("Supply"), 0, num_consumers + 1)
        
        for i in range(num_suppliers):
            # row header (suppliers)
            row_header = self._create_header_label(f"A{i+1}")
            grid.addWidget(row_header, i + 1, 0)
            
            # allocation values
            row_sum = 0
            for j in range(num_consumers):
                value = solution[i][j]
                row_sum += value
                cell = self._create_cell_label(value)
                grid.addWidget(cell, i + 1, j + 1)
            
            # supply used
            sum_label = self._create_sum_label(row_sum)
            grid.addWidget(sum_label, i + 1, num_consumers + 1)
        
        # demand
        grid.addWidget(self._create_header_label("Demand"), num_suppliers + 1, 0)
        for j in range(num_consumers):
            col_sum = sum(solution[i][j] for i in range(num_suppliers))
            sum_label = self._create_sum_label(col_sum)
            grid.addWidget(sum_label, num_suppliers + 1, j + 1)
        
        grid_widget = QWidget()
        grid_widget.setLayout(grid)
        self.allocation_layout.addWidget(grid_widget)
        self.allocation_layout.addStretch()
    
    def _create_header_label(self, text: str) -> QLabel:
        """Create header label for matrix"""
        label = QLabel(text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet(
            "font-weight: bold; color: #ffffff; "
            "background-color: #404040; padding: 5px; "
            "border: 1px solid #555555; min-width: 60px;"
        )
        return label
    
    def _create_cell_label(self, value: float) -> QLabel:
        """Create cell label for allocation value"""
        text = ResultFormatter.format_allocation_value(value)
        label = QLabel(text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        if value > 1e-6:
            style = (
                "background-color: #2d5a2d; color: #ffffff; "
                "padding: 5px; border: 1px solid #555555; "
                "min-width: 60px; font-weight: bold;"
            )
        else:
            style = (
                "background-color: #2d2d2d; color: #888888; "
                "padding: 5px; border: 1px solid #555555; min-width: 60px;"
            )
        
        label.setStyleSheet(style)
        return label
    
    def _create_sum_label(self, value: float) -> QLabel:
        """Create sum label"""
        text = ResultFormatter.format_allocation_value(value)
        label = QLabel(text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet(
            "background-color: #3a4a5a; color: #ffffff; "
            "padding: 5px; border: 1px solid #555555; "
            "min-width: 60px; font-weight: bold;"
        )
        return label
    
    def _display_summary(self, result: TLPResult) -> None:
        """Display solution summary"""
        summary = ResultFormatter.format_summary(result)
        self.summary_text.setPlainText(summary)
    
    def _display_error_summary(self, result: TLPResult) -> None:
        """Display error summary"""
        if result.error_message:
            self.summary_text.setPlainText(f"Error: {result.error_message}")
        else:
            self.summary_text.setPlainText("No solution found.")
    
    def _clear_allocation_matrix(self) -> None:
        """Clear allocation matrix display"""
        UIHelper.clear_layout(self.allocation_layout)
    
    def clear(self) -> None:
        """Clear all results"""
        self.status_label.setText("No results yet")
        self.status_label.setStyleSheet(
            "font-size: 14pt; font-weight: bold; padding: 10px; "
            "background-color: #3a3a3a; border-radius: 5px;"
        )
        self.optimal_value_label.hide()
        self._clear_allocation_matrix()
        self.summary_text.clear()