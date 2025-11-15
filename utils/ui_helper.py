from typing import Optional
from PyQt6.QtWidgets import QLabel, QLineEdit, QSpinBox, QLayout


class UIHelper:
    """Helper methods for UI operations"""
    @staticmethod
    def clear_layout(layout: QLayout) -> None:
        """Clear all widgets from layout"""
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
    
    @staticmethod
    def create_numeric_input(placeholder: str = "0", max_width: int = 70) -> QLineEdit:
        """Factory method for numeric input fields"""
        line_edit = QLineEdit()
        line_edit.setPlaceholderText(placeholder)
        line_edit.setMaximumWidth(max_width)
        return line_edit
    
    @staticmethod
    def create_label(text: str, max_width: Optional[int] = None, 
                    style: Optional[str] = None) -> QLabel:
        """Factory method for labels"""
        label = QLabel(text)
        if max_width:
            label.setMaximumWidth(max_width)
        if style:
            label.setStyleSheet(style)
        return label
    
    @staticmethod
    def create_spinbox(min_val: int, max_val: int, default: int, 
                      max_width: int = 100) -> QSpinBox:
        """Factory method for spinboxes"""
        spinbox = QSpinBox()
        spinbox.setMinimum(min_val)
        spinbox.setMaximum(max_val)
        spinbox.setValue(default)
        spinbox.setMaximumWidth(max_width)
        return spinbox