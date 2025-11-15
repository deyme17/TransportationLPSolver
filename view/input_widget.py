from typing import List, Optional, Tuple
from PyQt6.QtWidgets import (
    QGroupBox, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, 
    QComboBox, QPushButton, QScrollArea, QWidget
)


class InputSection(QGroupBox):
    """Widget for problem input and configuration"""
    def __init__(self) -> None:
        super().__init__("Problem Configuration")