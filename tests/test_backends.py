from czatpythom.backends import LocalJsonBackend
from czatpythom.models import ChatMessage


def test_local_backend_roundtrip(tmp_path):
    backend = LocalJsonBackend(tmp_path, max_messages=3)
    first = ChatMessage.create("Alice", "one")
    backend.append_message(first)
    messages = backend.list_messages("lobby")
    assert [item.text for item in messages] == ["one"]
    assert messages[0].id == first.id


def test_local_backend_trims_old_messages(tmp_path):
    backend = LocalJsonBackend(tmp_path, max_messages=3)
    for index in range(5):
        backend.append_message(ChatMessage.create("Alice", str(index)))
    assert [item.text for item in backend.list_messages("lobby")] == ["2", "3", "4"]


def test_rooms_are_isolated(tmp_path):
    backend = LocalJsonBackend(tmp_path)
    backend.append_message(ChatMessage.create("Alice", "a", room="one"))
    backend.append_message(ChatMessage.create("Bob", "b", room="two"))
    assert [item.text for item in backend.list_messages("one")] == ["a"]
    assert [item.text for item in backend.list_messages("two")] == ["b"]


def test_clear_messages_only_clears_selected_room(tmp_path):
    backend = LocalJsonBackend(tmp_path)
    backend.append_message(ChatMessage.create("Alice", "a", room="one"))
    backend.append_message(ChatMessage.create("Bob", "b", room="two"))

    backend.clear_messages("one")

    assert backend.list_messages("one") == []
    assert [item.text for item in backend.list_messages("two")] == ["b"]
