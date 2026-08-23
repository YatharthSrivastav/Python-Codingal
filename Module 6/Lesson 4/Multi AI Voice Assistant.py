import speech_recognition as sr
import pyttsx3
from datetime import datetime

def select_voice():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    print("--- Select Voice ---")
    available_voices = voices
    
    for i, voice in enumerate(available_voices):
        print(f"{i + 1}. {voice.name}")
        
    choice = input("Select voice (1-3): ")
    try:
        index = int(choice) - 1
        if 0 <= index < len(available_voices):
            return available_voices[index].id
    except ValueError:
        pass
        
    print("Defaulting to first voice.")
    return voices[0].id

def speak(text, voice_id):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('voice', voice_id)
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

def respond_to_command(command, voice_id):
    if "hello" in command or "hi" in command:
        speak("Hi! How can I help you today?", voice_id)
    elif "your name" in command:
        speak("I am your AI voice assistant!", voice_id)
    elif "time" in command:
        now = datetime.now().strftime("%H:%M")
        speak(f"The time is {now}", voice_id)
    elif "exit" in command or "quit" in command:
        speak("Goodbye!", voice_id)
        return False
    else:
        speak("I am not sure how I can help with that!", voice_id)
    return True

def main():
    selected_voice = select_voice()
    speak("Voice assistant activated. Say something!", selected_voice)
    
    while True:
        command = get_audio()
        if command and not respond_to_command(command, selected_voice):
            break

if __name__ == "__main__":
    main()