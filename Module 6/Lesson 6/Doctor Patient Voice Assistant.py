import speech_recognition as sr
import pyttsx3
from googletrans import Translator
import requests
import _asyncio
from Config import HF_API_KEY
HF_TOKEN = HF_API_KEY
MODEL = "facebook/bart-large-cnn"
HF_URL = f"https://router.huggingface.co/hf-inference/models/{MODEL}"
def speak(text):
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)
    print("🔊", text)
    engine.say(text)
    engine.runAndWait()
    engine.stop()
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source,phrase_time_limit=10)
    try:
        text = recognizer.recognize_google(audio)
        print("👤", text)
        return text
    except sr.UnknownValueError:
        print("❌ Could not understand.")
        return ""
    except sr.RequestError:
        print("❌ Speech API error.")
        return ""
async def detect_language(text):
    async with Translator() as translator:
        result = await translator.detect(text)
        print("🌍 Detected language:", result.lang)
    return result.lang
async def translate_text(text, target_language):
    async with Translator() as translator:
        result = await translator.translate(text,dest=target_language)
        print("🔄 Translation:", result.text)
    return result.text
def find_health_information(text):
    keywords = [
        "pain",
        "headache",
        "fever",
        "cough",
        "cold",
        "tired",
        "weak",
        "vomiting",
        "nausea",
        "dizzy",
        "stomach"
    ]
    found = []
    text = text.lower()
    for word in keywords:
        if word in text:
            found.append(word)
    return found
def generate_summary(conversation):
    if not conversation:
        return "No conversation recorded."
    text = "\n".join(conversation)
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    data = {"inputs": text}
    try:
        print("\n🤗 Asking Hugging Face AI...")
        response = requests.post( HF_URL, headers=headers, json=data, timeout=60)
        if response.status_code == 200:
            result = response.json()
            return result[0]["summary_text"]
        else:
            print("Hugging Face error:",response.status_code)
            return "AI summary unavailable."
    except Exception as error:
        print("❌ AI error:", error)
        return "AI summary unavailable."
    
def start_consultation(patient_language,doctor_language):
    conversation = []
    health_information = []
    speaker = "Patient"
    print("\n")
    print("=" * 55)
    print("🏥 MEDIBRIDGE AI")
    print("Real-Time Health Communication Assistant")
    print("=" * 55)
    print( f"🧑 Patient language: {patient_language}")
    print(f"👨‍⚕️ Doctor language: {doctor_language}")
    print("\nSay 'stop' to finish.")
    print("=" * 55)
    while True:
        print(f"\n🎙️ {speaker} speaking...")
        original_text = listen()
        if not original_text:
            continue
        if original_text.lower() == "stop":
            print("\n🛑 Consultation ended.")
            break
        detected_language = detect_language(original_text)
        if speaker == "Patient":
            target_language = doctor_language
        else:
            target_language = patient_language
        translated_text = translate_text(original_text,target_language)
        detected_health = find_health_information(translated_text)
        if detected_health:
            print("🩺 Health information:", ", ".join(detected_health))
            health_information.extend( detected_health)
        conversation.append(f"{speaker}: {translated_text}")
        speak(translated_text)
        if speaker == "Patient":
            speaker = "Doctor"
        else:
            speaker = "Patient"
    print("\n")
    print("=" * 55)
    print("🧠 GENERATING AI SUMMARY")
    print("=" * 55)
    summary = generate_summary(conversation)
    print("\n📋 CONSULTATION SUMMARY")
    print("-" * 55)
    print(summary)
    print("\n🩺 HEALTH INFORMATION MENTIONED")
    if health_information:
        unique_health = set( health_information)
        for item in unique_health:
            print("•", item)
    else:
        print("No basic health keywords detected.")
    print("\n⚠️ This is an AI-generated summary.")
    print("It is not a medical diagnosis.")
    print("=" * 55)
def choose_language(title):
    languages = {
        "1": ("English", "en"),
        "2": ("Hindi", "hi"),
        "3": ("Tamil", "ta"),
        "4": ("Telugu", "te"),
        "5": ("Kannada", "kn"),
        "6": ("Bengali", "bn"),
        "7": ("Marathi", "mr"),
        "8": ("Gujarati", "gu"),
        "9": ("Malayalam", "ml")
    }
    print("\n" + title)
    for number, language in languages.items():
        print(number,"-",language[0],"(" + language[1] + ")")
    while True:
        choice = input("\nEnter choice: ")
        if choice in languages:
            return languages[choice][1]
        print("❌ Invalid choice.")
def main():
    print("\n🏥 MEDIBRIDGE AI")
    print("Real-Time Healthcare ""Communication Assistant")
    print("\n")
    patient_language = choose_language("🧑 PATIENT LANGUAGE")
    doctor_language = choose_language("👨‍⚕️ DOCTOR LANGUAGE")
    start_consultation(patient_language,doctor_language)
if __name__ == "__main__":
    main()