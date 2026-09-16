# Changelog

## 2.0.0 - 2026-09-17

### Added
- Modular `src/czatpythom` architecture.
- Modern Rich terminal interface with dark blue styling.
- Polish and English UI in one application with system-language detection.
- Local JSON backend for zero-setup private/local use.
- Optional GitHub repository backend configured entirely outside source code.
- Rooms, nickname changes, mention highlighting, local clear and status commands.
- Optimistic GitHub update retries to reduce lost-message conflicts.
- Legacy message migration from the old `message` + Unix timestamp schema.
- Per-user settings in the operating system application-data directory.
- Custom CzatPythom icon source and automated Windows ICO generation.
- Python 3.10-3.14 CI and Windows EXE/portable ZIP release automation.
- Unit tests for models, configuration and local persistence.

### Changed
- GitHub credentials are read only from `CZATPYTHOM_GITHUB_TOKEN` and are never written to config files.
- Default backend is local instead of modifying a public repository.
- Remote messages are isolated by normalized room name.

### Removed
- Hard-coded placeholder GitHub tokens and repository URLs.
- Destructive remote `/clean` behavior. `/clear` now clears only the local terminal.
- Duplicate Polish/English client implementations.
- Repository-tracked runtime message/user/room state.
- Legacy MP3/WAV notification assets; terminal-native notifications are used instead.
