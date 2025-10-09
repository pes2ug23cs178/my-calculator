"""
Command Line Interface for Calculator
Example: python src/cli.py add 5 3
"""

import sys
import click
# Note the change: 'src.calculator' is used for module imports from the project root.
from src.calculator import add, subtract, multiply, divide, power, square_root


@click.command()
@click.argument("operation")
@click.argument("num1", type=float)
@click.argument("num2", type=float, required=False)
def calculate(operation, num1, num2=None):
    """Simple calculator CLI"""
    
    # List of operations that require a second number (binary operations)
    binary_operations = ["add", "subtract", "multiply", "divide", "power"]

    try:
        # --- Missing Operand Check for Binary Operations ---
        if operation in binary_operations and num2 is None:
            # This is the exact error message your tests expect for missing operands
            click.echo(f"Error: Operation '{operation}' requires two numbers")
            sys.exit(1)

        # --- Operation Logic ---
        if operation == "add":
            result = add(num1, num2)
        elif operation == "subtract":
            result = subtract(num1, num2)
        elif operation == "multiply":
            result = multiply(num1, num2)
        elif operation == "divide":
            result = divide(num1, num2)
        elif operation == "power":
            result = power(num1, num2)
        elif operation in ("square_root", "sqrt"):
            result = square_root(num1)
        else:
            click.echo(f"Unknown operation: {operation}")
            sys.exit(1)

        # Format result nicely
        if result == int(result):
            click.echo(int(result))
        else:
            click.echo(f"{result:.2f}")

    except ValueError as e:
        click.echo(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        click.echo(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    calculate()