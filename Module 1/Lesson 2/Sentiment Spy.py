import colorama
from colorama import Fore, Style
from textblob import TextBlob

colorama.init()
print(f"{Fore.GREEN} Wecome to sentiment spy{Style.RESET_ALL}")
user_name = input(f"{Fore.YELLOW} Enter your name {Style.RESET_ALL}")

if not user_name:
    user_name = "Mystery Agent"

conversation_history = []

print(f"\n{Fore.BLACK} Hello {user_name}, please enter a sentence and I will analyse its sentiment{Style.RESET_ALL}")
print(f"Type {Fore.YELLOW}reset{Fore.CYAN}, {Fore.YELLOW}history{Fore.CYAN}, "
    f"or {Fore.YELLOW}exit{Fore.CYAN} to quit.{Style.RESET_ALL}\n")

while True:
    user_input = input(f"{Fore.BLUE}>> {Style.RESET_ALL}")
    if not user_input:
        print(f"{Fore.GREY} Please enter a valid input {Style.RESET_ALL}")
        continue
    if user_input.lower() == "exit":
        print(f"{Fore.RED} Goodbye, {user_name}!{Style.RESET_ALL}")
        break
    elif user_input.lower() == "reset":
        conversation_history.clear()
        print(f"{Fore.BLUE} All history has been cleared {Style.RESET_ALL}")
        continue
    elif user_input.lower() == "history":
        if not conversation_history:
            print(f"{Fore.LIGHTMAGENTA_EX} No conversation history available.{Style.RESET_ALL}")
        else:
            print(f"{Fore.CYAN} Conversation History:{Style.RESET_ALL}")
            for i, (text, polarity, sentiment_type) in enumerate(conversation_history, start = 1):
                if sentiment_type == "Positive":
                    color = Fore.GREEN
                    emoji = "😊"
                elif sentiment_type == "Negative":
                    color = Fore.RED
                    emoji = "😞"
                else:
                    color = Fore.YELLOW
                    emoji = "😐"
                print(f"{color}{i}. {text} - Polarity: {polarity:.2f} - Sentiment: {sentiment_type} {emoji}{Style.RESET_ALL}")
        continue
    polarity = TextBlob(user_input).sentiment.polarity
    if polarity > 0.25:
        sentiment_type = "Positive"
        color = Fore.GREEN
        emoji = "😊"
    elif polarity < -0.25:
        sentiment_type = "Negative"
        color = Fore.RED
        emoji = "😞"
    else:
        sentiment_type = "Neutral"
        color = Fore.YELLOW
        emoji = "😐"

    conversation_history.append((user_input, polarity, sentiment_type))
    print(f"{color} {emoji} {sentiment_type} Sentiment Detected (Polarity: {polarity:.2f})")
