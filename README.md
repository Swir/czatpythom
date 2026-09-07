<div align="center">

# 💬 Console Chat / Czat Konsolowy

**Colorful terminal chat backed by GitHub JSON storage**  
**Kolorowy czat terminalowy oparty na plikach JSON w GitHubie**

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![GitHub API](https://img.shields.io/badge/API-GitHub-181717?logo=github)
![Terminal](https://img.shields.io/badge/UI-Console-2ea44f)

</div>

---

## 🇵🇱 Polski

Projekt implementuje prosty czat konsolowy w Pythonie, który pobiera i zapisuje wiadomości w pliku `messages.json` przez GitHub Contents API. Interfejs korzysta z `colorama`, dzięki czemu użytkownik może wybrać kolor nicka i wiadomości.

### ✨ Funkcje
- własny nick lub automatyczny nick gościa
- 9 kolorów nicka i tekstu
- zapis oraz odczyt historii z GitHuba
- automatyczne odświeżanie wiadomości
- komenda `/clean` do wyczyszczenia historii
- komenda `quit` do zakończenia sesji
- kilka wersji klienta, w tym `english.py` i wersja beta konsolowa
- pliki JSON dla wiadomości, użytkowników i pokoi

### 🚀 Uruchomienie
```bash
git clone https://github.com/Swir/czatpythom.git
cd czatpythom
pip install requests colorama
python english.py
```

Przed uruchomieniem ustaw własny token GitHub w zmiennej `GITHUB_TOKEN` albo przenieś go do bezpiecznej konfiguracji środowiskowej.

### 🔐 Bezpieczeństwo
Nie commituj prawdziwego GitHub Personal Access Token do publicznego repozytorium. Token powinien mieć wyłącznie minimalne uprawnienia wymagane do aktualizacji odpowiedniego pliku/repozytorium.

---

## 🇬🇧 English

This project implements a lightweight Python console chat that reads and writes messages in `messages.json` through the GitHub Contents API. `colorama` provides customizable nickname and message colors.

### ✨ Features
- custom nickname or generated guest nickname
- 9 nickname/text color choices
- GitHub-backed message history
- automatic message refresh
- `/clean` command for clearing history
- `quit` command for ending a session
- multiple client variants including `english.py` and a beta console client
- JSON files for messages, users and rooms

### 🚀 Run
```bash
git clone https://github.com/Swir/czatpythom.git
cd czatpythom
pip install requests colorama
python english.py
```

Set your own GitHub token before use, preferably through environment-based configuration rather than hard-coding a real credential.

### 🔐 Security
Never commit a real GitHub Personal Access Token to a public repository. Grant only the minimum permissions needed for the target repository/file.

---

## 👤 Author / Autor
Developed by **Swir**.
