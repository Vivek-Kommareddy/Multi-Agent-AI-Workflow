import asyncio
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class SharedState:
    data: dict[str, object] = field(default_factory=dict)
    log: list[dict[str, object]] = field(default_factory=list)

    def __post_init__(self) -> None:
        self._lock = asyncio.Lock()

    async def set(self, key: str, value: object) -> None:
        async with self._lock:
            self.data[key] = value

    async def get(self, key: str, default: object | None = None) -> object | None:
        async with self._lock:
            return self.data.get(key, default)

    async def append_log(self, agent: str, action: str, detail: object) -> None:
        async with self._lock:
            self.log.append({"ts": datetime.now(timezone.utc).isoformat(), "agent": agent, "action": action, "detail": detail})

    def to_json(self) -> str:
        return json.dumps({"data": self.data, "log": self.log}, ensure_ascii=False)
