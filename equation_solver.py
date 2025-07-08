"""
Linear equation solver with support for unique, infinite, and no solutions.
"""

from dataclasses import dataclass
from enum import Enum
from typing import List, Tuple, Set, Dict, Any
import copy


class Operator(Enum):
    ADD = "+"
    SUB = "-"


ADD = Operator.ADD
SUB = Operator.SUB


@dataclass
class Term:
    coefficient: float
    variable: str
    operator: Operator


def parse_question(equation: str) -> Tuple[List[Term], float]:
    """Parse an equation string into terms and right-hand side value."""
    # Split by '='
    left, right = equation.split('=')
    rhs = float(right.strip())
    
    # Parse left side
    terms = []
    left = left.replace('-', '+-').replace(' ', '')
    
    # Split by + and filter empty strings
    parts = [p for p in left.split('+') if p]
    
    for part in parts:
        if not part:
            continue
            
        # Determine operator
        if part.startswith('-'):
            operator = SUB
            part = part[1:]
        else:
            operator = ADD
            
        # Extract coefficient and variable
        if part.isalpha():
            # Just a variable like 'x'
            coefficient = 1.0
            variable = part
        else:
            # Find where variable starts
            var_start = 0
            for i, char in enumerate(part):
                if char.isalpha():
                    var_start = i
                    break
            
            if var_start == 0:
                # Variable at start, coefficient is 1
                coefficient = 1.0
                variable = part
            else:
                # Coefficient followed by variable
                coefficient = float(part[:var_start])
                variable = part[var_start:]
        
        terms.append(Term(coefficient, variable, operator))
    
    return terms, rhs


def gauss_jordan(matrix: List[List[float]]) -> None:
    """Perform Gauss-Jordan elimination on the augmented matrix."""
    rows = len(matrix)
    cols = len(matrix[0])
    
    for i in range(min(rows, cols - 1)):
        # Find pivot
        pivot_row = i
        for j in range(i + 1, rows):
            if abs(matrix[j][i]) > abs(matrix[pivot_row][i]):
                pivot_row = j
        
        # Swap rows if needed
        if pivot_row != i:
            matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
        
        # Skip if pivot is zero
        if abs(matrix[i][i]) < 1e-10:
            continue
            
        # Scale pivot row
        pivot = matrix[i][i]
        for j in range(cols):
            matrix[i][j] /= pivot
        
        # Eliminate other rows
        for j in range(rows):
            if j != i and abs(matrix[j][i]) > 1e-10:
                factor = matrix[j][i]
                for k in range(cols):
                    matrix[j][k] -= factor * matrix[i][k]


def check_rank(matrix: List[List[float]]) -> int:
    """Calculate the rank of a matrix."""
    if not matrix or not matrix[0]:
        return 0
    
    # Create a copy to avoid modifying the original
    temp_matrix = [row[:] for row in matrix]
    
    rows = len(temp_matrix)
    cols = len(temp_matrix[0])
    
    # Gaussian elimination
    rank = 0
    for col in range(cols):
        # Find pivot
        pivot_row = -1
        for row in range(rank, rows):
            if abs(temp_matrix[row][col]) > 1e-10:
                pivot_row = row
                break
        
        if pivot_row == -1:
            continue
        
        # Swap rows
        if pivot_row != rank:
            temp_matrix[rank], temp_matrix[pivot_row] = temp_matrix[pivot_row], temp_matrix[rank]
        
        # Eliminate
        for row in range(rows):
            if row != rank and abs(temp_matrix[row][col]) > 1e-10:
                factor = temp_matrix[row][col] / temp_matrix[rank][col]
                for c in range(cols):
                    temp_matrix[row][c] -= factor * temp_matrix[rank][c]
        
        rank += 1
    
    return rank


def solve_equations_manual(eq: List[str]) -> Dict[str, Any]:
    """
    Solve a system of linear equations.
    
    Returns a dictionary with variable assignments.
    For infinite solutions, provides multiple example solutions.
    """
    ret = []
    parsed_equations = []
    all_vars = set()

    for e in eq:
        terms, rhs = parse_question(e)
        parsed_equations.append((terms, rhs))
        for term in terms:
            all_vars.add(term.variable)

    var_order = sorted(all_vars)
    A = []
    B = []

    for terms, rhs in parsed_equations:
        row = [0] * len(var_order)
        for term in terms:
            idx = var_order.index(term.variable)
            sign = 1 if term.operator == ADD else -1
            row[idx] += sign * term.coefficient
        A.append(row)
        B.append(rhs)

    augmented = [row + [b] for row, b in zip(A, B)]

    print(f"Variable: {A}")
    print(f"Result  : {B}")

    gauss_jordan(augmented)
    for row in augmented:
        ret.append(row[-1])

    coefficient = [row[:-1] for row in augmented]

    c_rank_A = check_rank(coefficient)
    c_rank_aug = check_rank(augmented)
    c_num_vars = len(coefficient[0])

    if c_rank_A != c_rank_aug:
        print("No solution")
        return {}
    elif c_rank_A < c_num_vars:
        print("Infinite solutions detected!")
        
        # Enhanced infinite solution handling
        return _generate_infinite_solutions(coefficient, augmented, var_order)
    else:
        print("Unique solution")
        return dict(zip(var_order, ret))


def _generate_infinite_solutions(coefficient: List[List[float]], augmented: List[List[float]], var_order: List[str]) -> Dict[str, Any]:
    """
    Generate and display multiple example solutions for infinite solution cases.
    """
    num_vars = len(var_order)
    rank = check_rank(coefficient)
    
    # Identify basic and free variables
    basic_vars = []
    free_vars = []
    
    # Find pivot columns (basic variables)
    pivot_cols = []
    for row in range(len(augmented)):
        for col in range(num_vars):
            if abs(augmented[row][col]) > 1e-10:
                if col not in pivot_cols:
                    pivot_cols.append(col)
                    basic_vars.append(var_order[col])
                break
    
    # Free variables are those not in pivot columns
    for i, var in enumerate(var_order):
        if i not in pivot_cols:
            free_vars.append(var)
    
    print(f"Basic variables: {basic_vars}")
    print(f"Free variables: {free_vars}")
    print()
    
    # Generate 5 different example solutions
    free_var_values = [
        [0] * len(free_vars),           # All zeros
        [1] * len(free_vars),           # All ones
        [-1] * len(free_vars),          # All negative ones
        [2] * len(free_vars),           # All twos
        [-2] * len(free_vars)           # All negative twos
    ]
    
    # If we have multiple free variables, create more diverse combinations
    if len(free_vars) > 1:
        free_var_values = [
            [0] * len(free_vars),
            [1] * len(free_vars),
            [-1] * len(free_vars),
            [1, 0] + [0] * (len(free_vars) - 2),  # First free var = 1, rest = 0
            [0, 1] + [0] * (len(free_vars) - 2),  # Second free var = 1, rest = 0
        ]
    
    example_solutions = []
    
    for i, free_values in enumerate(free_var_values):
        solution = {}
        
        # Set free variables
        for j, var in enumerate(free_vars):
            solution[var] = free_values[j]
        
        # Calculate basic variables using back-substitution
        # Work backwards through the augmented matrix
        for row in range(len(augmented) - 1, -1, -1):
            # Find the pivot variable for this row
            pivot_col = -1
            for col in range(num_vars):
                if abs(augmented[row][col]) > 1e-10:
                    pivot_col = col
                    break
            
            if pivot_col != -1:
                var_name = var_order[pivot_col]
                if var_name not in solution:  # Only calculate if not already set (basic variable)
                    # Calculate value: solve for this variable
                    rhs = augmented[row][-1]  # Right-hand side
                    for col in range(pivot_col + 1, num_vars):
                        other_var = var_order[col]
                        if other_var in solution:
                            rhs -= augmented[row][col] * solution[other_var]
                    
                    if abs(augmented[row][pivot_col]) > 1e-10:
                        solution[var_name] = rhs / augmented[row][pivot_col]
        
        example_solutions.append(solution)
        
        print(f"Example solution {i + 1}:")
        for var in var_order:
            value = solution.get(var, 0)
            print(f"  {var} = {value}")
        print()
    
    return {
        "type": "infinite",
        "basic_variables": basic_vars,
        "free_variables": free_vars,
        "example_solutions": example_solutions
    }


if __name__ == "__main__":
    # Test cases
    
    print("=" * 50)
    print("Test 1: Unique solution")
    print("=" * 50)
    equations1 = ["2x + 3y = 7", "x - y = 1"]
    result1 = solve_equations_manual(equations1)
    print(f"Result: {result1}")
    print()
    
    print("=" * 50)
    print("Test 2: Infinite solutions")
    print("=" * 50)
    equations2 = ["2x + 4y = 6", "x + 2y = 3"]
    result2 = solve_equations_manual(equations2)
    print(f"Result: {result2}")
    print()
    
    print("=" * 50)
    print("Test 3: No solution")
    print("=" * 50)
    equations3 = ["2x + 4y = 6", "x + 2y = 4"]
    result3 = solve_equations_manual(equations3)
    print(f"Result: {result3}")