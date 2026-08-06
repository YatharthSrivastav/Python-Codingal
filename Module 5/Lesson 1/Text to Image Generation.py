from huggingface_hub import InferenceClient
from datetime import datetime
from PIL import Image
from Config1 import HF_API_KEY

MODELS = [
"ByteDance/SDXL-Lightning",
"stabilityai/stable-diffusion-xl-base-1.0",
"stabilityai/sdxl-turbo",
"runwayml/stable-diffusion-v1-5",
]

client = InferenceClient(api_key=HF_API_KEY)

print(f"Primary Model:{MODELS[0]}")
print("Type quit or q or exit to exit\n")

while True:
    prompt = input("Type: ").strip()
    if prompt.lower() in ["quit", "q", "exit"]:
        break
    if not prompt:
        continue
    print("Generating...")
    image = None

    for model in MODELS:
        try:
            image = client.text_to_image(prompt, model=model)
        
        except Exception as e:
            print(f"\nModel {model} failed")
            print(f"Reason: {e}\n")
            continue
    if image:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"image_{timestamp}.png"
        image.save(filename)
        print(f"Saved as {filename}")
        image.show()
        print()
    else:
        print("Error: All models failed!")
print("Bye")