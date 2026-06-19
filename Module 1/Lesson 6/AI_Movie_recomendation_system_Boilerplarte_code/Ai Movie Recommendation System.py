import time
import pandas as pd
from textblob import TextBlob
from colorama import init, Fore

# Init colors
init(autoreset=True)

# Load CSV
try:
    df = pd.read_csv("Module 1\\Lesson 6\\AI_Movie_recomendation_system_Boilerplarte_code\\imdb_top_1000.csv")
except FileNotFoundError:
    print(Fore.RED + "Error: The file 'imdb_top_1000.csv' was not found.")
    raise SystemExit

# Unique genres
genres = sorted({g.strip() for xs in df["Genre"].dropna().str.split(", ") for g in xs})


def dots():
    """Prints ... with delay (AI thinking effect)."""
    for _ in range(3):
        print(Fore.YELLOW + ".", end="", flush=True)
        time.sleep(0.5)
    print()


def senti(p):
    """Polarity -> sentiment label."""
    return "Positive 😊" if p > 0 else "Negative 😞" if p < 0 else "Neutral 😐"


def recommend(genre=None, mood=None, rating=None, n=5):
    """Filter by genre/rating, shuffle, analyze Overview polarity, return n recommendations."""
    d = df.copy()
    
    if genre:
        d = d[d["Genre"].str.contains(genre, case=False, na=False)]
    
    if rating is not None:
        d = d[d["IMDB_Rating"] >= rating]
    
    if d.empty:
        return None
    
    d = d.sample(frac=1).reset_index(drop=True)
    out = []
    need_nonneg = bool(mood) and TextBlob(mood).sentiment.polarity > 0
    
    for _, r in d.iterrows():
        ov = r.get("Overview")
        if pd.isna(ov):
            continue
        pol = TextBlob(ov).sentiment.polarity
        
        if not need_nonneg or pol >= 0:
            out.append((r["Series_Title"], pol))
            if len(out) == n:
                break
    
    return out if out else None


def show(recs, name):
    """Display recommendations with polarity and sentiment."""
    print(Fore.BLUE + f"\n🎬 AI Analysed Recommendations for {name}:\n")
    for i, (t, p) in enumerate(recs, 1):
        print(Fore.BLUE + f"{i}. {t} (Polarity: {p:.2f}, {senti(p)})")


def get_genre():
    """Get genre selection from user."""
    print(Fore.BLUE + "\nAvailable Genres:")
    for i, g in enumerate(genres, 1):
        print(Fore.GREEN + f"  {i}. {g}")
    
    print()
    while True:
        x = input(Fore.GREEN + "Enter the genre number or name: ").strip()
        
        if x.isdigit() and 1 <= int(x) <= len(genres):
            return genres[int(x) - 1]
        
        x = x.title()
        if x in genres:
            return x
        
        print(Fore.RED + "❌ Invalid input. Please try again.\n")


def get_rating():
    """Get rating threshold from user."""
    while True:
        x = input(Fore.GREEN + "Enter a rating from 7.6 to 9.3 (or 'skip'): ").strip()
        
        if x.lower() == 'skip':
            return None
        
        try:
            r = float(x)
            if 7.6 <= r <= 9.3:
                return r
            print(Fore.RED + "❌ Rating out of range (7.6 - 9.3). Please try again.\n")
        except ValueError:
            print(Fore.RED + "❌ Invalid input. Please enter a number or 'skip'.\n")


# Main Program
print(Fore.YELLOW + "\n" + "="*60)
print(Fore.YELLOW + "🤖 Welcome to your AI Movie Recommendation Assistant! 🎬")
print(Fore.YELLOW + "="*60 + "\n")

name = input(Fore.GREEN + "What is your name? ").strip()
print(Fore.YELLOW + f"\n✨ Nice to meet you, {name}!\n")
print(Fore.YELLOW + "Let's find you the perfect movie to watch today...\n")

genre = get_genre()
mood = input(Fore.GREEN + "\nHow are you feeling today? ").strip()

print(Fore.YELLOW + "📊 Analysing your mood", end="", flush=True)
dots()

mood_polarity = TextBlob(mood).sentiment.polarity
mood_desc = "Positive 😊" if mood_polarity > 0 else "Negative 😞" if mood_polarity < 0 else "Neutral 😐"
print(Fore.BLUE + f"Your mood is {mood_desc} (Polarity: {mood_polarity:.2f})\n")

rating = get_rating()

print(Fore.YELLOW + f"🎬 Finding movies for {name}", end="", flush=True)
dots()

rec = recommend(genre=genre, mood=mood, rating=rating, n=5)

if rec:
    show(rec, name)
else:
    print(Fore.RED + "❌ No suitable movie recommendations found.\n")

while True:
    a = input(Fore.GREEN + "\nWould you like more recommendations? (yes/no): ").strip().lower()
    
    if a == 'yes':
        print(Fore.YELLOW + f"🎬 Finding more movies for {name}", end="", flush=True)
        dots()
        rec = recommend(genre=genre, mood=mood, rating=rating, n=5)
        if rec:
            show(rec, name)
        else:
            print(Fore.RED + "❌ No more recommendations available.\n")
    elif a == 'no':
        print(Fore.BLUE + f"\n🎉 Thanks for using the recommendation system, {name}!")
        print(Fore.BLUE + "Enjoy your movie! 🍿\n")
        break
    else:
        print(Fore.RED + "❌ Invalid input. Please enter 'yes' or 'no'.\n")