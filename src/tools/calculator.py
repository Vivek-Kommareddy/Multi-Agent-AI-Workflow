import ast
import operator as op
from statistics import mean, median, pstdev
from typing import Any, Callable

from .base import Tool, ToolResult


class CalculatorTool(Tool):
    name = "calculator"
    description = "Safe arithmetic and stats"

    # Explicit Callable annotations so mypy knows the retrieved values are callable
    _ops: dict[type, Callable[..., Any]] = {
        ast.Add: op.add,
        ast.Sub: op.sub,
        ast.Mult: op.mul,
        ast.Div: op.truediv,
        ast.Pow: op.pow,
        ast.USub: op.neg,
    }
    _stat_ops: dict[str, Callable[..., Any]] = {
        "mean": mean,
        "median": median,
        "std": pstdev,
    }

    def _eval(self, node: ast.expr) -> Any:
        if isinstance(node, ast.Constant):
            return node.value
        if isinstance(node, ast.BinOp):
            op_fn = self._ops.get(type(node.op))
            if op_fn is None:
                raise ValueError(f"Unsupported operator: {type(node.op).__name__}")
            return op_fn(self._eval(node.left), self._eval(node.right))
        if isinstance(node, ast.UnaryOp):
            op_fn = self._ops.get(type(node.op))
            if op_fn is None:
                raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
            return op_fn(self._eval(node.operand))
        raise ValueError(f"Unsupported expression node: {type(node).__name__}")

    async def execute(self, **kwargs: Any) -> ToolResult:
        try:
            if kwargs.get("expression"):
                value = self._eval(ast.parse(kwargs["expression"], mode="eval").body)
                return ToolResult(True, {"value": value})
            numbers = kwargs.get("numbers")
            op_name = kwargs.get("operation")
            if numbers and op_name in self._stat_ops:
                fn = self._stat_ops[op_name]
                return ToolResult(True, {"value": fn(numbers)})
            return ToolResult(False, {}, "invalid input: provide 'expression' or 'numbers'+'operation'")
        except ZeroDivisionError:
            return ToolResult(False, {}, "division by zero")
        except SyntaxError as exc:
            return ToolResult(False, {}, f"syntax error in expression: {exc}")
        except ValueError as exc:
            return ToolResult(False, {}, str(exc))

    def get_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "expression": {"type": "string"},
                "numbers": {"type": "array", "items": {"type": "number"}},
                "operation": {"type": "string", "enum": ["mean", "median", "std"]},
            },
        }
