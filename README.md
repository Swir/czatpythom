# Czat Konsolowy z Obsługą Kolorów | Console Chat with Color Support

## Opis projektu | Project Description

Ten projekt to czat konsolowy napisany w Pythonie, który wykorzystuje **API GitHub** do zapisywania i pobierania wiadomości z pliku JSON. Aplikacja działa w terminalu i pozwala na interakcję wielu użytkowników w czasie rzeczywistym. Każdy użytkownik może wybrać swój własny kolor nicka oraz tekstu wiadomości, co sprawia, że czat jest bardziej spersonalizowany i przyjazny wizualnie.

**Funkcje:**
- Logowanie za pomocą pseudonimu użytkownika lub wygenerowanego losowego nicka.
- Możliwość wyboru koloru nicka oraz tekstu.
- Automatyczne zapisywanie wiadomości na GitHubie przy użyciu JSON.
- Wyświetlanie wiadomości w konsoli z dopasowaną ramką w zależności od długości wiadomości.
- Automatyczne odświeżanie wiadomości co 3 sekundy, co zapewnia płynność komunikacji.
- Możliwość czyszczenia historii wiadomości komendą `/clean`.
- Zakończenie sesji czatu poprzez wpisanie komendy `quit`.

## Project Description | Opis projektu

This project is a console-based chat application written in Python, utilizing the **GitHub API** to save and retrieve messages stored in a JSON file. The application runs in the terminal and allows multiple users to interact in real-time. Each user can choose their own nickname and text color, providing a personalized and visually engaging chat experience.

**Features:**
- Login with a user-specified nickname or a randomly generated one.
- Ability to choose a color for the nickname and the message text.
- Automatically saves messages to GitHub using JSON.
- Displays messages in the console with dynamically adjusted message frames based on the message length.
- Automatically refreshes messages every 3 seconds for seamless communication.
- Option to clear the chat history using the `/clean` command.
- End the chat session by typing `quit`.

## Jak uruchomić | How to Run

1. Upewnij się, że masz zainstalowane Python 3 oraz bibliotekę `colorama` (możesz ją zainstalować za pomocą komendy: `pip install colorama`).
2. Skonfiguruj swój **GitHub API Token** oraz zaktualizuj URL do swojego pliku JSON w kodzie (parametry: `GITHUB_TOKEN` i `GITHUB_API_MESSAGES_URL`).
3. Uruchom program w terminalu za pomocą komendy: `python <nazwa_pliku>.py`.

## How to Run | Jak uruchomić

1. Ensure you have Python 3 installed and the `colorama` library (you can install it with: `pip install colorama`).
2. Set up your **GitHub API Token** and update the URL to your JSON file in the code (parameters: `GITHUB_TOKEN` and `GITHUB_API_MESSAGES_URL`).
3. Run the program in the terminal with the command: `python <file_name>.py`.

## Wymagania | Requirements

- Python 3.x
- Biblioteka `colorama`
- GitHub API Token do zapisywania i pobierania wiadomości

## Requirements | Wymagania

- Python 3.x
- `colorama` library
- GitHub API Token for saving and retrieving messages
