from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import re
import time
import uuid

ROOM_RE = re.compile(r"[^a-zA-Z0-9_-]+")
COLOR_NAMES = (
    "green", "blue", "red", "yellow", "magenta", "cyan", "bright_green",
    "bright_red", "bright_blue", "white",
)


def normalize_room(value: str) -> str:
    value = ROOM_RE.sub("-", value.strip()).strip("-_ ").lower()
    return (value or "lobby")[:40]


def normalize_username(value: str) -> str:
    value = " ".join(value.strip().split())
    if not value:
        raise ValueError("username cannot be empty")
    return value[:32]


def normalize_text(value: str) -> str:
    value = value.replace("\x00", "").strip()
    if not value:
        raise ValueError("message cannot be empty")
    return value[:2000]


@dataclass(frozen=True, slots=True)
class ChatMessage:
    id: str
    username: str
    text: str
    timestamp: str
    room: str = "lobby"
    nick_color: str = "cyan"
    text_color: str = "white"

    @classmethod
    def create(
        cls,
        username: str,
        text: str,
        room: str = "lobby",
        nick_color: str = "cyan",
        text_color: str = "white",
    ) -> "ChatMessage":
        return cls(
            id=str(uuid.uuid4()),
            username=normalize_username(username),
            text=normalize_text(text),
            timestamp=datetime.now(timezone.utc).isoformat(),
            room=normalize_room(room),
            nick_color=nick_color if nick_color in COLOR_NAMES else "cyan",
            text_color=text_color if text_color in COLOR_NAMES else "white",
        )

    @classmethod
    def from_dict(cls, raw: dict) -> "ChatMessage":
        username = normalize_username(str(raw.get("username", "Guest")))
        text = normalize_text(str(raw.get("text", raw.get("message", ""))))
        timestamp = raw.get("timestamp")
        if isinstance(timestamp, (int, float)):
            timestamp = datetime.fromtimestamp(float(timestamp), timezone.utc).isoformat()
        elif not isinstance(timestamp, str) or not timestamp:
            timestamp = datetime.now(timezone.utc).isoformat()
        return cls(
            id=str(raw.get("id") or uuid.uuid5(uuid.NAMESPACE_URL, f"{username}:{timestamp}:{text}")),
            username=username,
            text=text,
            timestamp=timestamp,
            room=normalize_room(str(raw.get("room", "lobby"))),
            nick_color=str(raw.get("nick_color", "cyan")).lower(),
            text_color=str(raw.get("text_color", "white")).lower(),
        )

    def to_dict(self) -> dict:
        return asdict(self)

    def local_time(self) -> str:
        try:
            dt = datetime.fromisoformat(self.timestamp.replace("Z", "+00:00"))
            return dt.astimezone().strftime("%d.%m %H:%M:%S")
        except ValueError:
            return time.strftime("%d.%m %H:%M:%S")
