import colorama
from colorama import Fore, Style
from textblob import TextBlob
from halo import Halo
import time

def show_processing_animation():
    spinner = Halo(spinner='spinner')
    spinner.start()
    time.sleep(3)
    spinner.stop()

colorama.init()
print(f"{Fore.GREEN} Welcome to sentiment spy{Style.RESET_ALL}")
user_name = input(f"{Fore.YELLOW} Enter your name {Style.RESET_ALL}")

def valid_name(user_name):
    if not user_name.isalpha():
        return False
    return True

if not user_name:
    user_name = "Mystery Agent"

while not valid_name(user_name):
    user_name = input(f"{Fore.YELLOW} Enter your name {Style.RESET_ALL}")

conversation_history = []

print(f"\n{Fore.BLACK} Hello {user_name}, please enter a sentence and I will analyse its sentiment{Style.RESET_ALL}")
print(f"Type {Fore.YELLOW}help{Fore.CYAN}, {Fore.YELLOW}reset{Fore.CYAN}, {Fore.YELLOW}history{Fore.CYAN}, "
    f"or {Fore.YELLOW}exit{Fore.CYAN} to quit.{Style.RESET_ALL}\n")

while True:
    user_input = input(f"{Fore.BLUE}>> {Style.RESET_ALL}")
    if not user_input:
        print(f"{Fore.LIGHTBLACK_EX} Please enter a valid input {Style.RESET_ALL}")
        continue
    if user_input.lower() == "exit":
        print(f"{Fore.RED} Goodbye, {user_name}!{Style.RESET_ALL}")

        positive_count = 0
        negative_count = 0
        neutral_count = 0

        for text, polarity, sentiment_type in conversation_history:
            if sentiment_type == "Positive":
                positive_count += 1
            elif sentiment_type == "Negative":
                negative_count += 1
            else:
                neutral_count += 1

        summary = f"""
                Sentiment Analysis Report for {user_name}
                ========================================
                Total messages analyzed: {len(conversation_history)}
                Positive: {positive_count}
                Negative: {negative_count}
                Neutral: {neutral_count}
                """

        with open(f"{user_name}_sentiment_analysis.txt", "w") as f:
            f.write(summary)
        break
    elif user_input.lower() == "reset":
        conversation_history.clear()
        print(f"{Fore.BLUE} All history has been cleared {Style.RESET_ALL}")
        continue
    elif user_input.lower() == "help":
        print(f"{Fore.CYAN} Available commands:{Style.RESET_ALL}")
        print(f" - {Fore.YELLOW}reset{Fore.CYAN}: Clear conversation history{Style.RESET_ALL}")
        print(f" - {Fore.YELLOW}history{Fore.CYAN}: View conversation history{Style.RESET_ALL}")
        print(f" - {Fore.YELLOW}exit{Fore.CYAN}: Quit the application{Style.RESET_ALL}")
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
        show_processing_animation()
        sentiment_type = "Positive"
        color = Fore.GREEN
        emoji = "😊"
    elif polarity < -0.25:
        show_processing_animation()
        sentiment_type = "Negative"
        color = Fore.RED
        emoji = "😞"
    else:
        show_processing_animation()
        sentiment_type = "Neutral"
        color = Fore.YELLOW
        emoji = "😐"

    conversation_history.append((user_input, polarity, sentiment_type))
    print(f"{color} {emoji} {sentiment_type} Sentiment Detected (Polarity: {polarity:.2f})")
