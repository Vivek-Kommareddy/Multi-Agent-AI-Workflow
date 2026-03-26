from pathlib import Path

from .base import Tool, ToolResult


class FileWriterTool(Tool):
    name = "file_writer"
    description = "Writes files"

    async def execute(self, **kwargs) -> ToolResult:
        path = Path(kwargs.get("path", "outputs/report.md"))
        content = kwargs.get("content", "")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return ToolResult(True, {"path": str(path), "bytes": len(content.encode())})

    def get_schema(self) -> dict:
        return {"type": "object", "properties": {"path": {"type": "string"}, "content": {"type": "string"}}, "required": ["path", "content"]}
