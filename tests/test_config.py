import json

import pytest

from czatpythom.config import AppConfig


def test_config_never_persists_token(tmp_path, monkeypatch):
    monkeypatch.setenv("CZATPYTHOM_GITHUB_TOKEN", "secret-value")
    path = tmp_path / "config.json"
    config = AppConfig(repository="Swir/private-chat")
    config.save(path)
    raw = path.read_text(encoding="utf-8")
    assert "secret-value" not in raw
    assert "token" not in json.loads(raw)


def test_github_backend_requires_token(monkeypatch):
    monkeypatch.delenv("CZATPYTHOM_GITHUB_TOKEN", raising=False)
    config = AppConfig(backend="github", repository="Swir/private-chat")
    with pytest.raises(ValueError):
        config.validate()


def test_poll_interval_is_bounded():
    config = AppConfig(poll_seconds=0.1)
    config.validate()
    assert config.poll_seconds == 2.0
