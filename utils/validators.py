from typing import List
from PyQt6.QtWidgets import QLineEdit

class InputValidator:
    """Validates user input data"""
    @staticmethod
    def validate_coefficients(inputs: List[QLineEdit], 
                            name: str = "Value",
                            prefix: str = "") -> List[float]:
        """
        Validate and extract coefficients from input fields.
        Args:
            inputs: List of QLineEdit widgets
            name: Name for error messages
            prefix: Prefix for variable names in error messages
        Returns:
            List of validated float values
        Raises:
            ValueError: If any input is invalid
        """
        coefficients = []
        for i, line_edit in enumerate(inputs):
            text = line_edit.text().strip()
            var_name = f"{prefix}{i+1}" if prefix else f"{name} {i+1}"
            value = InputValidator.validate_coefficient(text, var_name)
            coefficients.append(value)
        return coefficients
    
    @staticmethod
    def validate_coefficient(text: str, var_name: str) -> float:
        """
        Validate a single coefficient value.
        Args:
            text: Input text to validate
            var_name: Variable name for error messages
        Returns:
            Validated float value
        Raises:
            ValueError: If input is invalid
        """
        if not text:
            raise ValueError(f"{var_name}: Value cannot be empty")
        try:
            value = float(text)
        except ValueError:
            raise ValueError(f"{var_name}: Invalid number format '{text}'")
        return value
    
    @staticmethod
    def validate_non_negative(value: float, var_name: str) -> float:
        """
        Validate that value is non-negative.
        Args:
            value: Value to validate
            var_name: Variable name for error messages
        Returns:
            Validated value
        Raises:
            ValueError: If value is negative
        """
        if value < 0:
            raise ValueError(f"{var_name}: Value must be non-negative (got {value})")
        return value
    
    @staticmethod
    def validate_positive(value: float, var_name: str) -> float:
        """
        Validate that value is positive.
        Args:
            value: Value to validate
            var_name: Variable name for error messages
        Returns:
            Validated value
        Raises:
            ValueError: If value is not positive
        """
        if value <= 0:
            raise ValueError(f"{var_name}: Value must be positive (got {value})")
        return value