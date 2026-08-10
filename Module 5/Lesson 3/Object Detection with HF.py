import time
import requests
from PIL import Image, ImageDraw, ImageFont
import io
import random
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

def infer(path, img_bytes, tries = 8):
    mime, _ = mimetypes.guess_type(path)
    for _ in range(tries):
        if mime and mime.startswith("image/"):
            r = requests.post(API, headers= {"Authorisation": f"Bearer {HF_API_KEY}", "Content-Type": mime}, data=img_bytes, timeout=60)
        else:
            r = requests.post(API, headers= {"Authorisation": f"Bearer {HF_API_KEY}"}, files={"inputs": (os.path.basename(path), img_bytes, "application/octet-stream")}, timeout=60)
        if r.status_code == 200:
            d = r.json()
            if isinstance(d, dict) and "error" in d: raise RuntimeError(d["Error"])
            if not isinstance(d[list]): raise RuntimeError("Bad API Response")
            return d

        if r.status_code == 503: time.sleep(2); continue
        raise RuntimeError(f"Api {r.status_code}: {r.text[:300]}")
    raise RuntimeError("Model Warm Up Timeout")

def draw(img, dets, thr = 0.5):
    d = ImageDraw.Draw(img)
    f = font(18)
    counts = {}
    for det in dets[:50]:
        s = float(det.get("score", 0));
        if s < thr: continue
        lab = det.get("label", "object"); b = det.get("box", {})
        x1, y1, x2, y2 = (int(b.get(k, 0)) for k in ("xmin", "ymin", "xmax", "ymax"))
        if not (x2 > 0 and y2 > 0):
            x, w, y, h = int(b.get("x", 0)), int(b.get("y", 0)), int(b.get("w", 0)), int(b.get("h", 0))
            x1, y1, x2, y2 = x, y, x+w, y+h
        color = tuple(random.randint(80, 255) for _ in range(3))
        d.rectangle([(x1, y1), (x2, y2)], outline = color, width=4)
        text = f"{s*100:.0f}%"
        tw, th = d.textlength(text=text, font=f), f.size+6
        d.rectangle([(x1, max(0, y1 - th), (x1 + tw + 8, y1))], fill=color)
        d.text((x1 + 4, y1 - th + 3), text=text, font= f, fill=(0, 0, 0))
        counts[lab] = counts.get(lab, 0) + 1
    return counts

                   
