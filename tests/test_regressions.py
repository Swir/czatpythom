from czatpythom.app import is_quit_input
from czatpythom.models import ChatMessage


def test_classic_plain_quit_is_still_supported():
    assert is_quit_input("quit")
    assert is_quit_input(" QUIT ")
    assert is_quit_input("/quit")
    assert is_quit_input("/exit")
    assert not is_quit_input("quit later")


def test_classic_bright_color_aliases_survive_migration():
    message = ChatMessage.from_dict(
        {
            "username": "LegacyUser",
            "message": "hello",
            "timestamp": 1_700_000_000.0,
            "nick_color": "LIGHTRED_EX",
            "text_color": "LIGHTGREEN_EX",
        }
    )
    assert message.nick_color == "bright_red"
    assert message.text_color == "bright_green"
