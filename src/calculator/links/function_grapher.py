"""FunctionGrapherLink - Link for graphing mathematical functions."""
import math
from codeuchain.core import Context, Link


class FunctionGrapherLink(Link[dict, dict]):
    """
    A CodeUChain Link for graphing mathematical functions.
    
    Supported functions: linear, quadratic, sine, exponential, logarithmic
    
    Input Contract:
        {
            \"function\": \"linear\" | \"quadratic\" | \"sine\" | \"exponential\" | \"logarithmic\",
            \"x_range\": [min, max],
            \"num_points\": int,
            ... function-specific parameters
        }
    
    Output Contract:
        {
            \"points\": [[x, y], [x, y], ...],
            \"function\": str,
            \"x_range\": [min, max],
            \"num_points\": int,
            ... all input parameters
        }
    """
    
    async def call(self, ctx: Context[dict]) -> Context[dict]:
        \"\"\"
        Execute the function graphing operation.
        
        Args:
            ctx: Context containing function type, x_range, num_points, and parameters
            
        Returns:
            Context with points array containing [x, y] coordinates
            
        Raises:
            ValueError: If function type is unsupported
            ValueError: If required parameters are missing
        \"\"\"
        function = ctx.get(\"function\")
        x_range = ctx.get(\"x_range\")
        num_points = ctx.get(\"num_points\")
        
        # Validate inputs
        if not function:
            raise ValueError(\"Function is required.\")
        if not x_range or len(x_range) != 2:
            raise ValueError(\"x_range must be [min, max].\")
        if not num_points or num_points < 2:
            raise ValueError(\"num_points must be at least 2.\")
        
        x_min, x_max = x_range
        points = []
        
        # Generate x values
        x_values = [x_min + (x_max - x_min) * i / (num_points - 1) for i in range(num_points)]
        
        # Calculate y values based on function type
        for x in x_values:
            try:
                if function == \"linear\":
                    coefficients = ctx.get(\"coefficients\")
                    if not coefficients or len(coefficients) < 2:
                        raise ValueError(\"Linear requires [slope, intercept].\")
                    y = coefficients[0] * x + coefficients[1]
                
                elif function == \"quadratic\":
                    coefficients = ctx.get(\"coefficients\")
                    if not coefficients or len(coefficients) < 3:
                        raise ValueError(\"Quadratic requires [a, b, c] for ax^2+bx+c.\")
                    y = coefficients[0] * (x ** 2) + coefficients[1] * x + coefficients[2]
                
                elif function == \"sine\":
                    amplitude = ctx.get(\"amplitude\") or 1
                    frequency = ctx.get(\"frequency\") or 1
                    phase = ctx.get(\"phase\") or 0
                    y = amplitude * math.sin(frequency * x + phase)
                
                elif function == \"exponential\":
                    base = ctx.get(\"base\") or math.e
                    y = base ** x
                
                elif function == \"logarithmic\":
                    base = ctx.get(\"base\") or math.e
                    if x <= 0:
                        continue  # Skip non-positive values for logarithm
                    if base == math.e:
                        y = math.log(x)
                    else:
                        y = math.log(x, base)
                
                else:
                    raise ValueError(f\"Unsupported function: {function}\")
                
                points.append([x, y])
            
            except (ValueError, ZeroDivisionError) as e:
                # Skip points that cause errors (e.g., log of negative)
                continue
        
        # Return enriched context with points
        return ctx.insert(\"points\", points)
