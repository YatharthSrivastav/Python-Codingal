import speech_recognition as sr
import pyttsx3
from datetime import datetime
import wikipedia
import webbrowser

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

def search_and_summarize(query):
    speak(f"Searching for {query}...")
    try:
        results = wikipedia.summary(query, sentences=2)
        print(f"Wikipedia: {results}")
        speak("According to Wikipedia:")
        speak(results)
    except wikipedia.exceptions.DisambiguationError:
        speak("There are multiple results for this topic. Please be more specific.")
    except wikipedia.exceptions.PageError:
        speak("I couldn't find a Wikipedia page for that, opening Google instead.")
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)
    except Exception as e:
        speak("Sorry, I encountered an error while searching.")
        print(f"Search error: {e}")

def respond_to_command(command):
    if "hello" in command or "hi" in command:
        speak("Hi! How can I help you today?")
        
    elif "your name" in command:
        speak("I am your AI voice assistant!")
        
    elif "time" in command:
        now = datetime.now().strftime("%H:%M")
        speak(f"The time is {now}")
        
    elif "search" in command or "search for" in command or "what is" in command or "who is" in command or "explain" in command:
  
        query = command.replace("search", "").replace("search for", "").replace("what is", "").replace("who is", "").replace("explain", "").strip()
        if query:
            search_and_summarize(query)
        else:
            speak("What would you like me to search for?")
            
    elif "exit" in command or "quit" in command:
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