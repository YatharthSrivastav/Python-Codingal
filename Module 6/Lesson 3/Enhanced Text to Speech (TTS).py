import speech_recognition as sr
import pyttsx3
from googletrans import Translator
import random

def speak(text, language="en"):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    voices = engine.getProperty('voices')
    if language == 'en':
        engine.setProperty('voice', voices[0].id)
    else:
        engine.setProperty('voice', voices[1].id)
    engine.say(text)
    engine.runAndWait()

def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please speak now in English...")
        audio = recognizer.listen(source)
    try:
        print("Recognizing speech...")
        text = recognizer.recognize_google(audio, language="en-US")
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Couldn't understand the audio...")
    except sr.RequestError as e:
        print(f"API Error: {e}")
    return ""

def translate_text(text, target_language="es"):
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    print(f"Translated text: {translation.text}")
    return translation.text

def display_options():
    print("Available language options are: ")
    print("1. Hindi (hi)")
    print("2. Tamil (ta)")
    print("3. Telugu (te)")
    print("4. Bengali (bn)")
    print("5. Marathi (mr)")
    print("6. Malayalam (ml)")
    print("7. Punjabi (pa)")
    print("8. Urdu (ur)")
    choice = input("Input a number (1-8)")
    language_dict = {
        "1": "hi",
        "2": "ta",
        "3": "te",
        "4": "bn",
        "5": "mr",
        "6": "ml",
        "7": "pa",
        "8": "ur"
    }
    return language_dict.get(choice, "es")

def get_samples():
    return [
        "hello",
        "how are you",
        "what's up",
        "tell me something fun",
        "make me laugh",
        "surprise me"
    ]

def speed_up():
    engine = pyttsx3.init()
    engine.setProperty('rate', 180)
    engine.say("I am speaking faster now.")
    engine.runAndWait()

def slow_down():
    engine = pyttsx3.init()
    engine.setProperty('rate', 100)
    engine.say("I am speaking slower now.")
    engine.runAndWait()

def increase_volume():
    engine = pyttsx3.init()
    engine.setProperty('volume', 1.0)
    engine.say("Volume increased.")
    engine.runAndWait()

def decrease_volume():
    engine = pyttsx3.init()
    engine.setProperty('volume', 0.3)
    engine.say("Volume decreased.")
    engine.runAndWait()

def tell_joke():
    jokes = [
        "Why did the computer go to the doctor? Because it had a virus!",
        "Why was the computer cold? Because it left its Windows open!",
        "Why do programmers prefer dark mode? Because light attracts bugs!"
    ]
    speak(random.choice(jokes))


def main():
    target_languages = display_options()

    while True:
        original_text = speech_to_text()

        if original_text:
            command = original_text.lower()

            if command == "exit":
                speak("Goodbye!")
                break

            elif command == "speed up":
                speed_up()

            elif command == "slow down":
                slow_down()

            elif command == "increase volume":
                increase_volume()

            elif command == "decrease volume":
                decrease_volume()

            elif command == "tell a joke":
                tell_joke()

            else:
                translated_text = translate_text(original_text, target_language=target_languages)
                speak(translated_text, language="en")
                print("Translation done!")
        else:
            speak("I didn't quite catch that. Try again!")


if __name__ == "__main__":
    main()
