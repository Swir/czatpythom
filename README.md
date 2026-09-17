<div align="center">

<img src="assets/app_icon.svg" alt="CzatPythom icon" width="128" height="128">

# 💬 CzatPythom 2.1

### Modern PL/EN terminal chat with restored classic features and safe local or GitHub-backed storage

**Python 3.10–3.14 • Rich • Requests • JSON • Windows EXE**

![Python](https://img.shields.io/badge/Python-3.10--3.14-3776AB?logo=python&logoColor=white)
![UI](https://img.shields.io/badge/UI-Rich%20Terminal-1596D2)
![Storage](https://img.shields.io/badge/Storage-Local%20%7C%20GitHub-181717?logo=github)
![Release](https://img.shields.io/badge/Windows-EXE-0078D6?logo=windows)

</div>

---

## Regression audit result

CzatPythom 2.1 was compared against the original Polish and English console clients. The modern architecture is kept, while useful behavior that disappeared in v2.0 has been restored.

### Restored from the classic client

- custom nickname on first run or an automatically generated `Guest_XXXXX` / `Gość_XXXXX`
- separate nickname and message colors
- classic Colorama colors migrated correctly, including `LIGHTGREEN_EX`, `LIGHTRED_EX` and `LIGHTBLUE_EX`
- background polling and timestamped framed messages
- `/clean` room-history clearing, now protected by an explicit confirmation
- `quit`/`/quit` session ending behavior

### Modern features retained

- one multilingual PL/EN codebase with system-language detection
- modular `src/czatpythom` architecture
- dark-blue Rich terminal UI
- zero-setup **local backend** by default
- optional **GitHub repository backend** for shared rooms
- rooms, nickname changes, mention highlighting with terminal bell and live polling
- per-user settings outside the repository/application directory
- no hard-coded GitHub token
- optimistic GitHub update retries
- Python 3.10–3.14 CI
- custom application icon, Windows EXE, portable ZIP and SHA256 files

---

## Quick start

### Windows Release

Download the newest `CzatPythom.exe` or portable ZIP from **GitHub Releases**. SHA256 checksum files are published next to both downloads.

### Python

```bash
git clone https://github.com/Swir/czatpythom.git
cd czatpythom
python -m pip install -e .
python -m czatpythom
```

On the first interactive run you can choose your nickname plus separate nickname/message colors. Press Enter at the nickname prompt to keep the generated guest identity.

---

## Shared GitHub rooms

GitHub mode stores each room as a JSON file in a repository you choose. For private conversations, use a **private repository**.

PowerShell example:

```powershell
$env:CZATPYTHOM_BACKEND = "github"
$env:CZATPYTHOM_REPOSITORY = "OWNER/private-chat-data"
$env:CZATPYTHOM_GITHUB_TOKEN = "github_pat_..."
CzatPythom.exe --room lobby
```

Use a fine-grained token restricted to that single repository. The token is read from the environment only and is never saved in `config.json`.

> GitHub-backed chat is intended for a small/private project or demo. Repository API limits still apply.

---

## Commands

| Command | Action |
|---|---|
| `/help` | Show command help |
| `/room NAME` | Switch rooms |
| `/nick NAME` | Change nickname |
| `/nickcolor COLOR` | Change nickname color |
| `/textcolor COLOR` | Change message color |
| `/colors` | Show supported colors |
| `/status` | Show backend, room, refresh interval and active colors |
| `/clear` | Clear only the local terminal screen |
| `/clean` | Clear the current room history after confirmation |
| `/quit` or `quit` | End the session |

Supported colors: `green`, `blue`, `red`, `yellow`, `magenta`, `cyan`, `bright_green`, `bright_red`, `bright_blue`, `white`.

`/clean` affects only the currently selected room. On the GitHub backend it writes an empty room history to the configured repository and requires confirmation before the destructive action.

---

## CLI options

```text
--version
--backend local|github
--repository OWNER/REPO
--room ROOM
--language auto|pl|en
--username NAME
--poll SECONDS
```

Refresh intervals are bounded to 2–60 seconds.

---

## Project structure

```text
src/czatpythom/
  app.py          # Rich terminal application and commands
  backends.py     # local + GitHub storage, append/clear operations
  client.py       # polling and client state
  config.py       # per-user configuration
  i18n.py         # PL/EN translations
  models.py       # validated message model + legacy migration
assets/
  app_icon.svg    # source icon displayed in this README
  app_icon.ico    # generated during Windows builds
tools/
  build_icon.py
tests/
.github/workflows/
```

Runtime data is not committed to the source repository.

---

## Development and regression tests

```bash
python -m pip install -e ".[dev]"
python -m pytest
python -m czatpythom --version
```

CI tests Python **3.10, 3.11, 3.12, 3.13 and 3.14**. Regression coverage includes legacy message/color migration and room-scoped history clearing.

---

## Privacy & security

- Never commit GitHub tokens.
- Use a private repository for non-public GitHub-backed chat history.
- Do not exchange passwords, API keys or recovery codes through repository-backed rooms.
- CzatPythom never persists the GitHub token.
- `/clean` requires interactive confirmation and only clears the active room.
- New writes and history clears use optimistic retries to reduce repository update conflicts.
- See [`SECURITY.md`](SECURITY.md) for details.

---

## Release artifacts

Each Windows release produces:

- `CzatPythom.exe`
- `CzatPythom.exe.sha256`
- `CzatPythom-vX.Y.Z-Windows-x64.zip`
- `CzatPythom-vX.Y.Z-Windows-x64.zip.sha256`

The EXE is smoke-tested with `--version` before publication and release filenames are generated from the application version automatically.

---

## Author

Developed by **Swir** — [github.com/Swir](https://github.com/Swir)

<div align="center">

### by Swir ⚡

</div>
