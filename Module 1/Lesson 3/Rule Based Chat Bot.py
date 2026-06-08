import re, random
from colorama import Fore, init

init(autoreset= True)

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
        "Delhi"]

}

Jokes = [
    "Why don't scientists trust atoms?",
    "Why did the bicycle fall over?",
    "Why don't skeletons fight each other?"
]

def normalise_input(text):
    return re.sub(r"\s+", " ", text.strip().lower())

def recommend():
    print(Fore.GREEN + "Travel Bot: Beaches, Mountains, Cities?")
    preference = input(Fore.BLUE + "You: ")
    preference = normalise_input(preference)

    if preference in destinations:
        suggest = random.choice(destinations[preference])
        print(Fore.GREEN + f"Travel Bot: I recommend visiting {suggest}!")
        print(Fore.GREEN + "Travel Bot: Do you like this (Yes/No)? ")
        answer = input(Fore.BLUE + "You: ").lower()

        if answer == "yes":
            print(Fore.GREEN + f"Travel Bot: Great! I hope you enjoy {suggest}!")
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
    print(Fore.GREEN + f"Travel Bot: Here's a joke for you: {random.choice(Jokes)}")

def show_help():
    print(Fore.GREEN + "\n I can:")
    print(Fore.GREEN + "- Recommend travel destinations based on your preferences. (say 'recommend')")
    print(Fore.GREEN + "- Provide packing tips for your trip. (say 'packing tips')")
    print(Fore.GREEN + "- Tell you a joke. (say 'joke')")
    print(Fore.GREEN + "- Type 'exit' to quit the chat.\n")

def chat():
    print(Fore.GREEN + "Welcome to Travel Bot! How can I assist you today?")
    name = input(Fore.BLUE + "What's your name? ")
    print(Fore.GREEN + f"Travel Bot: Nice to meet you, {name}!")

    show_help()

    while True:
        user_input = input(Fore.BLUE + "You: ").lower()
        user_input = normalise_input(user_input)

        if user_input == "recommend":
            recommend()
        elif "packing tips" in user_input:
            packing_tips()
        elif "joke" in user_input:
            tell_joke()
        elif user_input == "help":
            show_help()
        elif user_input == "exit":
            print(Fore.GREEN + f"Travel Bot: Goodbye, {name}! Safe travels!")
            break
        else:
            print(Fore.GREEN + "Travel Bot: I'm sorry, I didn't understand that. Please try again or type 'help' for options.")

if __name__ == "__main__":
    chat()
