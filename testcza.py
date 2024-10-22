import requests
import json
import time
import random
import string
from colorama import Fore, init, Style
import threading
import base64
from datetime import datetime
import os
import sys

# Inicjalizacja kolorów w konsoli
init(autoreset=True)

# URL do plików JSON na GitHubie
GITHUB_API_MESSAGES_URL = "https://api.github.com/repos/YourUser/czatpythom/contents/messages.json"

# Token GitHub (przywróć klucz)
GITHUB_TOKEN = "github_pat_KEYS"

# Lista dostępnych kolorów (nazwy)
COLOR_NAMES = ['GREEN', 'BLUE', 'RED', 'YELLOW', 'MAGENTA', 'CYAN', 'LIGHTGREEN_EX', 'LIGHTRED_EX', 'LIGHTBLUE_EX']

# Mapowanie nazw kolorów na kody z biblioteki colorama
COLOR_MAP = {
    'GREEN': Fore.GREEN,
    'BLUE': Fore.BLUE,
    'RED': Fore.RED,
    'YELLOW': Fore.YELLOW,
    'MAGENTA': Fore.MAGENTA,
    'CYAN': Fore.CYAN,
    'LIGHTGREEN_EX': Fore.LIGHTGREEN_EX,
    'LIGHTRED_EX': Fore.LIGHTRED_EX,
    'LIGHTBLUE_EX': Fore.LIGHTBLUE_EX
}

# Funkcja pobierająca dane z pliku JSON na GitHubie za pomocą API
def get_json_from_github(api_url):
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Cache-Control": "no-cache"
    }
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Sprawdza, czy kod odpowiedzi to 200
        content = response.json()["content"]
        return json.loads(base64.b64decode(content).decode('utf-8'))
    except requests.exceptions.RequestException as e:
        print(f"Błąd pobierania danych: {e}")
        return []

# Funkcja pobierająca SHA pliku JSON z GitHub
def get_sha_from_github(api_url):
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}"
    }
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        return response.json()["sha"]
    except requests.exceptions.RequestException as e:
        print(f"Błąd pobierania SHA: {e}")
        return None

# Funkcja zapisująca dane do pliku JSON na GitHubie (zakodowane w Base64)
def save_json_to_github(api_url, data, sha):
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}"
    }

    # Kodowanie danych do Base64
    json_data = json.dumps(data, indent=2).encode('utf-8')
    encoded_content = base64.b64encode(json_data).decode('utf-8')

    payload = {
        "message": "Update JSON",
        "content": encoded_content,
        "sha": sha
    }

    try:
        put_response = requests.put(api_url, headers=headers, json=payload)
        put_response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Błąd zapisu danych: {e}")

# Funkcja zapisująca wiadomości
def save_message(new_message):
    try:
        # Pobranie SHA istniejącego pliku
        sha = get_sha_from_github(GITHUB_API_MESSAGES_URL)

        if sha:
            # Pobranie istniejących wiadomości
            messages = get_json_from_github(GITHUB_API_MESSAGES_URL)
            messages.append(new_message)
            # Zapisanie wszystkich wiadomości (starych + nowych) do GitHub
            save_json_to_github(GITHUB_API_MESSAGES_URL, messages, sha)

    except requests.exceptions.RequestException as e:
        print(f"Błąd podczas zapisu wiadomości: {e}")

# Funkcja czyszcząca wiadomości
def clean_messages():
    try:
        # Pobranie SHA istniejącego pliku
        sha = get_sha_from_github(GITHUB_API_MESSAGES_URL)

        if sha:
            # Czyszczenie listy wiadomości (zapisujemy pustą listę)
            save_json_to_github(GITHUB_API_MESSAGES_URL, [], sha)
            print("Wiadomości zostały wyczyszczone.")

            # Wyczyszczenie ekranu w konsoli
            print("\033[H\033[J", end="")  # Komenda do czyszczenia ekranu w terminalu

    except requests.exceptions.RequestException as e:
        print(f"Błąd podczas czyszczenia wiadomości: {e}")

# Funkcja logowania lub generowania losowego użytkownika
def login_or_guest():
    choice = input("Wpisz swój login (lub wciśnij Enter, aby wygenerować losowy nick): ").strip()

    if not choice:  # Jeśli nic nie wpisano, generujemy losowy nick
        username = "Gość_" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    else:
        username = choice

    nick_color_name = choose_color("nick")
    text_color_name = choose_color("text")
    return username, nick_color_name, text_color_name

# Funkcja do wyboru koloru nicka i tekstu
def choose_color(item):
    print(f"Wybierz kolor dla {item}:")
    for i, color_name in enumerate(COLOR_NAMES, 1):
        print(f"{i} - {COLOR_MAP[color_name]}{color_name}")
    choice = input("Twój wybór: ")

    try:
        index = int(choice) - 1
        if 0 <= index < len(COLOR_NAMES):
            return COLOR_NAMES[index]
        else:
            print(f"Nieprawidłowy wybór, domyślnie ustawiono 'GREEN' dla {item}.")
            return 'GREEN'
    except (ValueError, IndexError):
        print(f"Nieprawidłowy wybór, domyślnie ustawiono 'GREEN' dla {item}.")
        return 'GREEN'

# Funkcja do wysyłania wiadomości
def send_message(username, nick_color_name, text_color_name):
    nick_color = COLOR_MAP[nick_color_name]
    text_color = COLOR_MAP[text_color_name]

    while True:
        # Teraz wyświetlamy użytkownikowi jego wiadomość w odpowiednim kolorze
        message = input(f"{nick_color}{username}{Fore.RESET}: {text_color}")

        # Unikamy wysyłania pustych wiadomości
        if message.strip() == "":
            print("Nie można wysłać pustej wiadomości.")
            continue

        if message.lower() == '/clean':
            clean_messages()
        elif message.lower() == 'quit':
            print("Zakończono sesję.")
            break
        else:
            # Dodajemy nową wiadomość
            new_message = {
                'username': username,
                'message': message,
                'nick_color': nick_color_name,  # Przechowujemy nazwę koloru dla nicka
                'text_color': text_color_name,  # Przechowujemy nazwę koloru dla tekstu
                'timestamp': time.time()  # Ustawienie bieżącego timestampu
            }

            # Zapisz na GitHub
            save_message(new_message)

# Funkcja do formatowania daty
def format_timestamp(timestamp):
    try:
        return datetime.fromtimestamp(timestamp).strftime("%d.%m %H:%M")
    except Exception as e:
        print(f"Błąd formatowania daty: {e}")
        return "Błędna data"

# Funkcja wyświetlania wiadomości z dopasowaną ramką i dwoma kolorami (nick i tekst)
def typing_effect(nick_color, text_color, message, username, timestamp):
    # Obliczamy szerokość wiadomości i dopasowujemy ramkę
    message_length = len(f"[{username}] {message}") + 2  # Dodatkowe miejsce na ramkę
    message_length = max(50, message_length)  # Ustawiamy minimalną szerokość ramki (50)

    # Dodajemy ramki wokół wiadomości z odpowiednim kolorem
    print(nick_color + "╔" + "═" * message_length + "╗")  # Górna linia
    sys.stdout.write(f"║ [{nick_color}{username}{Fore.RESET} - {timestamp}]: ")  # Treść nicka z ramką i czasem
    sys.stdout.write(f"{text_color}{message}{Fore.RESET} ║\n")  # Treść wiadomości w kolorze tekstu
    print(nick_color + "╚" + "═" * message_length + "╝")  # Zakończenie wiadomości w kolorze nicka

# Funkcja do odbierania wiadomości (ciągłe odświeżanie co 3 sekundy)
def receive_messages(username):
    last_seen_message = 0

    while True:
        time.sleep(3)  # Odświeżanie wiadomości co 3 sekundy
        messages = get_json_from_github(GITHUB_API_MESSAGES_URL)

        # Jeśli są nowe wiadomości, wyświetl tylko te, które są nowe
        if len(messages) > last_seen_message:
            new_messages = messages[last_seen_message:]

            # Wyświetl nowe wiadomości
            for msg in new_messages:
                formatted_time = format_timestamp(msg['timestamp'])
                
                # Sprawdzanie, czy wiadomość ma pola 'nick_color' i 'text_color'
                nick_color_name = msg.get('nick_color', 'GREEN')  # Domyślnie zielony, jeśli nie ma
                text_color_name = msg.get('text_color', 'WHITE')  # Domyślnie biały, jeśli nie ma
                
                nick_color = COLOR_MAP.get(nick_color_name, Fore.GREEN)  # Pobranie kodu koloru dla nicka
                text_color = COLOR_MAP.get(text_color_name, Fore.WHITE)  # Pobranie kodu koloru dla tekstu
                formatted_message = f"{msg['message']}"

                # Jeśli wiadomość pochodzi od siebie, pomiń ją
                if msg['username'] == username:
                    continue

                # Efekt pisania lub proste wyświetlanie wiadomości z ramkami
                typing_effect(nick_color, text_color, formatted_message, msg['username'], formatted_time)

            # Zaktualizuj licznik wiadomości
            last_seen_message = len(messages)

# Funkcja uruchamiająca czat w osobnych wątkach
def run_chat(username, nick_color_name, text_color_name):
    # Wątek do odbierania wiadomości (w tle)
    receive_thread = threading.Thread(target=receive_messages, args=(username,), daemon=True)
    receive_thread.start()

    # Wysyłanie wiadomości (w głównym wątku)
    send_message(username, nick_color_name, text_color_name)

if __name__ == '__main__':
    # Logowanie lub wejście jako gość
    username, nick_color_name, text_color_name = login_or_guest()

    nick_color = COLOR_MAP[nick_color_name]
    print(f"Twoja nazwa użytkownika to: {nick_color}{username}{Fore.RESET}")

    # Uruchomienie czatu
    run_chat(username, nick_color_name, text_color_name)
