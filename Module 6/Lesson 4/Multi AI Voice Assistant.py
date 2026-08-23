import speech_recognition as sr
import pyttsx3
from datetime import datetime

def setup_engine():
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    
    voices = engine.getProperty('voices')
    print("--- Select Voice ---")
    available_voices = voices[:4]
    
    for i, voice in enumerate(available_voices):
        print(f"{i + 1}. {voice.name}")
        
    try:
        choice = int(input(f"Enter choice (1-{len(available_voices)}): ")) - 1
        if 0 <= choice < len(available_voices):
            engine.setProperty('voice', available_voices[choice].id)
    except ValueError:
        print("Invalid selection. Using default voice.")
        
    return engine

def speak(engine, text):
    engine.say(text)
    engine.runAndWait()

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak...")
        audio = r.listen(source=source)
        try:
            command = r.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            print("I couldn't understand that")
        except sr.RequestError as e:
            print(f"API Error: {e}")
    return ""

def respond_to_command(engine, command):
    if "hello" in command or "hi" in command:
        speak(engine, "Hi! How can I help you today?")
    elif "your name" in command:
        speak(engine, "I am your AI voice assistant!")
    elif "time" in command:
        now = datetime.now().strftime("%H:%M")
        speak(engine, f"The time is {now}")
    elif "exit" in command or "quit" in command:
        speak(engine, "Goodbye!")
        return False
    else:
        speak(engine, "I am not sure how I can help with that!")
    return True

def main():
    engine = setup_engine()
    speak(engine, "Voice assistant activated. Say something!")
    
    while True:
        command = get_audio()
        if command:
            if not respond_to_command(engine, command):
                break

if __name__ == "__main__":
    main()