from enum import Enum

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