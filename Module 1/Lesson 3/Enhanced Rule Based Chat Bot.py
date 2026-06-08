import re, random
from colorama import Fore, init

init(autoreset= True)

selected_city = None
history_file = "conversation_history.txt"
conversation_history = []

destinations = {
    "beaches":[
        "Maldives",
        "Marine Drive",
        "Goa",]
    ,"mountains":[
        "Himalayas",
        "Alps",
        "Rockies",]
    ,"cities":[
        "New York",
        "Mumbai",
        "Tokyo"]
}

times = {
    "new york": "07:00 AM",
    "mumbai": "4:30 PM",
    "tokyo": "8:00 PM",
    "maldives": "05:30 PM",
    "marine drive": "04:30 PM",
    "goa": "03:30 PM",
    "himalayas": "05:45 AM",
    "alps": "12:00 PM",
    "rockies": "02:00 PM",
}



jokes = [
    "Why don't scientists trust atoms?",
    "Why did the bicycle fall over?",
    "Why don't skeletons fight each other?"
]

weather = [
    "sunny",
    "rainy",
    "cloudy",
    "snowy",
]

news = {
    "world": [
        "Global markets rally on economic recovery hopes.",
        "New climate change report warns of severe consequences.",
        "International leaders meet to discuss trade agreements."
    ],
    "technology": [
        "Tech company unveils groundbreaking new smartphone.",
        "AI advancements raise ethical questions in the industry.",
        "Cybersecurity threats continue to evolve, experts warn."
    ],
    "sports": [
        "Local team wins championship after thrilling final.",
        "Star athlete announces retirement from professional sports.",
        "Upcoming sports event promises exciting matchups."
    ]
}


def normalise_input(text):
    return re.sub(r"\s+", " ", text.strip().lower())

def save_to_history(user_input):
    global conversation_history
    conversation_history.append(user_input)
    with open(history_file, "a") as f:
        f.write(user_input + "\n")

def load_history():
    global conversation_history
    try:
        with open(history_file, "r") as f:
            conversation_history = [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        conversation_history = []

def show_memory():
    if conversation_history:
        print(Fore.GREEN + "\nTravel Bot: Here's your conversation history:")
        for i, entry in enumerate(conversation_history[-10:], 1):
            print(Fore.GREEN + f"{i}. {entry}")
        print()
    else:
        print(Fore.GREEN + "Travel Bot: No conversation history yet.\n")

def show_time():
    global selected_city
    print(Fore.GREEN + "Travel Bot: Here is the time for your chosen city:")
    if selected_city in times:
        print(Fore.GREEN + f"Travel Bot: The current time in {selected_city.title()} is {times[selected_city]}.")
    else:
        print(Fore.GREEN + "Travel Bot: Please choose a destination first using 'recommend'.")

def recommend():
    global selected_city
    print(Fore.GREEN + "Travel Bot: Beaches, Mountains, Cities?")
    preference = input(Fore.BLUE + "You: ")
    preference = normalise_input(preference)

    if preference in destinations:
        suggest = random.choice(destinations[preference])
        selected_city = normalise_input(suggest)
        print(Fore.GREEN + f"Travel Bot: I recommend visiting {suggest}!")
        print(Fore.GREEN + "Travel Bot: Do you like this (Yes/No)? ")
        answer = input(Fore.BLUE + "You: ").lower()

        if answer == "yes":
            if preference == "cities":
                print(Fore.GREEN + "Travel Bot: Would you like to know the time there? (Yes/No)")
                time_answer = input(Fore.BLUE + "You: ").lower()
                if time_answer == "yes":
                    show_time()
                elif time_answer == "no":
                    print(Fore.GREEN + "No problem! We can talk about something else")
                else:
                    print(Fore.GREEN + "Please type a valid answer. (Yes/No)")
            print(Fore.GREEN + f"Travel Bot: I hope you enjoy {suggest}!")
        elif answer == "no":
            print(Fore.GREEN + "Travel Bot: No worries! Let's try again.")
            recommend()
        else:
            print(Fore.GREEN + "Travel Bot: I will suggest another one!")
            recommend()

    else:
        print(Fore.GREEN + "Travel Bot: I didn't understand that. Please choose from Beaches, Mountains, or Cities.")

def packing_tips():
    print(Fore.GREEN + "Travel Bot: Where to?")
    location = normalise_input(input(Fore.BLUE + "You: "))
    print(Fore.GREEN + f"Travel Bot: How many days?:")
    days = input(Fore.BLUE + "You: ")
    print(Fore.GREEN + f"Travel Bot: Here are some packing tips for your trip to {location} for {days} days:")
    print(Fore.GREEN + "- Pack light and only bring essentials.")
    print(Fore.GREEN + "- Check the weather forecast for your destination.")
    print(Fore.GREEN + "- Don't forget to pack any necessary medications.")
    print(Fore.GREEN + "- Consider the activities you'll be doing and pack accordingly.")

def tell_joke():
    print(Fore.GREEN + f"Travel Bot: Here's a joke for you: {random.choice(jokes)}")

def check_weather():
    print(Fore.GREEN + "Travel Bot: Where are you headed?")
    location = normalise_input(input(Fore.BLUE + "You: "))
    print(Fore.GREEN + f"Travel Bot: Checking the weather for {location}...")
    print(Fore.GREEN + f"Travel Bot: The current weather in {location} is {random.choice(weather)}.")

def get_news():
    while True:
        print(Fore.GREEN + "Travel Bot: What news category are you interested in? (World, Technology, Sports)")
        category = normalise_input(input(Fore.BLUE + "You: "))
        if category in news:
            print(Fore.GREEN + f"Travel Bot: Here are the latest {category} news headlines:")
            for headline in news[category]:
                print(Fore.GREEN + f"- {headline}")
            break
        else:
            print(Fore.GREEN + "Travel Bot: I'm sorry, I don't have news for that category. Please choose from World, Technology, or Sports.")

def show_help():
    print(Fore.GREEN + "\n I can:")
    print(Fore.GREEN + "- Recommend travel destinations based on your preferences. (say 'recommend')")
    print(Fore.GREEN + "- Provide packing tips for your trip. (say 'packing tips')")
    print(Fore.GREEN + "- Tell you a joke. (say 'joke')")
    print(Fore.GREEN + "- Check the weather for your destination. (say 'weather')")
    print(Fore.GREEN + "- Get the latest news headlines. (say 'news')")
    print(Fore.GREEN + "- View your conversation history. (say 'memory')")
    print(Fore.GREEN + "- Type 'exit' to quit the chat.\n")

def chat():
    load_history()
    print(Fore.GREEN + "Welcome to Travel Bot! How can I assist you today?")
    name = input(Fore.BLUE + "What's your name? ")
    print(Fore.GREEN + f"Travel Bot: Nice to meet you, {name}!")

    show_help()

    while True:
        user_input = input(Fore.BLUE + "You: ").lower()
        user_input = normalise_input(user_input)
        save_to_history(user_input)

        if user_input == "recommend":
            recommend()
        elif "packing tips" in user_input:
            packing_tips()
        elif "joke" in user_input:
            tell_joke()
        elif user_input == "weather":
            check_weather()
        elif user_input == "news":
            get_news()
        elif user_input == "help":
            show_help()
        elif user_input == "memory":
            show_memory()
        elif user_input == "exit":
            print(Fore.GREEN + f"Travel Bot: Goodbye, {name}! Safe travels!")
            break
        else:
            print(Fore.GREEN + "Travel Bot: I'm sorry, I didn't understand that. Please try again or type 'help' for options.")

if __name__ == "__main__":
    chat()
