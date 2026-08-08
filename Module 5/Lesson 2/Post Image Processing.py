import time 
import requests
from PIL import Image, ImageEnhance, ImageFilter
from io import BytesIO
import os
from dotenv import load_dotenv
load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")
print(HF_API_KEY)
MODELS = [ 
    "black-forest-labs/FLUX.1-schnell",
    "stabilityai/stable-diffusion-xl-base-1.0",
    "stable-diffusion-v1-5/stable-diffusion-v1-5",
    "CompVis/stable-diffusion-v1-4",
]

HEADERS = {"Authorization": f"Bearer {HF_API_KEY}", "Accept": "image/png"}
def generate_image(prompt):
    payload, last_err = {"inputs": prompt}, None
    for model in MODELS:
        url = f"https://router.huggingface.co/hf-inference/models/{model}"

        for _ in range(3):
            r = requests.post(url, headers=HEADERS, json=payload, timeout=120)
            ct = (r.headers.get("content-type") or "").lower()

            if r.status_code == 503 and "application/json" in ct:
                try:
                    wait_s = int(r.json().get("estimated_time"), 5)
                except Exception:
                    wait_s = 5
                time.sleep(wait_s + 1)
                continue

            if r.status_code == 200 and "application/json" not in ct:
                try: 
                    return  Image.open(BytesIO(r.content)).convert("RGB")
                except Exception as e:
                    last_err = f"Request failed with status code 200: Couldn't decode image bytes {e}"
                    break

            try:
                body = r.json() if "application/json" in ct else r.text
            except Exception:
                body = r.text
            last_err = f"Request failed with status code {r.status_code}: {body}"
            break

    raise Exception(last_err or "Request failed with status code 500: Unknown Error")

def post_process(image):
    image = ImageEnhance.Brightness(image).enhance(1.2)
    image = ImageEnhance.Contrast(image).enhance(1.3)
    return image.filter(ImageFilter.GaussianBlur(radius=2))

def main():
    print("Welcome to Post Processing Image Workshop!")
    print("This program generates an image from text and applies post processing effects to it.")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("Enter a description for the image or type 'exit' to quit the application:\n")
        if user_input.lower() == "exit":
            print("Bye!")
            break
        try:
            print("\nGenerating Image...")
            image = generate_image(user_input)
            print("Appling post processing effects...\n")
            processed_image = post_process(image)
            processed_image.show()
            save = input("Do you want to save the image? (y/n): ").strip().lower()
            if save == "y":
                file_name = input("Enter a name for the file (without extension): ").strip()
                processed_image.save(f"{file_name}.png")
                print(f"Image saved as {file_name}.png\n")
            print("-" * 80 + "\n")
        except Exception as e:
            print(f"Error: {e}\n")

if __name__ == "__main__":
    main()