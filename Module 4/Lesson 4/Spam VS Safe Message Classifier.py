import requests
import os
from dotenv import load_dotenv
load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")
MODEL_ID = "facebook/bart-large-mnli"
API_URL = f"https://router.huggingface.co/hf-inference/models/{MODEL_ID}"
HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}
LABELS = ["Spam","Safe"]



def classify_message(message):
    payload = {"inputs": message, "parameters": {"candidate_labels": LABELS}}
    response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=30)
    if not response.ok:
        raise RuntimeError(f"API Error: {response.status_code}")
    data = response.json()
    results = [(item["label"], item["score"]) for item in data]
    return sorted(results, key=lambda x: x[1], reverse=True)

def show_results(message, results):
    label, score = results[0]

    print("\n" + "=" * 44)
    print("Spam vs Safe Message Classifier")
    print("=" * 44)
    print(f"Message: {message}")
    print(f"Result: {label} ({score*100:.1f}%)\n")
    print("Confidence scores:")

    for i, (lbl, scr) in enumerate(results, 1):
        print(f"{i}. {lbl}: {scr*100:.1f}%")

    if label == "Spam":
        print("\nWarning: Don't click links or share personal info!")
    else:
        print("\nLooks safe, but always stay alert!")
    print("=" * 44)

def main():
    print("Spam vs Safe Message Classifier")
    print("Type 'exit' to quit\n")
    while True:
        msg = input("Enter message: ").strip()
        if msg.lower() == "exit":
            print("Goodbye!")
            break

        if not msg:
            print("Please enter a message!\n")
            continue

        try:
            results = classify_message(msg)
            show_results(msg, results)
        except Exception as e:
            print(f"\n Error: {e}")
            print("Check your API key and internet connection\n")

if __name__ == "__main__":
    main()
