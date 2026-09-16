from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import locale
import os
from pathlib import Path


def app_dir() -> Path:
    if os.name == "nt":
        root = Path(os.environ.get("APPDATA", Path.home()))
        return root / "CzatPythom"
    return Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "czatpythom"


def detect_language() -> str:
    language = (locale.getlocale()[0] or os.environ.get("LANG", "en")).lower()
    return "pl" if language.startswith("pl") else "en"


@dataclass(slots=True)
class AppConfig:
    backend: str = "local"
    repository: str = ""
    branch: str = "main"
    remote_dir: str = "chat_data/rooms"
    room: str = "lobby"
    username: str = ""
    nick_color: str = "cyan"
    text_color: str = "white"
    language: str = "auto"
    poll_seconds: float = 3.0
    max_messages: int = 500
    notifications: bool = True

    @property
    def token(self) -> str:
        return os.environ.get("CZATPYTHOM_GITHUB_TOKEN", "").strip()

    @property
    def resolved_language(self) -> str:
        return detect_language() if self.language == "auto" else self.language

    def validate(self) -> None:
        if self.backend not in {"local", "github"}:
            raise ValueError("backend must be local or github")
        if self.language not in {"auto", "pl", "en"}:
            raise ValueError("language must be auto, pl or en")
        self.poll_seconds = min(max(float(self.poll_seconds), 2.0), 60.0)
        self.max_messages = min(max(int(self.max_messages), 50), 2000)
        if self.backend == "github":
            if "/" not in self.repository:
                raise ValueError("GitHub backend requires repository in owner/name format")
            if not self.token:
                raise ValueError("GitHub backend requires CZATPYTHOM_GITHUB_TOKEN")

    def save(self, path: Path | None = None) -> Path:
        target = path or (app_dir() / "config.json")
        target.parent.mkdir(parents=True, exist_ok=True)
        payload = asdict(self)
        target.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
        return target

    @classmethod
    def load(cls, path: Path | None = None) -> "AppConfig":
        target = path or (app_dir() / "config.json")
        values: dict = {}
        if target.exists():
            try:
                values = json.loads(target.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                values = {}
        known = {field for field in cls.__dataclass_fields__}
        config = cls(**{key: value for key, value in values.items() if key in known})
        env_backend = os.environ.get("CZATPYTHOM_BACKEND")
        env_repository = os.environ.get("CZATPYTHOM_REPOSITORY")
        if env_backend:
            config.backend = env_backend.strip().lower()
        if env_repository:
            config.repository = env_repository.strip()
        return config
