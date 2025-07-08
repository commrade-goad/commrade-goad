# Enhanced Linear Equation Solver

This repository contains an enhanced linear equation solver that can handle systems with unique solutions, infinite solutions, and no solutions. The key enhancement is the ability to provide **multiple example solutions** when infinite solutions exist.

## Features

- **Unique Solution Detection**: Finds exact values when the system has one unique solution
- **Infinite Solution Enhancement**: Generates 5 different example solutions showing various ways to satisfy the system
- **No Solution Detection**: Identifies inconsistent systems
- **Comprehensive Parsing**: Handles various equation formats including negative coefficients and fractional values
- **Solution Verification**: All generated solutions are mathematically verified

## Enhanced Infinite Solution Handling

When infinite solutions are detected (when `rank(A) < number of variables` and `rank(A) = rank(augmented)`), the solver:

1. **Identifies Variable Types**:
   - Basic variables: Variables that depend on others
   - Free variables: Variables that can take any value

2. **Generates 5 Example Solutions**:
   - Sets free variables to different values: `[0, 1, -1, 2, -2]`
   - For multiple free variables, creates diverse combinations
   - Calculates corresponding basic variable values using back-substitution

3. **Displays Results Clearly**:
   - Shows which variables are basic vs. free
   - Lists all example solutions with variable assignments
   - Provides mathematical verification that solutions work

## Usage

```python
from equation_solver import solve_equations_manual

# Example with infinite solutions
equations = ["2x + 4y = 6", "x + 2y = 3"]
result = solve_equations_manual(equations)

# Output shows:
# - Basic variables: ['x']
# - Free variables: ['y']
# - 5 example solutions with different y values and corresponding x values
```

## Example Output

For the system `2x + 4y = 6`, `x + 2y = 3`:

```
Infinite solutions detected!
Basic variables: ['x']
Free variables: ['y']

Example solution 1:
  x = 3.0
  y = 0

Example solution 2:
  x = 1.0
  y = 1

Example solution 3:
  x = 5.0
  y = -1

Example solution 4:
  x = -1.0
  y = 2

Example solution 5:
  x = 7.0
  y = -2
```

## Mathematical Verification

All generated solutions satisfy the original equations:
- Solution 1: `2(3.0) + 4(0) = 6` ✓ and `3.0 + 2(0) = 3` ✓
- Solution 2: `2(1.0) + 4(1) = 6` ✓ and `1.0 + 2(1) = 3` ✓
- And so on...

## Files

- `equation_solver.py`: Main solver implementation
- `test_equation_solver.py`: Basic functionality tests
- `test_edge_cases.py`: Edge case and verification tests

## Algorithm Details

The solver uses:
1. **Gaussian-Jordan Elimination** for matrix reduction
2. **Rank Calculation** to determine solution type
3. **Back-substitution** to calculate basic variables from free variables
4. **Systematic Free Variable Assignment** to generate diverse examples

## Supported Equation Formats

- Standard form: `2x + 3y = 7`
- Negative coefficients: `-2x + 4y = 6`
- Fractional coefficients: `0.5x + y = 1.5`
- Mixed formats: `x - 2y = -3`

## Testing

Run the tests to verify functionality:

```bash
python test_equation_solver.py    # Basic tests
python test_edge_cases.py         # Edge cases and verification
python equation_solver.py         # Built-in examples
```

All tests include mathematical verification that generated solutions actually satisfy the original equations.