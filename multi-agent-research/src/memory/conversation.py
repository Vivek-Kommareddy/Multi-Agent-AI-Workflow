from collections import deque


class ConversationMemory:
    def __init__(self, max_messages: int = 20) -> None:
        self._messages: deque[dict[str, str]] = deque(maxlen=max_messages)

    def add(self, role: str, content: str) -> None:
        self._messages.append({"role": role, "content": content})

    def history(self) -> list[dict[str, str]]:
        return list(self._messages)
