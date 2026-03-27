from math import sqrt


class VectorMemory:
    def __init__(self) -> None:
        self._items: list[tuple[str, list[float], dict[str, object]]] = []

    def _embed(self, text: str) -> list[float]:
        vec = [0.0, 0.0, 0.0]
        for i, ch in enumerate(text.lower()[:300]):
            vec[i % 3] += ord(ch) / 255
        return vec

    def _cos(self, a: list[float], b: list[float]) -> float:
        dot = sum(x * y for x, y in zip(a, b))
        na = sqrt(sum(x * x for x in a)) or 1.0
        nb = sqrt(sum(x * x for x in b)) or 1.0
        return dot / (na * nb)

    def _keyword_overlap(self, query: str, text: str) -> float:
        q = set(query.lower().split())
        t = set(text.lower().split())
        if not q:
            return 0.0
        return len(q & t) / len(q)

    def add(self, text: str, metadata: dict[str, object]) -> None:
        self._items.append((text, self._embed(text), metadata))

    def search(self, query: str, k: int = 3) -> list[dict[str, object]]:
        q_vec = self._embed(query)
        ranked = sorted(
            self._items,
            key=lambda x: (self._keyword_overlap(query, x[0]) * 2.0) + self._cos(q_vec, x[1]),
            reverse=True,
        )[:k]
        return [{"text": text, "metadata": metadata} for text, _, metadata in ranked]
