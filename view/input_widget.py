from typing import List, Tuple
from PyQt6.QtWidgets import (
    QGroupBox, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, 
    QPushButton, QScrollArea, QWidget, QGridLayout
)
from utils import (
    UIHelper, InputWidgetConstants, InputValidator,
    TLPProblem
)


class InputSection(QGroupBox):
    """Widget for Transportation LP problem input and configuration"""
    def __init__(self) -> None:
        super().__init__("Problem Configuration")
        self.supply_inputs: List[QLineEdit] = []
        self.demand_inputs: List[QLineEdit] = []
        self.cost_inputs: List[List[QLineEdit]] = []
        self._init_widgets()
        self._init_ui()
    
    def _init_widgets(self) -> None:
        """Initialize widgets"""
        self.supply_count = UIHelper.create_spinbox(
            1, InputWidgetConstants.MAX_SUPPLIERS, 
            InputWidgetConstants.DEFAULT_SUPPLIERS, 
            InputWidgetConstants.SPINBOX_WIDTH
        )
        self.demand_count = UIHelper.create_spinbox(
            1, InputWidgetConstants.MAX_CONSUMERS, 
            InputWidgetConstants.DEFAULT_CONSUMERS, 
            InputWidgetConstants.SPINBOX_WIDTH
        )
        self.generate_btn = QPushButton("Create Form")
    
    def _init_ui(self) -> None:
        """Initialize the input section UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # config
        config_layout = self._create_config_layout()
        layout.addLayout(config_layout)
        
        self.generate_btn.clicked.connect(self.update)
        layout.addWidget(self.generate_btn)
        
        layout.addSpacing(15)
        
        # supply section
        layout.addWidget(self._create_section_label("Supply (A):", "Available resources at suppliers"))
        
        supply_container = QWidget()
        supply_container.setMaximumWidth(InputWidgetConstants.MAX_SECTION_WIDTH)
        self.supply_layout = QHBoxLayout(supply_container)
        self.supply_layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(supply_container)
        
        layout.addSpacing(15)
        
        # demand section
        layout.addWidget(self._create_section_label("Demand (B):", "Required resources at consumers"))
        
        demand_container = QWidget()
        demand_container.setMaximumWidth(InputWidgetConstants.MAX_SECTION_WIDTH)
        self.demand_layout = QHBoxLayout(demand_container)
        self.demand_layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(demand_container)
        
        layout.addSpacing(15)
        
        # cost matrix section
        layout.addWidget(self._create_section_label("Cost Matrix (C):", "Transportation costs from supplier i to consumer j"))
        self.cost_scroll = self._create_cost_scroll()
        layout.addWidget(self.cost_scroll)
    
    def _create_config_layout(self) -> QHBoxLayout:
        """Create configuration panel layout"""
        config_layout = QHBoxLayout()
        config_layout.setSpacing(30)
        
        # suppliers
        config_layout.addWidget(QLabel("Suppliers (m):"))
        config_layout.addWidget(self.supply_count)
        
        # consumers
        config_layout.addWidget(QLabel("Consumers (n):"))
        config_layout.addWidget(self.demand_count)
        
        config_layout.addStretch()
        return config_layout
    
    @staticmethod
    def _create_section_label(title: str, description: str) -> QLabel:
        """Create section label with description"""
        return UIHelper.create_label(
            f"{title} {description}",
            style="color: #aaaaaa; font-style: italic;"
        )
    
    def _create_cost_scroll(self) -> QScrollArea:
        """Create scrollable cost matrix area"""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        self.cost_container = QWidget()
        self.cost_layout = QVBoxLayout(self.cost_container)
        self.cost_layout.setSpacing(5)
        self.cost_layout.setContentsMargins(5, 5, 5, 5)
        
        scroll.setWidget(self.cost_container)
        return scroll
    
    def update(self) -> None:
        """Update input form based on selected parameters"""
        supply_count = self.supply_count.value()
        demand_count = self.demand_count.value()
        
        self._update_supply_inputs(supply_count)
        self._update_demand_inputs(demand_count)
        self._update_cost_matrix(supply_count, demand_count)
    
    def _update_supply_inputs(self, count: int) -> None:
        """Update supply inputs"""
        UIHelper.clear_layout(self.supply_layout)
        self.supply_inputs.clear()
        
        for i in range(count):
            label, line_edit = self._create_value_input(f"A{i+1}:")
            self.supply_inputs.append(line_edit)
            self.supply_layout.addWidget(label)
            self.supply_layout.addWidget(line_edit)
        
        self.supply_layout.addStretch()
    
    def _update_demand_inputs(self, count: int) -> None:
        """Update demand inputs"""
        UIHelper.clear_layout(self.demand_layout)
        self.demand_inputs.clear()
        
        for i in range(count):
            label, line_edit = self._create_value_input(f"B{i+1}:")
            self.demand_inputs.append(line_edit)
            self.demand_layout.addWidget(label)
            self.demand_layout.addWidget(line_edit)
        
        self.demand_layout.addStretch()
    
    def _create_value_input(self, label_text: str) -> Tuple[QLabel, QLineEdit]:
        """Factory method for creating value inputs"""
        label = UIHelper.create_label(label_text, InputWidgetConstants.LABEL_WIDTH)
        line_edit = UIHelper.create_numeric_input("0", InputWidgetConstants.VALUE_INPUT_WIDTH)
        return label, line_edit
    
    def _update_cost_matrix(self, supply_count: int, demand_count: int) -> None:
        """Update cost matrix grid"""
        UIHelper.clear_layout(self.cost_layout)
        self.cost_inputs.clear()
        grid = QGridLayout()
        grid.setSpacing(5)
        
        # header row (consumers)
        grid.addWidget(QLabel(""), 0, 0)  # corner
        for j in range(demand_count):
            header = UIHelper.create_label(f"B{j+1}", InputWidgetConstants.MATRIX_HEADER_WIDTH)
            header.setStyleSheet("font-weight: bold; color: #ffffff;")
            grid.addWidget(header, 0, j + 1)
        
        # data rows
        for i in range(supply_count):
            # suppliers
            row_header = UIHelper.create_label(f"A{i+1}", InputWidgetConstants.MATRIX_HEADER_WIDTH)
            row_header.setStyleSheet("font-weight: bold; color: #ffffff;")
            grid.addWidget(row_header, i + 1, 0)
            
            # cost
            row_inputs = []
            for j in range(demand_count):
                cost_input = UIHelper.create_numeric_input("0", InputWidgetConstants.COST_INPUT_WIDTH)
                row_inputs.append(cost_input)
                grid.addWidget(cost_input, i + 1, j + 1)
            
            self.cost_inputs.append(row_inputs)

        grid_widget = QWidget()
        grid_widget.setLayout(grid)
        self.cost_layout.addWidget(grid_widget)
        self.cost_layout.addStretch()
    
    def get_data(self) -> Tuple[TLPProblem, bool, str]:
        """
        Extract and validate input data.
        Returns:
            TLPProblem: Dataclass containing:
                - supply (List[float]): Supply values at each supplier
                - demand (List[float]): Demand values at each consumer
                - costs (List[List[float]]): Cost matrix (m x n)
            bool: True if extraction and validation succeeded, otherwise False
            str: Error message if validation failed, empty string otherwise
        """
        try:
            supply = InputValidator.validate_coefficients(
                self.supply_inputs,
                name="Supply"
            )
            demand = InputValidator.validate_coefficients(
                self.demand_inputs,
                name="Demand"
            )
            costs = self._parse_cost_matrix()
            return TLPProblem(
                supply=supply,
                demand=demand,
                costs=costs
            ), True, ""
        except ValueError as e:
            return None, False, str(e)
    
    def _parse_cost_matrix(self) -> List[List[float]]:
        """Parse and validate cost matrix"""
        costs = []
        for i, row in enumerate(self.cost_inputs):
            try:
                row_costs = InputValidator.validate_coefficients(
                    row,
                    name=f"Cost matrix row {i+1}"
                )
                costs.append(row_costs)
            except ValueError as e:
                raise ValueError(f"Cost matrix row {i+1}: {str(e)}")
        return costs
    
    def clear(self) -> None:
        """Clear all input fields"""
        for line_edit in self.supply_inputs:
            line_edit.clear()
        
        for line_edit in self.demand_inputs:
            line_edit.clear()
        
        for row in self.cost_inputs:
            for line_edit in row:
                line_edit.clear()