"""Tests for FunctionGrapherLink."""
import pytest
import math
from codeuchain.core import Context
from calculator.links.function_grapher import FunctionGrapherLink


@pytest.mark.asyncio
async def test_linear_function():
    \"\"\"Test graphing linear function.\"\"\"
    link = FunctionGrapherLink()
    # f(x) = 2x + 1
    ctx = Context({
        \"function\": \"linear\",
        \"coefficients\": [2, 1],  # [slope, intercept]
        \"x_range\": [-5, 5],
        \"num_points\": 11
    })
    result = await link.call(ctx)
    
    assert result.get(\"function\") == \"linear\"
    assert result.get(\"num_points\") == 11
    assert \"points\" in result.to_dict()
    # Check a few points: f(-5) = -9, f(0) = 1, f(5) = 11
    points = result.get(\"points\")
    assert abs(points[0][1] - (-9)) < 1e-10
    assert abs(points[5][1] - 1) < 1e-10
    assert abs(points[10][1] - 11) < 1e-10


@pytest.mark.asyncio
async def test_quadratic_function():
    \"\"\"Test graphing quadratic function.\"\"\"
    link = FunctionGrapherLink()
    # f(x) = x^2
    ctx = Context({
        \"function\": \"quadratic\",
        \"coefficients\": [1, 0, 0],  # [a, b, c] for ax^2 + bx + c
        \"x_range\": [-3, 3],
        \"num_points\": 7
    })
    result = await link.call(ctx)
    
    points = result.get(\"points\")
    assert len(points) == 7
    # f(-3) = 9, f(0) = 0, f(3) = 9
    assert abs(points[0][1] - 9) < 1e-10
    assert abs(points[3][1] - 0) < 1e-10
    assert abs(points[6][1] - 9) < 1e-10


@pytest.mark.asyncio
async def test_sine_function():
    \"\"\"Test graphing sine function.\"\"\"
    link = FunctionGrapherLink()
    ctx = Context({
        \"function\": \"sine\",
        \"amplitude\": 1,
        \"frequency\": 1,
        \"phase\": 0,
        \"x_range\": [0, 2 * math.pi],
        \"num_points\": 5
    })
    result = await link.call(ctx)
    
    points = result.get(\"points\")
    assert len(points) == 5
    # sin(0) = 0, sin(π/2) ≈ 1, sin(π) ≈ 0, sin(3π/2) ≈ -1, sin(2π) ≈ 0
    assert abs(points[0][1] - 0) < 1e-10
    assert abs(points[2][1] - 0) < 1e-10
    assert abs(points[4][1] - 0) < 1e-10


@pytest.mark.asyncio
async def test_exponential_function():
    \"\"\"Test graphing exponential function.\"\"\"
    link = FunctionGrapherLink()
    # f(x) = e^x
    ctx = Context({
        \"function\": \"exponential\",
        \"base\": math.e,
        \"x_range\": [-2, 2],
        \"num_points\": 5
    })
    result = await link.call(ctx)
    
    points = result.get(\"points\")
    # f(0) = 1, f(1) = e ≈ 2.718
    assert abs(points[2][1] - 1) < 1e-10


@pytest.mark.asyncio
async def test_logarithmic_function():
    \"\"\"Test graphing logarithmic function.\"\"\"
    link = FunctionGrapherLink()
    # f(x) = ln(x)
    ctx = Context({
        \"function\": \"logarithmic\",
        \"base\": math.e,
        \"x_range\": [0.1, 10],
        \"num_points\": 5
    })
    result = await link.call(ctx)
    
    points = result.get(\"points\")
    assert len(points) == 5
    # ln(1) = 0
    # Find point closest to x=1
    ln_1_point = min([p for p in points], key=lambda p: abs(p[0] - 1))
    assert abs(ln_1_point[1] - 0) < 0.1  # Approximate since not exactly x=1


@pytest.mark.asyncio
async def test_points_format():
    \"\"\"Test that output points are in correct format.\"\"\"
    link = FunctionGrapherLink()
    ctx = Context({
        \"function\": \"linear\",
        \"coefficients\": [1, 0],
        \"x_range\": [0, 2],
        \"num_points\": 3
    })
    result = await link.call(ctx)
    
    points = result.get(\"points\")
    # Points should be [x, y] tuples/lists
    for point in points:
        assert len(point) == 2
        assert isinstance(point[0], (int, float))
        assert isinstance(point[1], (int, float))
