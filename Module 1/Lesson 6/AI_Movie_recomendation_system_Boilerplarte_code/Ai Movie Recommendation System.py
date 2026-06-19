import time, pandas as pd
from textblob import TextBlob
from colorama import init, Fore

# Init colors
init(autoreset=True)

# Load CSV (same error output)
try: df = pd.read_csv("Module 1\\Lesson 6\\AI_Movie_recomendation_system_Boilerplarte_code\\imdb_top_1000.csv")
except FileNotFoundError:
    print(Fore.RED + "Error: The file 'imdb_top_1000.csv' was not found."); raise SystemExit

# Unique genres
genres = sorted({g.strip() for xs in df["Genre"].dropna().str.split(", ") for g in xs})

def dots():
    """Prints ... with delay (AI thinking effect)."""
    for _ in range(3): print(Fore.YELLOW + ".", end="", flush=True); time.sleep(0.5)

def senti(p):
    """Polarity -> label."""
    return "Positive 😊" if p > 0 else "Negative 😞" if p < 0 else "Neutral 😐"

def recommend(genre=None, mood=None, rating=None, n=5):
    """Filter by genre/rating, shuffle, analyze Overview polarity, return n (title, polarity) or message."""
    d = df
    if genre: d = d[d["Genre"].str.contains(genre, case = False, na=False)]
    if rating is not None: d[d["IMDB_Rating"] >= rating]
    if d.empty: return "No suitable recommendations"
    d, need_nonneg, out = d.sample(frac = 1).reset_index(drop = True), bool(mood), []
    for _, r in d.iterrows():
        ov = r.get("Overview")
        if pd.isna(ov): continue
        pol = TextBlob(ov).sentiment.polarity

        if(not need_nonneg) or pol >= 0 :
            out.append((r["Series_Title"], pol))
            if len (out) == n: break
    return out if out else "No suitable movie recommendations"
            
    


def show(recs, name):
    """Print in same format: header + numbered 🎥 lines with polarity + senti()."""
    print(Fore.BLUE + f"AI analysed the recommendations for {name}")
    for i, (t, p) in enumerate (recs, 1):
        print(Fore.BLUE + "{i}.{t} (Polarity: {p:.2f}, {senti(p)})")

def get_genre():
    print(Fore.GREEN + "Genres: ", end = '')
    for i,g in enumerate(genres, 1): print(f"{Fore.GREEN}{i}. {g}")
    print()
    while True:
        x = input(Fore.YELLOW + "Enter the genre number or name: ").strip()
        if x.isdigit() and 1<= int(x) <= len(genres): 
            return genres[int(x) -1]
        x = x.title()
        if x in genres:
            return x
        print(Fore.GREEN + "Invalid input\n")

    
def get_rating():
    while True:
        x = input(Fore.YELLOW + "Enter a rating from 7.6 to 9.3 or skip").strip()
        if x.lower() == 'skip':
            return None
        try:
            r = float(x)
            if 7.6 <= r <= 9.3:
                return r 
            print(Fore.YELLOW + "Rating out of range\n")
        except ValueError:
            print(Fore.YELLOW + "Invalid Input")

            
print(Fore.YELLOW + "Welcome to your movie recommendation assistant")
name = input(Fore.YELLOW + "What is your name").strip()
print(Fore.YELLOW + f"Nice to meet you {name}\n")
print(Fore.YELLOW + "Lets find you your watch for today")

genre = get_genre()
mood = input(Fore.YELLOW + "How are you feeling today?\n").strip()
print(Fore.YELLOW + "Analysing your mood", flush = True)
dots()

mp = TextBlob(mood).sentiment.polarity
md = "Positive" if mp >   0 else "Negative" if mp < 0 else "Neutral"

print(Fore.YELLOW + f"Your mood is {md} (Polarity {mp:.2f})\n")

rating = get_rating()
print(Fore.YELLOW + f"Finding movies for {name}", end='', flush=True)
dots()

rec = recommend(genre=genre, mood=mood, rating=rating, n = 5)
print(Fore.YELLOW + "Recommended movies are", rec) if isinstance (rec, str) else show(rec, name)

while True:
    a = input(Fore.YELLOW + "Would you like more recommendations?\n").strip().lower()
    if a == 'no':
        print(Fore.BLUE + f"No problem! Enjoy {name}")
        break
    if a == 'yes':
        rec = recommend(genre=genre, mood=mood, rating=rating, n = 5)
        print(Fore.YELLOW + "Recommended movies are", rec) if isinstance (rec, str) else show(rec, name)

    else:
        print(Fore.RED + "Error: Invalid Choice")