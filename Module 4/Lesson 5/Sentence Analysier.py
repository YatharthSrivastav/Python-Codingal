import requests, re, random

from Config1 import HF_API_KEY

MODEL="sentence-transformers/all-MiniLM-L6-v2"

API=f"https://router.huggingface.co/hf-inference/models/{MODEL}"

HEAD={"Authorization":f"Bearer {HF_API_KEY}"}

TH=0.72

DEMOS=[("how to delete my account","how do i remove my account"),

("start the game","begin the game"),

("nearest hospital to me","closest clinic near me"),

("mobile games are getting bigger in size","game size on phones is increasing"),

("is it going to rain today","today is rainy"),

("reset my password","change my password")]

TOK=lambda s:" | ".join(s.split())

bar=lambda s:"█"*int(s*10)+"░"*(10-int(s*10))

clean=lambda t:[w for w in (re.sub(r"[^a-z0-9']+","",x.lower()) for x in t.split()) if w]

nums=lambda t:set(re.findall(r"\d+(?:\.\d+)?", t))

has_any=lambda t,arr:any(a in set(clean(t)) for a in arr)

def hf(q1, q2):
    r = requests.post(API, headers=HEAD, json={"inputs": {"source_sentence": q1, "sentences": [q2]}}, timeout=30)
    if not r.ok:
        raise RuntimeError(r.text)
    data = r.json()
    if isinstance(data, dict):
        raise RuntimeError(data.get("error", str(data)))
    return float(data[0])

def smart_score(base, q1, q2, strong):
    w1 = {w for w in clean(q1) if len(w) >=4}; w2 = {w for w in clean(q2) if len(w) >=4}
    jac = len(w1&w2)/max(1, len(w1|w2))
    boost = (0.04 if len(strong) >=2 else 0) + (0.03 if jac >= 0.20 else 0) + (0.05 if jac >= 0.35 else 0)
    negA=["not","no","never","without","can't","cant","cannot","don't","dont","won't","wont","n't"]

    oppA=[("increase","decrease"),("bigger","smaller"),("more","less"),("add","remove"),("open","close"),("enable","disable")]
    num_pen = 0.10 if (nums(q1)) and nums(q2) and nums(q1) != nums(q2) else 0
    neg_pen = 0.12 if has_any(q1, negA) != has_any(q2, negA) else 0
    opp_pen = 0.12 if any((has_any(q1, [a]) and has_any(q2, [b])) or (has_any(q1, [b]) and has_any(q2, [a])) for a, b in oppA) else 0
    return max(0.0, min(1.0, base + boost - num_pen - neg_pen - opp_pen))

                          

