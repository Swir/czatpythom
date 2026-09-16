from __future__ import annotations

from collections.abc import Callable
import threading
import time

from .backends import MessageBackend
from .models import ChatMessage, normalize_room, normalize_username


class ChatClient:
    def __init__(
        self,
        backend: MessageBackend,
        username: str,
        room: str = "lobby",
        nick_color: str = "cyan",
        text_color: str = "white",
    ) -> None:
        self.backend = backend
        self.username = normalize_username(username)
        self.room = normalize_room(room)
        self.nick_color = nick_color
        self.text_color = text_color
        self._seen: set[str] = set()
        self._lock = threading.Lock()

    def send(self, text: str) -> ChatMessage:
        message = ChatMessage.create(
            username=self.username,
            text=text,
            room=self.room,
            nick_color=self.nick_color,
            text_color=self.text_color,
        )
        self.backend.append_message(message)
        with self._lock:
            self._seen.add(message.id)
        return message

    def poll_once(self, include_existing: bool = False) -> list[ChatMessage]:
        messages = self.backend.list_messages(self.room)
        fresh: list[ChatMessage] = []
        with self._lock:
            if not self._seen and not include_existing:
                self._seen.update(item.id for item in messages)
                return []
            for item in messages:
                if item.id not in self._seen:
                    self._seen.add(item.id)
                    fresh.append(item)
        return fresh

    def change_room(self, room: str) -> None:
        with self._lock:
            self.room = normalize_room(room)
            self._seen.clear()

    def change_username(self, username: str) -> None:
        self.username = normalize_username(username)

    def receiver_loop(
        self,
        callback: Callable[[ChatMessage], None],
        stop_event: threading.Event,
        poll_seconds: float,
        on_error: Callable[[Exception], None] | None = None,
    ) -> None:
        while not stop_event.wait(poll_seconds):
            try:
                for message in self.poll_once():
                    callback(message)
            except Exception as exc:  # network/backend boundary
                if on_error:
                    on_error(exc)
                time.sleep(min(poll_seconds, 5.0))
