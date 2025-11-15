from typing import List, Tuple
from utils import TLPResult, SolutionStatus, StatusColor, StatusFormatter


class ResultFormatter:
    """Formats Transportation LP optimization results for display"""
    
    @staticmethod
    def format_status(status: str) -> Tuple[str, str]:
        """
        Format status text and return corresponding color.
        Args:
            status: Status string from solver (will be converted to SolutionStatus)
        Returns:
            Tuple of (formatted_status, color_hex)
        """
        try:
            status_enum = SolutionStatus(status.lower())
            return StatusFormatter.format_status(status_enum)
        except (ValueError, AttributeError):
            return status.capitalize(), StatusColor.UNKNOWN.value
    
    @staticmethod
    def format_optimal_value(value: float) -> str:
        """
        Format optimal value for display.
        Args:
            value: Optimal objective value
            
        Returns:
            Formatted string
        """
        return f"Total Transportation Cost: {value:.2f}"
    
    @staticmethod
    def format_allocation_value(value: float) -> str:
        """
        Format allocation value for display.
        Args:
            value: Allocation amount
            
        Returns:
            Formatted string
        """
        if abs(value) < 1e-6:
            return "—"
        return f"{value:.2f}"
    
    @staticmethod
    def format_summary(result: TLPResult) -> str:
        """
        Format complete solution summary.
        Args:
            result: TLPResult object
            
        Returns:
            Formatted summary string
        """
        if not result.is_optimal or result.solution is None:
            return "No optimal solution available."
        
        lines = []
        lines.append("=" * 60)
        lines.append("TRANSPORTATION SOLUTION SUMMARY")
        lines.append("=" * 60)
        lines.append("")
        
        # optimal cost
        lines.append(f"Total Transportation Cost: {result.optimal_value:.2f}")
        lines.append("")
        
        # allocation details
        lines.append("Transportation Routes (non-zero allocations):")
        lines.append("-" * 60)
        
        solution = result.solution
        num_suppliers = len(solution)
        num_consumers = len(solution[0]) if solution else 0
        
        route_count = 0
        for i in range(num_suppliers):
            for j in range(num_consumers):
                amount = solution[i][j]
                if amount > 1e-6:
                    route_count += 1
                    lines.append(f"  A{i+1} → B{j+1}: {amount:.2f} units")
        
        if route_count == 0:
            lines.append("  No active routes")
        
        lines.append("")
        lines.append(f"Total active routes: {route_count}")
        lines.append("=" * 60)
        
        return "\n".join(lines)
    
    @staticmethod
    def format_matrix_to_text(matrix: List[List[float]], 
                             row_labels: List[str] = None,
                             col_labels: List[str] = None) -> str:
        """
        Format matrix as text table.
        Args:
            matrix: 2D matrix to format
            row_labels: Optional row labels
            col_labels: Optional column labels
        Returns:
            Formatted text table
        """
        if not matrix:
            return "Empty matrix"
        
        rows = len(matrix)
        cols = len(matrix[0]) if matrix else 0
        
        # default labels
        if row_labels is None:
            row_labels = [f"Row {i+1}" for i in range(rows)]
        if col_labels is None:
            col_labels = [f"Col {j+1}" for j in range(cols)]
        
        # calc width
        col_widths = [max(len(label), 8) for label in col_labels]
        row_label_width = max(len(label) for label in row_labels)
        
        lines = []
        
        # header row
        header = " " * (row_label_width + 2)
        header += " | ".join(f"{label:>{w}}" for label, w in zip(col_labels, col_widths))
        lines.append(header)
        lines.append("-" * len(header))
        
        # data rows
        for i, row in enumerate(matrix):
            row_str = f"{row_labels[i]:<{row_label_width}} |"
            for j, value in enumerate(row):
                formatted = ResultFormatter.format_allocation_value(value)
                row_str += f" {formatted:>{col_widths[j]}} |"
            lines.append(row_str)
        
        return "\n".join(lines)