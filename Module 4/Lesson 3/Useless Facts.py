import requests

def random_facts():
    URL = "https://uselessfacts.jsph.pl/api/v2/facts/random?language=en"
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        print(f"Fun Fact: {data["text"]}")
    else:
        print("Error: Failed to load a fact.")

def today_facts():
    URL = "https://uselessfacts.jsph.pl/api/v2/facts/today?language=en"
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        print(f"Today's Fun Fact: {data["text"]}")
    else:
        print("Error: Failed to load a fact.")

print("1. Random Facts")
print("2. Useless Facts")
print("3. Quit")
choice = input("Select what you want")

if choice == "1":
    random_facts()
    print("Bye!")
elif choice == "2":
    today_facts()
elif choice == "3":
    print("Bye!")
    exit()
else:
    print("Please enter 1, 2 or 3")





