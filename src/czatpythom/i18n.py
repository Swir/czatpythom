from __future__ import annotations

STRINGS = {
    "en": {
        "title": "CzatPythom 2",
        "subtitle": "Modern terminal chat",
        "backend_local": "Local JSON backend",
        "backend_github": "GitHub repository backend",
        "welcome": "Connected as {username} in #{room}",
        "prompt": "Message or /help",
        "empty": "Message cannot be empty.",
        "sent_error": "Could not send message: {error}",
        "poll_error": "Could not refresh messages: {error}",
        "help": "Commands: /help, /room NAME, /nick NAME, /colors, /clear, /status, /quit",
        "room_changed": "Room changed to #{room}",
        "nick_changed": "Nickname changed to {username}",
        "cleared": "Local screen cleared. Remote history was not deleted.",
        "status": "Backend: {backend} | room: #{room} | refresh: {poll}s",
        "bye": "Session ended.",
        "github_setup": "GitHub mode needs CZATPYTHOM_REPOSITORY=owner/repo and CZATPYTHOM_GITHUB_TOKEN.",
        "guest": "Guest",
        "colors": "Colors: green, blue, red, yellow, magenta, cyan, bright_green, bright_red, bright_blue, white",
        "privacy": "GitHub-backed messages are stored in the configured repository. Use a private repository for private conversations.",
    },
    "pl": {
        "title": "CzatPythom 2",
        "subtitle": "Nowoczesny czat terminalowy",
        "backend_local": "Lokalny backend JSON",
        "backend_github": "Backend repozytorium GitHub",
        "welcome": "Połączono jako {username} w #{room}",
        "prompt": "Wiadomość lub /help",
        "empty": "Wiadomość nie może być pusta.",
        "sent_error": "Nie udało się wysłać wiadomości: {error}",
        "poll_error": "Nie udało się odświeżyć wiadomości: {error}",
        "help": "Komendy: /help, /room NAZWA, /nick NAZWA, /colors, /clear, /status, /quit",
        "room_changed": "Zmieniono pokój na #{room}",
        "nick_changed": "Zmieniono nick na {username}",
        "cleared": "Wyczyszczono ekran lokalny. Historia zdalna nie została usunięta.",
        "status": "Backend: {backend} | pokój: #{room} | odświeżanie: {poll}s",
        "bye": "Zakończono sesję.",
        "github_setup": "Tryb GitHub wymaga CZATPYTHOM_REPOSITORY=owner/repo i CZATPYTHOM_GITHUB_TOKEN.",
        "guest": "Gość",
        "colors": "Kolory: green, blue, red, yellow, magenta, cyan, bright_green, bright_red, bright_blue, white",
        "privacy": "Wiadomości w trybie GitHub są przechowywane w skonfigurowanym repozytorium. Do prywatnych rozmów używaj prywatnego repozytorium.",
    },
}


def tr(language: str, key: str, **kwargs) -> str:
    language = language if language in STRINGS else "en"
    template = STRINGS[language].get(key, STRINGS["en"].get(key, key))
    return template.format(**kwargs)
