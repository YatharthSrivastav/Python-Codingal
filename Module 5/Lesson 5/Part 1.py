from Config import HF_API_KEY
import requests, base64, os, re, time
from PIL import Image
from colorama import init, Fore, Style

init(autoreset=True)

ROUTER_URL = "https://router.huggingface.co/v1/chat/completions"
HEADERS = {"Authorization": f"Bearer {HF_API_KEY}", "Content-Type": "application/json"}
VISION_MODELS = [

"moonshotai/Kimi-K2.6:novita",

"meta-llama/Llama-4-Maverick-17B-128E-Instruct:sambanova",

"meta-llama/Llama-3.2-11B-Vision-Instruct:sambanova",

]

TEXT_MODELS = [

"Qwen/Qwen2.5-7B-Instruct:together",

"Qwen/Qwen2.5-14B-Instruct:together",

"Qwen/Qwen2.5-32B-Instruct:together",

"mistralai/Mistral-7B-Instruct-v0.3:together",

"mistralai/Mixtral-8x7B-Instruct-v0.1:together",
]

def query_hf_api(payload: dict):
    try:
        r = requests.post(ROUTER_URL, headers=HEADERS, json=payload, timeout=120)
    except requests.RequestException as e:
        return None, f"Request Failed {e}"
    if r.status_code != 200:
        try:
            j = r.json()
            msg = j.get("error", {}).get("message") or str(j)
        except Exception:
            msg = (r.text or "").strip() or r.reason or "Request Failed"
            return None, f"Status {r.status_code}: {msg}"
    try:
        return r.json(), None
    except Exception:
        return None, "Non JSON Response"

def data_url(path: str) -> str:
    with open(path, "rb") as f:
        return "data:image/jpeg;base64," + base64.b64encode(f.read()).decode("utf-8")

def get_basic_caption(image_path: str) -> str:
    print(f"{Fore.YELLOW} Generating basic caption...")
    msgs = [{
        "role": "user",
        "content": [
            {"type": "text", "text": "Write one complete sentence describing the image"},
            {"type": "image_url", "image_url": {"url":data_url(image_path)}},
        ],
    }]
    #cap, err = _run_models(VISION_MODELS, msgs, max_tokens=90, temparature=0.2)
    #return cap if cap else f"Error: {err}"

    