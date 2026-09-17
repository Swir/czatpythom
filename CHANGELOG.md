# Changelog

## 2.1.0 - 2026-09-17

### Restored after regression audit
- First-run nickname setup with generated guest fallback, matching the classic client behavior without blocking headless runs.
- Interactive nickname and message color selection on first run.
- Runtime `/nickcolor COLOR` and `/textcolor COLOR` commands so users can actually change both colors again.
- Legacy `/clean` room-history clearing with an explicit destructive-action confirmation. `/clear` remains local-screen-only.
- Full migration of legacy Colorama names such as `LIGHTGREEN_EX`, `LIGHTRED_EX` and `LIGHTBLUE_EX` to Rich equivalents.

### Improved
- `/status` now reports nickname and message colors.
- Local history clearing is atomic and isolated to the selected room.
- GitHub-backed room clearing uses the same conflict-retry strategy as message appends.
- Regression tests cover room clearing and legacy color migration.
- README now displays the project icon and documents the audited classic-to-modern feature mapping.
- Windows release packaging derives its version from the package instead of hard-coding artifact/tag names.

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
- Duplicate Polish/English client implementations.
- Repository-tracked runtime message/user/room state.
- Legacy MP3/WAV notification assets; terminal-native notifications are used instead.
