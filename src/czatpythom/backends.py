from __future__ import annotations

import base64
import json
from pathlib import Path
import random
import threading
import time
from typing import Protocol
from urllib.parse import quote

import requests

from .config import AppConfig, app_dir
from .models import ChatMessage, normalize_room


class MessageBackend(Protocol):
    def list_messages(self, room: str) -> list[ChatMessage]: ...
    def append_message(self, message: ChatMessage) -> None: ...


class LocalJsonBackend:
    def __init__(self, root: Path | None = None, max_messages: int = 500) -> None:
        self.root = root or (app_dir() / "rooms")
        self.max_messages = max_messages
        self._lock = threading.Lock()

    def _path(self, room: str) -> Path:
        return self.root / f"{normalize_room(room)}.json"

    def list_messages(self, room: str) -> list[ChatMessage]:
        path = self._path(room)
        if not path.exists():
            return []
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return []
        result: list[ChatMessage] = []
        for item in raw if isinstance(raw, list) else []:
            try:
                result.append(ChatMessage.from_dict(item))
            except (TypeError, ValueError):
                continue
        return result

    def append_message(self, message: ChatMessage) -> None:
        with self._lock:
            path = self._path(message.room)
            path.parent.mkdir(parents=True, exist_ok=True)
            messages = self.list_messages(message.room)
            messages.append(message)
            payload = [item.to_dict() for item in messages[-self.max_messages :]]
            temp = path.with_suffix(".tmp")
            temp.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
            temp.replace(path)


class GitHubJsonBackend:
    API = "https://api.github.com"

    def __init__(self, config: AppConfig, session: requests.Session | None = None) -> None:
        self.config = config
        self.session = session or requests.Session()
        self.timeout = (5, 15)

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.config.token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Cache-Control": "no-cache",
        }

    def _remote_path(self, room: str) -> str:
        directory = self.config.remote_dir.strip("/")
        return f"{directory}/{normalize_room(room)}.json"

    def _url(self, room: str) -> str:
        owner_repo = "/".join(quote(part, safe="") for part in self.config.repository.split("/", 1))
        path = quote(self._remote_path(room), safe="/")
        return f"{self.API}/repos/{owner_repo}/contents/{path}"

    def _read(self, room: str) -> tuple[list[ChatMessage], str | None]:
        response = self.session.get(
            self._url(room), headers=self._headers(), params={"ref": self.config.branch}, timeout=self.timeout
        )
        if response.status_code == 404:
            return [], None
        response.raise_for_status()
        body = response.json()
        content = base64.b64decode(body.get("content", "")).decode("utf-8")
        raw = json.loads(content or "[]")
        messages: list[ChatMessage] = []
        for item in raw if isinstance(raw, list) else []:
            try:
                messages.append(ChatMessage.from_dict(item))
            except (TypeError, ValueError):
                continue
        return messages, body.get("sha")

    def list_messages(self, room: str) -> list[ChatMessage]:
        messages, _ = self._read(room)
        return messages

    def append_message(self, message: ChatMessage) -> None:
        for attempt in range(5):
            messages, sha = self._read(message.room)
            if any(item.id == message.id for item in messages):
                return
            messages.append(message)
            payload = [item.to_dict() for item in messages[-self.config.max_messages :]]
            encoded = base64.b64encode(json.dumps(payload, ensure_ascii=False, indent=2).encode()).decode()
            body: dict[str, object] = {
                "message": f"chat: append message in {message.room}",
                "content": encoded,
                "branch": self.config.branch,
            }
            if sha:
                body["sha"] = sha
            response = self.session.put(self._url(message.room), headers=self._headers(), json=body, timeout=self.timeout)
            if response.status_code in {409, 422} and attempt < 4:
                time.sleep(0.3 + random.random() * 0.7)
                continue
            response.raise_for_status()
            return
        raise RuntimeError("message update conflict after retries")


def build_backend(config: AppConfig) -> MessageBackend:
    if config.backend == "github":
        return GitHubJsonBackend(config)
    return LocalJsonBackend(max_messages=config.max_messages)
