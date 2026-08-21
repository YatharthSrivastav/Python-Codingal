import speech_recognition as sr
import pyttsx3
from datetime import datetime

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
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

def respond_to_command(command):
    if "hello" in command or "hi" in command:
        speak("Hi! How can I help you today?")
    elif "your name" in command:
        speak("I am you AI voice assistant!")
    elif "time" in command:
        now = datetime.now().strftime("%H:%M")
        speak(f"The time is {now}")
    elif "exit" or "quit" in command:
        speak("Goodbye!")
        return False
    else:
        speak("I am not sure how I can help with that!")
    return True

def main():
    speak("Voice assistant activated. Say something!")
    while True:
        command = get_audio()
        if command and not respond_to_command(command):
            break

if __name__ == "__main__":
    main()