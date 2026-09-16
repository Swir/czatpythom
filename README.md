<div align="center">

# 💬 CzatPythom 2

### Modern PL/EN terminal chat with safe local or GitHub-backed storage

**Python 3.10–3.14 • Rich • Requests • JSON • Windows EXE**

![Python](https://img.shields.io/badge/Python-3.10--3.14-3776AB?logo=python&logoColor=white)
![UI](https://img.shields.io/badge/UI-Rich%20Terminal-1596D2)
![Storage](https://img.shields.io/badge/Storage-Local%20%7C%20GitHub-181717?logo=github)
![Release](https://img.shields.io/badge/Windows-EXE-0078D6?logo=windows)

</div>

---

## What changed in v2

CzatPythom 2 replaces the old duplicated Polish/English scripts and repository-tracked runtime JSON files with one maintainable application.

- one multilingual codebase with automatic Polish/English selection
- modular `src/czatpythom` architecture
- modern dark-blue Rich terminal UI
- zero-setup **local backend** by default
- optional **GitHub repository backend** for shared rooms
- room switching, nickname changes, colors, mention highlighting and live polling
- legacy message compatibility
- per-user settings outside the repository/application directory
- no hard-coded tokens
- no destructive remote `/clean`
- tests + Python 3.10–3.14 CI
- custom app icon + Windows EXE + portable ZIP + SHA256 release artifacts

---

## Quick start

### Windows Release

Download the newest `CzatPythom.exe` or portable ZIP from **GitHub Releases**. The release also includes SHA256 checksum files.

### Python

```bash
git clone https://github.com/Swir/czatpythom.git
cd czatpythom
python -m pip install -e .
python -m czatpythom
```

The default mode is local and needs no account or token.

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

> GitHub-backed chat is a small-project/demo backend, not a replacement for a dedicated realtime messaging service. Repository API rate limits still apply.

---

## Commands

| Command | Action |
|---|---|
| `/help` | Show command help |
| `/room NAME` | Switch rooms |
| `/nick NAME` | Change nickname |
| `/colors` | Show supported color names |
| `/status` | Show backend/room/refresh state |
| `/clear` | Clear the local terminal only |
| `/quit` | End the session |

The legacy remote history-deletion command was intentionally removed to prevent accidental destructive writes.

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
  app.py          # Rich terminal application
  backends.py     # local + GitHub storage
  client.py       # polling and client state
  config.py       # per-user configuration
  i18n.py         # PL/EN translations
  models.py       # validated message model
assets/
  app_icon.svg
tools/
  build_icon.py
tests/
.github/workflows/
```

Runtime data is not committed to the source repository.

---

## Development

```bash
python -m pip install -e ".[dev]"
python -m pytest
python -m czatpythom --version
```

CI tests Python **3.10, 3.11, 3.12, 3.13 and 3.14**.

---

## Privacy & security

- Never commit GitHub tokens.
- Use a private repository for non-public GitHub-backed chat history.
- Do not exchange passwords, API keys or recovery codes through repository-backed rooms.
- CzatPythom does not persist the GitHub token.
- New writes use optimistic retries to reduce concurrent-update conflicts.
- See [`SECURITY.md`](SECURITY.md) for details.

---

## Release artifacts

A release build produces:

- `CzatPythom.exe`
- `CzatPythom.exe.sha256`
- `CzatPythom-v2.0.0-Windows-x64.zip`
- `CzatPythom-v2.0.0-Windows-x64.zip.sha256`

The EXE is smoke-tested with `--version` before publication.

---

## Author

Developed by **Swir** — [github.com/Swir](https://github.com/Swir)

<div align="center">

### by Swir ⚡

</div>
