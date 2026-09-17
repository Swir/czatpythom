# Security

## GitHub token handling

CzatPythom never requires a token in source code or in `config.json`.

For GitHub-backed chat, set the token only in the process environment:

```powershell
$env:CZATPYTHOM_GITHUB_TOKEN = "github_pat_..."
$env:CZATPYTHOM_REPOSITORY = "owner/private-chat-data"
$env:CZATPYTHOM_BACKEND = "github"
```

Use a fine-grained token restricted to the single repository used for chat storage and grant only the repository contents permission required to read/write the configured room JSON files.

## Privacy

GitHub-backed chat messages are ordinary repository content. A public repository means public chat history. Use a private repository for conversations that should not be public. Do not use this project to exchange passwords, API keys, recovery codes or other secrets.

The local backend stores room JSON under the current user's application-data/config directory and is intended for local testing or single-device use.

## Message deletion

CzatPythom 2.1 restores the legacy `/clean` capability because it was part of the original client, but it is no longer a blind one-key destructive action:

- `/clear` only clears the local terminal screen.
- `/clean` clears messages only in the currently selected room.
- `/clean` always asks for explicit confirmation first.
- On the GitHub backend, the clear operation is limited to the configured room JSON path in the configured repository and uses conflict retries.

Treat `/clean` as irreversible history deletion and keep repository backups if chat history is important.

## Reporting

If you find a vulnerability, report it privately to the repository owner rather than publishing working exploit details in a public issue.
