from src.memory.conversation import ConversationMemory
from src.memory.shared_memory import SharedMemory
from src.memory.vector_memory import VectorMemory


def test_conversation_window():
    memory = ConversationMemory(max_messages=2)
    memory.add("u", "a")
    memory.add("u", "b")
    memory.add("u", "c")
    assert [m["content"] for m in memory.history()] == ["b", "c"]


def test_shared_memory_rw():
    memory = SharedMemory()
    memory.write("topic", "key", 1)
    assert memory.read("topic", "key") == 1


def test_vector_memory_search():
    vm = VectorMemory()
    vm.add("AI healthcare", {"id": 1})
    vm.add("robotics farming", {"id": 2})
    assert vm.search("healthcare", 1)[0]["metadata"]["id"] == 1
