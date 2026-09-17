from czatpythom.models import ChatMessage, normalize_room, normalize_text, normalize_username


def test_normalizers():
    assert normalize_room("  Main Room! ") == "main-room"
    assert normalize_username("  Jan   Kowalski  ") == "Jan Kowalski"
    assert normalize_text("  hello\x00  ") == "hello"


def test_create_message():
    message = ChatMessage.create("Swir", "Hello", room="Main Room", nick_color="cyan")
    assert message.username == "Swir"
    assert message.room == "main-room"
    assert message.text == "Hello"
    assert message.id


def test_legacy_message_is_migrated():
    message = ChatMessage.from_dict(
        {
            "username": "Guest",
            "message": "legacy",
            "timestamp": 1_700_000_000.0,
            "nick_color": "GREEN",
            "text_color": "WHITE",
        }
    )
    assert message.text == "legacy"
    assert message.room == "lobby"
    assert message.nick_color == "green"
    assert message.text_color == "white"
    assert "+00:00" in message.timestamp


def test_legacy_light_colors_map_to_rich_equivalents():
    message = ChatMessage.from_dict(
        {
            "username": "Guest",
            "message": "legacy colors",
            "timestamp": 1_700_000_000.0,
            "nick_color": "LIGHTGREEN_EX",
            "text_color": "LIGHTBLUE_EX",
        }
    )
    assert message.nick_color == "bright_green"
    assert message.text_color == "bright_blue"
