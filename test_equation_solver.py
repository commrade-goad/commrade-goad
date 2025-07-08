"""
Test cases for the equation solver to verify the enhanced infinite solution functionality.
"""

from equation_solver import solve_equations_manual


def test_infinite_solutions_cases():
    """Test various infinite solution scenarios."""
    
    print("=" * 60)
    print("TEST CASE 1: Simple infinite solutions (2 variables)")
    print("=" * 60)
    # System: 2x + 4y = 6, x + 2y = 3 (same equation essentially)
    equations1 = ["2x + 4y = 6", "x + 2y = 3"]
    result1 = solve_equations_manual(equations1)
    print(f"Result type: {result1.get('type', 'unique')}")
    print()
    
    print("=" * 60)
    print("TEST CASE 2: Infinite solutions with 3 variables")
    print("=" * 60)
    # System with 3 variables, 2 equations, infinite solutions
    equations2 = ["x + 2y + 3z = 6", "2x + 4y + 6z = 12"]
    result2 = solve_equations_manual(equations2)
    print(f"Result type: {result2.get('type', 'unique')}")
    print()
    
    print("=" * 60)
    print("TEST CASE 3: More complex infinite solutions")
    print("=" * 60)
    # System: x + y + z = 6, 2x + 2y + 2z = 12
    equations3 = ["x + y + z = 6", "2x + 2y + 2z = 12"]
    result3 = solve_equations_manual(equations3)
    print(f"Result type: {result3.get('type', 'unique')}")
    print()
    
    print("=" * 60)
    print("TEST CASE 4: Unique solution for comparison")
    print("=" * 60)
    # System with unique solution
    equations4 = ["2x + 3y = 7", "x - y = 1"]
    result4 = solve_equations_manual(equations4)
    print(f"Result type: {result4.get('type', 'unique')}")
    print()
    
    print("=" * 60)
    print("TEST CASE 5: No solution for comparison")
    print("=" * 60)
    # Inconsistent system
    equations5 = ["x + y = 1", "x + y = 2"]
    result5 = solve_equations_manual(equations5)
    print(f"Result type: {result5.get('type', 'none')}")
    print()


def verify_infinite_solution_examples():
    """Verify that the example solutions actually satisfy the original equations."""
    
    print("=" * 60)
    print("VERIFICATION: Checking if example solutions are correct")
    print("=" * 60)
    
    # Test case: 2x + 4y = 6, x + 2y = 3
    equations = ["2x + 4y = 6", "x + 2y = 3"]
    result = solve_equations_manual(equations)
    
    if result.get('type') == 'infinite':
        print("Verifying example solutions:")
        for i, solution in enumerate(result['example_solutions']):
            x = solution.get('x', 0)
            y = solution.get('y', 0)
            
            # Check first equation: 2x + 4y = 6
            eq1_left = 2*x + 4*y
            eq1_right = 6
            
            # Check second equation: x + 2y = 3
            eq2_left = x + 2*y
            eq2_right = 3
            
            print(f"Solution {i+1}: x={x}, y={y}")
            print(f"  Equation 1: 2({x}) + 4({y}) = {eq1_left} (should be {eq1_right}) - {'✓' if abs(eq1_left - eq1_right) < 1e-10 else '✗'}")
            print(f"  Equation 2: {x} + 2({y}) = {eq2_left} (should be {eq2_right}) - {'✓' if abs(eq2_left - eq2_right) < 1e-10 else '✗'}")
            print()


if __name__ == "__main__":
    test_infinite_solutions_cases()
    verify_infinite_solution_examples()