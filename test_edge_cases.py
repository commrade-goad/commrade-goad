"""
Edge case tests for the enhanced equation solver.
"""

from equation_solver import solve_equations_manual


def test_edge_cases():
    """Test various edge cases for the equation solver."""
    
    print("=" * 60)
    print("EDGE CASE 1: Single variable, infinite solutions")
    print("=" * 60)
    # 0x = 0 (infinite solutions)
    equations1 = ["0x = 0"]
    result1 = solve_equations_manual(equations1)
    print(f"Result: {result1}")
    print()
    
    print("=" * 60)
    print("EDGE CASE 2: Single equation with multiple variables")
    print("=" * 60)
    # x + y + z = 5 (infinite solutions)
    equations2 = ["x + y + z = 5"]
    result2 = solve_equations_manual(equations2)
    print(f"Result type: {result2.get('type', 'unique')}")
    print()
    
    print("=" * 60)
    print("EDGE CASE 3: System with negative coefficients")
    print("=" * 60)
    # -2x + 4y = 6, x - 2y = -3 (infinite solutions)
    equations3 = ["-2x + 4y = 6", "x - 2y = -3"]
    result3 = solve_equations_manual(equations3)
    print(f"Result type: {result3.get('type', 'unique')}")
    print()
    
    print("=" * 60)
    print("EDGE CASE 4: Large system with infinite solutions")
    print("=" * 60)
    # 4 variables, 2 equations, infinite solutions
    equations4 = ["x + 2y + 3z + 4w = 10", "2x + 4y + 6z + 8w = 20"]
    result4 = solve_equations_manual(equations4)
    print(f"Result type: {result4.get('type', 'unique')}")
    print()
    
    print("=" * 60)
    print("EDGE CASE 5: Mixed integer and fractional coefficients")
    print("=" * 60)
    # 0.5x + y = 1.5, x + 2y = 3 (infinite solutions)
    equations5 = ["0.5x + y = 1.5", "x + 2y = 3"]
    result5 = solve_equations_manual(equations5)
    print(f"Result type: {result5.get('type', 'unique')}")
    print()


def test_solution_verification():
    """Test that solutions actually work with original equations."""
    
    print("=" * 60)
    print("SOLUTION VERIFICATION: Complex case")
    print("=" * 60)
    
    # Test with 3 variables
    equations = ["x + 2y + 3z = 6", "2x + 4y + 6z = 12"]
    result = solve_equations_manual(equations)
    
    if result.get('type') == 'infinite':
        print("Verifying 3-variable infinite solution examples:")
        for i, solution in enumerate(result['example_solutions']):
            x = solution.get('x', 0)
            y = solution.get('y', 0)
            z = solution.get('z', 0)
            
            # Check first equation: x + 2y + 3z = 6
            eq1_left = x + 2*y + 3*z
            eq1_right = 6
            
            # Check second equation: 2x + 4y + 6z = 12
            eq2_left = 2*x + 4*y + 6*z
            eq2_right = 12
            
            print(f"Solution {i+1}: x={x}, y={y}, z={z}")
            print(f"  Equation 1: {x} + 2({y}) + 3({z}) = {eq1_left} (should be {eq1_right}) - {'✓' if abs(eq1_left - eq1_right) < 1e-10 else '✗'}")
            print(f"  Equation 2: 2({x}) + 4({y}) + 6({z}) = {eq2_left} (should be {eq2_right}) - {'✓' if abs(eq2_left - eq2_right) < 1e-10 else '✗'}")
            print()


def test_parser_edge_cases():
    """Test equation parsing with various formats."""
    
    print("=" * 60)
    print("PARSER EDGE CASES")
    print("=" * 60)
    
    # Test various equation formats
    test_equations = [
        ["x + y = 2", "x + y = 2"],  # Identical equations
        ["3x - 2y = 5", "6x - 4y = 10"],  # Proportional equations
        ["-x + y = 1", "x - y = -1"],  # Negative coefficients
        ["x = 1", "y = 2"],  # Simple assignments
    ]
    
    for i, equations in enumerate(test_equations):
        print(f"Test {i+1}: {equations}")
        try:
            result = solve_equations_manual(equations)
            print(f"  Result type: {result.get('type', 'unique')}")
        except Exception as e:
            print(f"  Error: {e}")
        print()


if __name__ == "__main__":
    test_edge_cases()
    test_solution_verification()
    test_parser_edge_cases()