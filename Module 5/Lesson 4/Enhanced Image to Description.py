import base64
import os
import requests
from io import BytesIO
from PIL import Image
from Config import HF_API_KEY


API_URL = "https://router.huggingface.co/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Content-Type": "application/json"
}

MODEL = "google/gemma-4-31B-it:cerebras"


def extract_err(r: requests.Response) -> str:
    try:
        j = r.json()

        if isinstance(j, dict):
            error = j.get("error")

            if isinstance(error, dict):
                return error.get("message") or str(error)

            if error:
                return str(error)

        return str(j)

    except Exception:
        return (r.text or "").strip() or r.reason or "Request failed."


def caption_image(image_source):

    try:
        with Image.open(image_source) as img:
            img = img.convert("RGB")

        
            buffer = BytesIO()
            img.save(buffer, format="JPEG", quality=95)

            image_bytes = buffer.getvalue()

    except Exception as e:
        return None, f"Could not load/convert image: {e}"

  
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")


    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Describe this image clearly in one sentence."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 100
    }


    try:
        r = requests.post(
            API_URL,
            headers=HEADERS,
            json=payload,
            timeout=120
        )

    except requests.RequestException as e:
        return None, f"Request failed: {e}"


    if r.status_code != 200:
        return None, extract_err(r)


    try:
        data = r.json()

        caption = data["choices"][0]["message"]["content"].strip()

        if caption:
            return caption, None

        return None, "No caption found."

    except (KeyError, IndexError, TypeError, ValueError) as e:
        return None, f"Could not read API response: {e}"


def main():
    folder = input(
        "Enter the folder path containing images (default: images): "
    ).strip() or "images"

    
    if not os.path.isdir(folder):
        print(f"Error: The folder '{folder}' does not exist.")
        return


    image_extensions = {
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".bmp",
        ".webp"
    }

    image_files = [
        filename
        for filename in os.listdir(folder)
        if os.path.isfile(os.path.join(folder, filename))
        and os.path.splitext(filename)[1].lower() in image_extensions
    ]

    if not image_files:
        print(f"Error: No images were found in '{folder}'.")
        return

    captions = []

    print(f"\nFound {len(image_files)} image(s). Processing...\n")


    for filename in image_files:
        image_path = os.path.join(folder, filename)

        print(f"Processing: {filename}")

        caption, error = caption_image(image_path)

        if caption:
            print(f"Caption: {caption}\n")
            captions.append(f"{filename}: {caption}")

        else:
            print(f"Error: {error}\n")
            captions.append(f"{filename}: ERROR - {error}")


    with open("captions_summary.txt", "w", encoding="utf-8") as f:
        for item in captions:
            f.write(item + "\n")

    print("Done!")
    print("Captions saved to captions_summary.txt")


if __name__ == "__main__":
    main()
