from .base import Tool, ToolResult


class SummarizerTool(Tool):
    name = "summarizer"
    description = "Summarizes text"

    async def execute(self, **kwargs) -> ToolResult:
        text = kwargs.get("text", "")
        target = int(kwargs.get("target_length", 120))
        mode = kwargs.get("mode", "extractive")
        words = text.split()
        summary = " ".join(words[:target]) if mode == "extractive" else "Summary: " + " ".join(words[:max(20, min(len(words), target // 2))])
        return ToolResult(True, {"summary": summary})

    def get_schema(self) -> dict:
        return {"type": "object", "properties": {"text": {"type": "string"}, "target_length": {"type": "integer"}, "mode": {"type": "string"}}, "required": ["text"]}
