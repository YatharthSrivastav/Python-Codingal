import time
import requests
from PIL import Image, ImageDraw, ImageFont
import io
import os, mimetypes
from dotenv import load_dotenv
load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")

MODEL = "facebook/detr-resnet-101"
API = f"https://router.huggingface.co/hf-inference/models/{MODEL}"
ALLOWED, MAX_MB = {".png", ".jpg", ".gif", ".webp"}, 8
EMOJI = {{"person":"🧍","car":"🚗","truck":"🚚","bus":"🚌","bicycle":"🚲","motorcycle":"🏍️","dog":"🐶","cat":"🐱",

    "bird":"🐦","horse":"🐴","sheep":"🐑","cow":"🐮","bear":"🐻","giraffe":"🦒","zebra":"🦓","banana":"🍌",

    "apple":"🍎","orange":"🍊","pizza":"🍕","broccoli":"🥦","book":"📘","laptop":"💻","tv":"📺","bottle":"🧴","cup":"🥤"}}

def font(sz = 18):
    for font in ("DejaVuSans.ttf", "arial.ttf"):
        try:
            return ImageFont.truetype(font, sz)
        except:
            pass
    return ImageFont.load_default()

def ask_image():
    print("\nPick an image (PNG/JPG/GIF/WEBP < 8MB) from this folder")
    while True:
        p = input("Image path: ").strip().strip('"').strip('"')
        if not p or not os.path.isfile(p):
            print("Not Found")
            continue
        if os.path.splitext(p)[1].lower() not in ALLOWED:
            print("Unsupported format")
            continue
        if os.path.getsize(p) / (1024 * 1024) > MAX_MB:
            print("Too big (> 8MB)")
            continue
        try:
            Image.open(p).verify()
        except:
            print("Corrupted Image")
            continue
        return p

""""def infer(path, img_bytes, tries = 8):
    mime, _ = mimetypes.guess_type(path)
    for _ in range(tries):"""