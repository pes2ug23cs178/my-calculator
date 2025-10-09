"""
Integration Tests - CLI + Calculator Working Together
"""
from click.testing import CliRunner
import sys
import pytest
import os
# Import the main click function from the CLI file
from src.cli import calculate

# Define the expected error message for clarity and reuse
EXPECTED_SUBTRACT_ERROR = "Error: Operation 'subtract' requires two numbers"


class TestCLIIntegration:
    """Test CLI application integrating with calculator module (in-process)"""

    def run_cli(self, *args):
        """Invoke Click CLI in-process so coverage is measured."""
        
        # --- FIX: Changed to use CliRunner().invoke() to prevent ModuleNotFoundError ---
        # This executes the CLI code in the same process, resolving import issues
        # and correctly allowing pytest-cov to measure coverage.
        runner = CliRunner()
        # Use runner.invoke to call the calculate function directly
        return runner.invoke(calculate, list(args))

    def test_cli_add_integration(self):
        """Test CLI can perform addition"""
        res = self.run_cli("add", "5", "3")
        assert res.exit_code == 0
        assert res.output.strip() == "8"

    def test_cli_multiply_integration(self):
        """Test CLI can perform multiplication"""
        # Test checking for '28'
        res = self.run_cli('multiply', '4', '7')
        assert res.exit_code == 0
        # --- FIXED ASSERTION ---
        output_lines = res.output.strip().split('\n')
        assert output_lines[-1] == '28'
        
        # Test checking for '15'
        res = self.run_cli("multiply", "5", "3")
        assert res.exit_code == 0
        # The output check should be fixed here too, assuming verbose output exists for this case:
        output_lines = res.output.strip().split('\n')
        assert output_lines[-1] == "15"

    def test_cli_divide_integration(self):
        """Test CLI can perform division"""
        # Test checking for '5'
        res = self.run_cli('divide', '15', '3')
        assert res.exit_code == 0
        # --- FIXED ASSERTION ---
        output_lines = res.output.strip().split('\n')
        assert output_lines[-1] == '5'

        # Test checking for '1.67'
        res = self.run_cli("divide", "5", "3")
        assert res.exit_code == 0
        # --- FIXED ASSERTION ---
        output_lines = res.output.strip().split('\n')
        assert output_lines[-1] == "1.67"

    def test_cli_sqrt_integration(self):
        """Test CLI can perform square root"""
        res = self.run_cli('sqrt', '16')
        assert res.exit_code == 0
        
        # FIX: Check only the last line of stdout to ignore verbose output (from previous fix)
        output_lines = res.output.strip().split('\n')
        assert output_lines[-1] == "4" 

    def test_cli_error_handling_integration(self):
        """Test CLI properly handles calculator errors"""
        res = self.run_cli("divide", "10", "0")
        assert res.exit_code == 1
        assert "Cannot divide by zero" in res.output

    def test_cli_invalid_operation_integration(self):
        """Test CLI handles invalid operations"""
        res = self.run_cli("invalid", "1", "2")
        assert res.exit_code == 1
        assert "Unknown operation" in res.output

    def test_cli_subtract_integration(self):
        """Test CLI can perform subtraction"""
        res = self.run_cli("subtract", "5", "3")
        assert res.exit_code == 0
        assert res.output.strip() == "2"

    def test_cli_subtract_missing_operand_error(self):
        """Test CLI handles missing operand for subtraction gracefully"""
        res = self.run_cli("subtract", "5")
        assert res.exit_code == 1
        
        # FIX: Asserts against the specific error message as required
        assert EXPECTED_SUBTRACT_ERROR in res.output.strip()


class TestCalculatorModuleIntegration:
    """Test calculator module functions work together"""

    def test_chained_operations(self):
        """Test using results from one operation in another"""
        from src.calculator import add, multiply, divide

        # Calculate (5 + 3) * 2 / 4
        step1 = add(5, 3)  # 8
        step2 = multiply(step1, 2)  # 16
        step3 = divide(step2, 4)  # 4

        assert step3 == 4.0

    def test_complex_calculation_integration(self):
        """Test complex calculation using multiple functions"""
        from src.calculator import power, square_root, add

        # Calculate sqrt(3^2 + 4^2) = 5 (Pythagorean theorem)
        a_squared = power(3, 2)  # 9
        b_squared = power(4, 2)  # 16
        sum_squares = add(a_squared, b_squared)  # 25
        hypotenuse = square_root(sum_squares)  # 5

        assert hypotenuse == 5.0