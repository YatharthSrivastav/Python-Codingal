import requests
from colorama import Fore, Style, init
init(autoreset=True)
import os
from dotenv import load_dotenv
load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")
DEFAULT_MODEL = "google/pegasus-xsum"

def build_api_url(model_name):
    return f"https://router.huggingface.co/hf-inference/models/{model_name}"

def query(payload, model_name = DEFAULT_MODEL):
    api_url = build_api_url(model_name)
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    try:
        response = requests.post(
            api_url,
            headers=headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        return None

def summarise_text(text, min_length, max_length, model_name = DEFAULT_MODEL):
    payload = {"inputs": text, "parameters": {"min_length": min_length, "max_length": max_length}}
    print(Fore.BLUE + Style.BRIGHT + f"\n?????Summarisation AI using {model_name} model")
    result = query(payload, model_name=model_name)
    if result is None:
        return None
    if isinstance(result, list) and result and "summary_text" in result[0]:
        return result[0]["summary_text"]
    else:
        print(Fore.RED + "Error: Summarisation Response", result)
        return None

if __name__ == "__main__":
    print(Fore.YELLOW + Style.BRIGHT + "???Hi! What is your name?")
    user_name = input("Your name is ").strip()
    if not user_name:
        user_name = "User"
    print(Fore.GREEN + Style.BRIGHT + f"Welcome {user_name}")
    print(Fore.YELLOW + Style.BRIGHT + "\nPLEASE ENTER THE TEXT YOU WANT TO SUMMARISE!")
    user_text = input("> ").strip()
    if not user_text:
        print(Fore.RED + "No text provided. Exiting.")
    else:
        print(Fore.YELLOW + "\nChoose your summarisation model: ")
        model_choice = input("Model name (leave blank for default model): ").strip()
        if not model_choice:
            model_choice = DEFAULT_MODEL
        print(Fore.YELLOW + "\nChoose your summarisation style:")
        print("1. Standard Summary (quick and concise)")
        print("2. Enhanced Summary (detailed and refined)")
        style_choice = input("Enter 1 or 2\n").strip()
        if style_choice == "2":
            min_length = 80
            max_length = 200
            print(Fore.BLUE + "Enhancing summarisation process...")
        else:
            min_length = 50
            max_length = 150
            print(Fore.BLUE + "Using standard summarisation settings...???")
        summary = summarise_text(user_text, min_length, max_length, model_name = model_choice)
        if summary:
            print(Fore.GREEN + Style.BRIGHT + f"\n???? AI Summarisation Output for {user_name}")
            print(Fore.GREEN + summary)
        else:
            print(Fore.RED + "Error: Failed to generate summary")
