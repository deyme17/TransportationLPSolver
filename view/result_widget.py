from typing import List, Optional
from PyQt6.QtWidgets import (
    QGroupBox, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
)

class ResultSection(QGroupBox):
    """Widget for displaying optimization results and transportation matrix"""
    def __init__(self) -> None:
        super().__init__("Results")