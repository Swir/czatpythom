import requests
import json
import time
import random
import string
from colorama import Fore, init
import threading
import base64
from datetime import datetime
import os

# Inicjalizacja kolorów w konsoli
init(autoreset=True)

# URL do plików JSON na GitHubie
GITHUB_RAW_MESSAGES_URL = "https://raw.githubusercontent.com/Swir/czatpythom/main/messages.json"
GITHUB_API_MESSAGES_URL = "https://api.github.com/repos/Swir/czatpythom/contents/messages.json"

# Token GitHub (umieszczony bezpośrednio w kodzie)
GITHUB_TOKEN = "github_pat_KEY"

# Globalna lista wiadomości, aby przechowywać lokalną kopię wiadomości
local_messages = []

# Funkcja pobierająca dane z pliku JSON na GitHubie
def get_json_from_github(raw_url):
    try:
        response = requests.get(raw_url, headers={"Cache-Control": "no-cache"})
        response.raise_for_status()  # Sprawdza, czy kod odpowiedzi to 200
        return json.loads(response.text)
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
def save_messages():
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}"
    }

    try:
        # Pobranie SHA istniejącego pliku
        sha = get_sha_from_github(GITHUB_API_MESSAGES_URL)
        
        if sha:
            # Zapisanie wszystkich wiadomości (starych + nowych) do GitHub
            save_json_to_github(GITHUB_API_MESSAGES_URL, local_messages, sha)

    except requests.exceptions.RequestException as e:
        print(f"Błąd podczas zapisu wiadomości: {e}")

# Funkcja do czyszczenia wiadomości
def clean_messages():
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}"
    }

    try:
        # Pobranie SHA istniejącego pliku
        sha = get_sha_from_github(GITHUB_API_MESSAGES_URL)
        
        if sha:
            # Czyszczenie listy wiadomości (zapisujemy pustą listę)
            save_json_to_github(GITHUB_API_MESSAGES_URL, [], sha)
            print("Wiadomości zostały wyczyszczone.")

            # Wyczyszczenie lokalnej kopii wiadomości
            global local_messages
            local_messages.clear()

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
    
    color = choose_color()
    return username, color

# Funkcja do wyboru koloru nicka
def choose_color():
    print("Wybierz kolor nicka:")
    print("1 - Zielony, 2 - Niebieski, 3 - Czerwony, 4 - Żółty, 5 - Magenta, 6 - Cyjan")
    choice = input("Twój wybór: ")

    if choice == '1':
        return Fore.GREEN
    elif choice == '2':
        return Fore.BLUE
    elif choice == '3':
        return Fore.RED
    elif choice == '4':
        return Fore.YELLOW
    elif choice == '5':
        return Fore.MAGENTA
    elif choice == '6':
        return Fore.CYAN
    else:
        print("Nieprawidłowy wybór, domyślnie ustawiono zielony.")
        return Fore.GREEN

# Funkcja do wysyłania wiadomości
def send_message(username, color):
    global local_messages

    while True:
        message = input(f"{color}{username}: ")

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
            # Dodajemy nową wiadomość do listy
            new_message = {
                'username': username,
                'message': message,
                'color': color,
                'timestamp': time.time()  # Ustawienie bieżącego timestampu
            }

            # Dodaj nową wiadomość do lokalnej kopii
            local_messages.append(new_message)
            # Zapisz na GitHub
            save_messages()

# Funkcja do formatowania daty
def format_timestamp(timestamp):
    try:
        return datetime.fromtimestamp(timestamp).strftime("%d.%m %H:%M")
    except Exception as e:
        print(f"Błąd formatowania daty: {e}")
        return "Błędna data"

# Funkcja wyświetlająca profesjonalny licznik odliczania do odświeżania w prawym górnym rogu
def countdown(seconds):
    while seconds:
        # Przesuń kursor do prawego górnego rogu
        print(f"\033[s\033[1;60HOdświeżenie za {seconds} sekundy...\033[u", end='')
        time.sleep(1)
        seconds -= 1
    # Po odliczeniu wyświetl informację o odświeżaniu
    print(f"\033[s\033[1;60HOdświeżanie wiadomości...          \033[u", end='')

# Funkcja do odbierania wiadomości (ciągłe odświeżanie co 3 sekundy)
def receive_messages():
    global local_messages
    last_seen_message = 0

    while True:
        countdown(3)  # Profesjonalny licznik do odświeżania
        messages = get_json_from_github(GITHUB_RAW_MESSAGES_URL)

        # Zaktualizuj lokalną kopię wiadomości (local_messages)
        if isinstance(messages, list):
            local_messages = messages

        # Jeśli są nowe wiadomości, wyświetl tylko te, które są nowe
        if len(messages) > last_seen_message:
            new_messages = messages[last_seen_message:]

            # Wyświetl nowe wiadomości
            for msg in new_messages:
                formatted_time = format_timestamp(msg['timestamp'])
                print(f"{msg['color']}[{formatted_time}] {msg['username']}: {msg['message']}")
            
            # Zaktualizuj licznik wiadomości
            last_seen_message = len(messages)

# Funkcja uruchamiająca czat w osobnych wątkach
def run_chat(username, color):
    # Wątek do odbierania wiadomości (w tle)
    receive_thread = threading.Thread(target=receive_messages, daemon=True)
    receive_thread.start()

    # Wysyłanie wiadomości (w głównym wątku)
    send_message(username, color)

if __name__ == '__main__':
    # Logowanie lub wejście jako gość
    username, color = login_or_guest()

    print(f"Twoja nazwa użytkownika to: {color}{username}")

    # Uruchomienie czatu
    run_chat(username, color)
