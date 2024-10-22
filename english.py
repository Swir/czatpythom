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

# Initialize colorama for console coloring
init(autoreset=True)

# GitHub API configuration
GITHUB_API_MESSAGES_URL = "https://api.github.com/repos/Swir/czatpythom/contents/messages.json"
GITHUB_TOKEN = "YOUR_GITHUB_TOKEN"  # Replace with your actual GitHub token

# Available colors for user nicknames and messages
COLOR_NAMES = ['GREEN', 'BLUE', 'RED', 'YELLOW', 'MAGENTA', 'CYAN', 'LIGHTGREEN_EX', 'LIGHTRED_EX', 'LIGHTBLUE_EX']
COLOR_MAP = {
    'GREEN': Fore.GREEN, 'BLUE': Fore.BLUE, 'RED': Fore.RED, 'YELLOW': Fore.YELLOW,
    'MAGENTA': Fore.MAGENTA, 'CYAN': Fore.CYAN, 'LIGHTGREEN_EX': Fore.LIGHTGREEN_EX,
    'LIGHTRED_EX': Fore.LIGHTRED_EX, 'LIGHTBLUE_EX': Fore.LIGHTBLUE_EX
}

# Fetch JSON data from GitHub
def get_json_from_github(api_url):
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Cache-Control": "no-cache"}
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Check if status code is 200
        content = response.json()["content"]
        return json.loads(base64.b64decode(content).decode('utf-8'))
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

# Get the SHA of the file for updates
def get_sha_from_github(api_url):
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        return response.json()["sha"]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching SHA: {e}")
        return None

# Save JSON data to GitHub
def save_json_to_github(api_url, data, sha):
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    json_data = json.dumps(data, indent=2).encode('utf-8')
    encoded_content = base64.b64encode(json_data).decode('utf-8')

    payload = {"message": "Update JSON", "content": encoded_content, "sha": sha}
    try:
        put_response = requests.put(api_url, headers=headers, json=payload)
        put_response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error saving data: {e}")

# Save message to GitHub
def save_message(new_message):
    try:
        sha = get_sha_from_github(GITHUB_API_MESSAGES_URL)
        if sha:
            messages = get_json_from_github(GITHUB_API_MESSAGES_URL)
            messages.append(new_message)
            save_json_to_github(GITHUB_API_MESSAGES_URL, messages, sha)
    except requests.exceptions.RequestException as e:
        print(f"Error saving message: {e}")

# Clear messages
def clean_messages():
    try:
        sha = get_sha_from_github(GITHUB_API_MESSAGES_URL)
        if sha:
            save_json_to_github(GITHUB_API_MESSAGES_URL, [], sha)
            print("Messages cleared.")
            print("\033[H\033[J", end="")  # Clears terminal screen
    except requests.exceptions.RequestException as e:
        print(f"Error clearing messages: {e}")

# User login or guest generation
def login_or_guest():
    choice = input("Enter your login (or press Enter for a random nickname): ").strip()
    username = choice if choice else "Guest_" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    nick_color_name = choose_color("nickname")
    text_color_name = choose_color("text")
    return username, nick_color_name, text_color_name

# Choose color for nickname or text
def choose_color(item):
    print(f"Choose a color for your {item}:")
    for i, color_name in enumerate(COLOR_NAMES, 1):
        print(f"{i} - {COLOR_MAP[color_name]}{color_name}")
    choice = input("Your choice: ")
    try:
        index = int(choice) - 1
        return COLOR_NAMES[index] if 0 <= index < len(COLOR_NAMES) else 'GREEN'
    except (ValueError, IndexError):
        print(f"Invalid choice, defaulting to 'GREEN'.")
        return 'GREEN'

# Send message
def send_message(username, nick_color_name, text_color_name):
    nick_color = COLOR_MAP[nick_color_name]
    text_color = COLOR_MAP[text_color_name]
    while True:
        sys.stdout.write(f"{nick_color}{username}{Fore.RESET}: {text_color}")
        sys.stdout.flush()
        message = input()
        if not message.strip():
            print("Cannot send an empty message.")
            continue
        if message.lower() == '/clean':
            clean_messages()
        elif message.lower() == 'quit':
            print("Session ended.")
            break
        else:
            new_message = {
                'username': username, 'message': message,
                'nick_color': nick_color_name, 'text_color': text_color_name,
                'timestamp': time.time()
            }
            save_message(new_message)

# Format timestamp
def format_timestamp(timestamp):
    try:
        return datetime.fromtimestamp(timestamp).strftime("%d.%m %H:%M")
    except Exception as e:
        print(f"Date formatting error: {e}")
        return "Invalid date"

# Typing effect with formatted borders and colors
def typing_effect(nick_color, text_color, message, username, timestamp):
    message_length = max(50, len(f"[{username}] {message}") + 2)  # Minimum width of 50 characters
    print(nick_color + "╔" + "═" * message_length + "╗")
    sys.stdout.write(f"║ [{nick_color}{username}{Fore.RESET} - {timestamp}]: ")
    sys.stdout.write(f"{text_color}{message}{Fore.RESET} ║\n")
    print(nick_color + "╚" + "═" * message_length + "╝")

# Receive messages
def receive_messages(username):
    last_seen_message = 0
    while True:
        time.sleep(3)
        messages = get_json_from_github(GITHUB_API_MESSAGES_URL)
        if len(messages) > last_seen_message:
            new_messages = messages[last_seen_message:]
            for msg in new_messages:
                if msg['username'] == username:
                    continue
                formatted_time = format_timestamp(msg['timestamp'])
                nick_color = COLOR_MAP.get(msg.get('nick_color', 'GREEN'), Fore.GREEN)
                text_color = COLOR_MAP.get(msg.get('text_color', 'WHITE'), Fore.WHITE)
                typing_effect(nick_color, text_color, msg['message'], msg['username'], formatted_time)
            last_seen_message = len(messages)

# Run chat
def run_chat(username, nick_color_name, text_color_name):
    receive_thread = threading.Thread(target=receive_messages, args=(username,), daemon=True)
    receive_thread.start()
    send_message(username, nick_color_name, text_color_name)

# Main entry point
if __name__ == '__main__':
    username, nick_color_name, text_color_name = login_or_guest()
    print(f"Your username is: {COLOR_MAP[nick_color_name]}{username}{Fore.RESET}")
    run_chat(username, nick_color_name, text_color_name)
