class SharedMemory:
    def __init__(self) -> None:
        self._data: dict[str, dict[str, object]] = {}

    def write(self, namespace: str, key: str, value: object) -> None:
        self._data.setdefault(namespace, {})[key] = value

    def read(self, namespace: str, key: str, default: object | None = None) -> object | None:
        return self._data.get(namespace, {}).get(key, default)
