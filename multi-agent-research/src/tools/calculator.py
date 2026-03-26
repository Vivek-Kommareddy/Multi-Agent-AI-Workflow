import ast
import operator as op
from statistics import mean, median, pstdev

from .base import Tool, ToolResult


class CalculatorTool(Tool):
    name = "calculator"
    description = "Safe arithmetic and stats"
    _ops = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul, ast.Div: op.truediv, ast.Pow: op.pow, ast.USub: op.neg}

    def _eval(self, node):
        if isinstance(node, ast.Constant):
            return node.value
        if isinstance(node, ast.BinOp):
            return self._ops[type(node.op)](self._eval(node.left), self._eval(node.right))
        if isinstance(node, ast.UnaryOp):
            return self._ops[type(node.op)](self._eval(node.operand))
        raise ValueError("Unsupported expression")

    async def execute(self, **kwargs) -> ToolResult:
        if kwargs.get("expression"):
            value = self._eval(ast.parse(kwargs["expression"], mode="eval").body)
            return ToolResult(True, {"value": value})
        numbers = kwargs.get("numbers")
        op_name = kwargs.get("operation")
        if numbers and op_name in {"mean", "median", "std"}:
            fn = {"mean": mean, "median": median, "std": pstdev}[op_name]
            return ToolResult(True, {"value": fn(numbers)})
        return ToolResult(False, {}, "invalid input")

    def get_schema(self) -> dict:
        return {"type": "object", "properties": {"expression": {"type": "string"}, "numbers": {"type": "array", "items": {"type": "number"}}, "operation": {"type": "string"}}}
