from __future__ import annotations

import argparse
import random
import string
import sys
import threading

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.text import Text

from . import __version__
from .backends import build_backend
from .client import ChatClient
from .config import AppConfig
from .i18n import tr
from .models import COLOR_NAMES, ChatMessage, normalize_room, normalize_username

console = Console()

RICH_COLORS = {
    "green": "green",
    "blue": "blue",
    "red": "red",
    "yellow": "yellow",
    "magenta": "magenta",
    "cyan": "cyan",
    "bright_green": "bright_green",
    "bright_red": "bright_red",
    "bright_blue": "bright_blue",
    "white": "white",
}


def guest_name(language: str) -> str:
    prefix = "Gość" if language == "pl" else "Guest"
    suffix = "".join(random.choices(string.ascii_uppercase + string.digits, k=5))
    return f"{prefix}_{suffix}"


def print_message(message: ChatMessage, mention_target: str = "") -> None:
    nick_style = RICH_COLORS.get(message.nick_color, "cyan")
    text_style = RICH_COLORS.get(message.text_color, "white")
    header = Text()
    header.append(message.username, style=f"bold {nick_style}")
    header.append(f"  {message.local_time()}  ", style="dim")
    header.append(f"#{message.room}", style="bright_blue")
    body_style = text_style
    if mention_target and mention_target.lower() in message.text.lower():
        body_style = f"bold {text_style} on grey15"
        try:
            console.bell()
        except Exception:
            pass
    console.print(Panel(Text(message.text, style=body_style), title=header, border_style=nick_style, expand=False))


def render_banner(language: str, config: AppConfig) -> None:
    backend_name = tr(language, "backend_github" if config.backend == "github" else "backend_local")
    console.print(
        Panel.fit(
            f"[bold bright_blue]{tr(language, 'title')}[/]\n[cyan]{tr(language, 'subtitle')}[/]\n[dim]{backend_name}[/]",
            border_style="bright_blue",
        )
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="CzatPythom 2 terminal chat")
    parser.add_argument("--version", action="version", version=f"CzatPythom {__version__}")
    parser.add_argument("--backend", choices=["local", "github"])
    parser.add_argument("--repository", help="GitHub repository in owner/name form")
    parser.add_argument("--room", help="Initial room")
    parser.add_argument("--language", choices=["auto", "pl", "en"])
    parser.add_argument("--username")
    parser.add_argument("--poll", type=float, help="Refresh interval in seconds (2-60)")
    return parser.parse_args(argv)


def apply_args(config: AppConfig, args: argparse.Namespace) -> AppConfig:
    if args.backend:
        config.backend = args.backend
    if args.repository:
        config.repository = args.repository
    if args.room:
        config.room = normalize_room(args.room)
    if args.language:
        config.language = args.language
    if args.username:
        config.username = normalize_username(args.username)
    if args.poll is not None:
        config.poll_seconds = args.poll
    return config


def first_run_identity(config: AppConfig, language: str, args: argparse.Namespace) -> None:
    """Restore the legacy nickname/color setup without blocking headless runs."""
    if config.username or args.username or not sys.stdin.isatty():
        if not config.username:
            config.username = guest_name(language)
        return

    default_guest = guest_name(language)
    chosen = Prompt.ask(tr(language, "login_prompt"), default=default_guest).strip()
    config.username = normalize_username(chosen or default_guest)
    config.nick_color = Prompt.ask(
        tr(language, "nick_color_prompt"),
        choices=list(COLOR_NAMES),
        default=config.nick_color if config.nick_color in COLOR_NAMES else "cyan",
    )
    config.text_color = Prompt.ask(
        tr(language, "text_color_prompt"),
        choices=list(COLOR_NAMES),
        default=config.text_color if config.text_color in COLOR_NAMES else "white",
    )


def _set_color(client: ChatClient, config: AppConfig, language: str, target: str, value: str) -> bool:
    color = value.strip().lower()
    if color not in COLOR_NAMES:
        console.print(f"[yellow]{tr(language, 'invalid_color', colors=', '.join(COLOR_NAMES))}[/]")
        return False
    if target == "nick":
        client.nick_color = color
        config.nick_color = color
        label = tr(language, "nick_color_name")
    else:
        client.text_color = color
        config.text_color = color
        label = tr(language, "text_color_name")
    config.save()
    console.print(f"[green]{tr(language, 'color_changed', target=label, color=color)}[/]")
    return True


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    config = apply_args(AppConfig.load(), args)
    language = config.resolved_language
    first_run_identity(config, language, args)

    try:
        config.validate()
    except ValueError as exc:
        console.print(f"[bold red]{exc}[/]")
        if config.backend == "github":
            console.print(f"[yellow]{tr(language, 'github_setup')}[/]")
        return 2

    config.save()
    backend = build_backend(config)
    client = ChatClient(
        backend=backend,
        username=config.username,
        room=config.room,
        nick_color=config.nick_color,
        text_color=config.text_color,
    )

    render_banner(language, config)
    console.print(f"[green]{tr(language, 'welcome', username=client.username, room=client.room)}[/]")
    if config.backend == "github":
        console.print(f"[yellow]{tr(language, 'privacy')}[/]")

    try:
        history = backend.list_messages(client.room)[-20:]
        for message in history:
            print_message(message, client.username)
        client.poll_once(include_existing=True)
    except Exception as exc:
        console.print(f"[yellow]{tr(language, 'poll_error', error=exc)}[/]")

    stop_event = threading.Event()

    def on_message(message: ChatMessage) -> None:
        if message.username != client.username:
            print_message(message, client.username)

    def on_error(exc: Exception) -> None:
        console.print(f"[dim yellow]{tr(language, 'poll_error', error=exc)}[/]")

    receiver = threading.Thread(
        target=client.receiver_loop,
        args=(on_message, stop_event, config.poll_seconds, on_error),
        daemon=True,
    )
    receiver.start()

    try:
        while True:
            try:
                raw = Prompt.ask(f"[bold cyan]{client.username}[/] [dim]#{client.room}[/] >").strip()
            except (EOFError, KeyboardInterrupt):
                raw = "/quit"
            if not raw:
                console.print(f"[yellow]{tr(language, 'empty')}[/]")
                continue
            if raw.startswith("/"):
                command, _, value = raw.partition(" ")
                command = command.lower()
                value = value.strip()
                if command in {"/quit", "/exit"}:
                    break
                if command == "/help":
                    console.print(tr(language, "help"))
                    continue
                if command == "/clear":
                    console.clear()
                    render_banner(language, config)
                    console.print(f"[dim]{tr(language, 'cleared')}[/]")
                    continue
                if command == "/clean":
                    if Confirm.ask(tr(language, "clean_confirm", room=client.room), default=False):
                        try:
                            backend.clear_messages(client.room)
                            console.print(f"[green]{tr(language, 'history_cleared', room=client.room)}[/]")
                        except Exception as exc:
                            console.print(f"[bold red]{tr(language, 'clean_error', error=exc)}[/]")
                    else:
                        console.print(f"[dim]{tr(language, 'cancelled')}[/]")
                    continue
                if command == "/status":
                    console.print(
                        tr(
                            language,
                            "status",
                            backend=config.backend,
                            room=client.room,
                            poll=config.poll_seconds,
                            nick_color=client.nick_color,
                            text_color=client.text_color,
                        )
                    )
                    continue
                if command == "/room" and value:
                    client.change_room(value)
                    config.room = client.room
                    config.save()
                    console.print(f"[green]{tr(language, 'room_changed', room=client.room)}[/]")
                    for message in backend.list_messages(client.room)[-20:]:
                        print_message(message, client.username)
                    client.poll_once(include_existing=True)
                    continue
                if command == "/nick" and value:
                    client.change_username(value)
                    config.username = client.username
                    config.save()
                    console.print(f"[green]{tr(language, 'nick_changed', username=client.username)}[/]")
                    continue
                if command == "/nickcolor" and value:
                    _set_color(client, config, language, "nick", value)
                    continue
                if command == "/textcolor" and value:
                    _set_color(client, config, language, "text", value)
                    continue
                if command == "/colors":
                    console.print(tr(language, "colors"))
                    continue
                console.print(f"[yellow]{tr(language, 'help')}[/]")
                continue
            try:
                sent = client.send(raw)
                print_message(sent, client.username)
            except Exception as exc:
                console.print(f"[bold red]{tr(language, 'sent_error', error=exc)}[/]")
    finally:
        stop_event.set()
        config.room = client.room
        config.username = client.username
        config.nick_color = client.nick_color
        config.text_color = client.text_color
        config.save()
        console.print(f"[cyan]{tr(language, 'bye')}[/]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
