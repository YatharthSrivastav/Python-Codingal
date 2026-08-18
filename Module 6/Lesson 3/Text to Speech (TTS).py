import speech_recognition as sr
import pyttsx3
from googletrans import Translator

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

def main():
    target_languages = display_options()
    original_text = speech_to_text()
    if original_text:
        translated_text = translate_text(original_text, target_language=target_languages)
        speak(translated_text, language="en")
        print("Translation done!")

if __name__ == "__main__":
    main()


