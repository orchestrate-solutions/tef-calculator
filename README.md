# TEF Calculator

A feature-rich calculator application demonstrating CodeUChain framework implementation with modular Links and composable Chains.

## Features

- **Arithmetic Operations**: Add, subtract, multiply, divide
- **Scientific Functions**: Powers, roots, trigonometry
- **Geometry**: 2D and 3D shape calculations
- **Graphing**: Function visualization and shape rendering
- **CLI Interface**: Command-line interface for easy access

## Architecture

The calculator is built using CodeUChain's Link/Chain pattern:

- **Links**: Isolated, async operations (e.g., `AddSubtractLink`, `TrigonometricLink`)
- **Chains**: Composed workflows that orchestrate Links (e.g., `ArithmeticChain`, `ScientificChain`)
- **Context**: Immutable data flowing through the pipeline

## Installation

```bash
pip install -e .
```

### Development Installation

```bash
pip install -e ".[dev]"
```

## Usage

### CLI

```bash
calculator --help
calculator add 5 3
calculator sqrt 16
```

### Python API

```python
from calculator.chains.arithmetic import ArithmeticChain
from codeuchain.core import Context

chain = ArithmeticChain()
result = await chain.run(Context({
    "operation": "add",
    "operands": [5, 3]
}))

print(result.get("result"))  # 8
```

## Project Structure

```
tef-calculator/
├── src/calculator/
│   ├── __init__.py
│   ├── cli.py
│   ├── links/
│   │   ├── add_subtract.py
│   │   ├── multiply_divide.py
│   │   ├── power_root.py
│   │   ├── trigonometric.py
│   │   ├── shapes_2d.py
│   │   ├── shapes_3d.py
│   │   ├── function_grapher.py
│   │   └── shape_renderer.py
│   └── chains/
│       ├── arithmetic.py
│       ├── scientific.py
│       ├── geometry.py
│       └── calculator.py
├── tests/
│   ├── conftest.py
│   ├── links/
│   │   ├── test_add_subtract.py
│   │   ├── test_multiply_divide.py
│   │   ├── test_power_root.py
│   │   ├── test_trigonometric.py
│   │   ├── test_shapes_2d.py
│   │   ├── test_shapes_3d.py
│   │   ├── test_function_grapher.py
│   │   └── test_shape_renderer.py
│   └── chains/
│       ├── test_arithmetic_chain.py
│       ├── test_scientific_chain.py
│       ├── test_geometry_chain.py
│       └── test_calculator_chain.py
├── pyproject.toml
├── README.md
└── .github/workflows/
    └── tests.yml
```

## Testing

Run all tests:

```bash
pytest
```

Run specific test file:

```bash
pytest tests/links/test_add_subtract.py
```

Run with coverage:

```bash
pytest --cov=src --cov-report=html
```

## CI/CD

GitHub Actions automatically runs tests and generates coverage reports on every push.

## Development Guidelines

- Use CodeUChain's Link/Chain pattern for all operations
- Keep Links focused and pure (no side effects)
- Use async/await for all Link operations
- Write tests before implementation (TDD)
- Maintain >80% code coverage

## License

MIT
