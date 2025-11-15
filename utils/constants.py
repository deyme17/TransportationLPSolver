from enum import Enum

class SolutionStatus(Enum):
    OPTIMAL = 'optimal'
    INFEASIBLE = 'infeasible'
    UNBOUNDED = 'unbounded'
    ERROR = 'error'
    UNKNOWN = 'unknown'
    PENDING = 'pending'

class StatusColor(Enum):
    OPTIMAL = '#4CAF50'
    INFEASIBLE = '#f44336'
    UNBOUNDED = '#FF9800'
    ERROR = '#f44336'
    UNKNOWN = '#aaaaaa'
    PENDING = '#aaaaaa'
    
    @staticmethod
    def get_color(status: SolutionStatus) -> str:
        """Get color for given status"""
        return StatusColor[status.name].value

class StatusFormatter:
    """Status formatting utilities"""
    STATUS_LABELS = {
        SolutionStatus.OPTIMAL: "Optimal Solution Found",
        SolutionStatus.INFEASIBLE: "Problem is Infeasible",
        SolutionStatus.UNBOUNDED: "Problem is Unbounded",
        SolutionStatus.ERROR: "Solver Error",
        SolutionStatus.UNKNOWN: "Unknown Status",
        SolutionStatus.PENDING: "Solving...",
    }

# app
class AppConstants:
    WINDOW_TITLE = "Transportation Linear Programming Solver"
    WINDOW_SIZE = (900, 700)
    TITLE_FONT_SIZE = 16
    BUTTON_HEIGHT = 40
    BUTTON_FONT_SIZE = 12
    LAYOUT_SPACING = 15
    LAYOUT_MARGINS = 15

# input widget
class InputWidgetConstants:
    # spinbox settings
    MAX_SUPPLIERS = 20
    MAX_CONSUMERS = 20
    DEFAULT_SUPPLIERS = 3
    DEFAULT_CONSUMERS = 4
    SPINBOX_WIDTH = 100
    
    # layout widths
    MAX_SECTION_WIDTH = 800
    LABEL_WIDTH = 40
    VALUE_INPUT_WIDTH = 80
    COST_INPUT_WIDTH = 70
    MATRIX_HEADER_WIDTH = 50

# result widget
class ResultWidgetConstants:
    MIN_MATRIX_HEIGHT = 300
    SUMMARY_HEIGHT = 200