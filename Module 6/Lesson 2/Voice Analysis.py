import threading

try:
    import sys, time, pyaudio, wave
    import numpy as np
    import matplotlib.pyplot as plt
    import speech_recognition as sr
    from speech_recognition import AudioData
    import os
except ImportError as e:
    print(f"Import Error: {e}")
    sys.exit(1)

stop_event = threading.Event()


def wait_for_enter():
    input()
    stop_event.set()

def record_audio(label):
    stop_event.clear()
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,channels=1,rate=16000,input=True,frames_per_buffer=1024)

    frames = []
    print(f"\n {label}")
    print(" Press enter to stop...")
    threading.Thread(target=wait_for_enter, daemon=True).start()
    print("Recording", end="", flush=True)

    while not stop_event.is_set():
        frames.append(stream.read(1024, exception_on_overflow=False))

    print(".", end="", flush=True)
    print("...")

    stream.stop_stream()
    stream.close()

    width = p.get_sample_size(pyaudio.paInt16)
    p.terminate()

    return b"".join(frames), 16000, width


def analyze_audio(data, rate):
    samples = np.frombuffer(data, dtype=np.int16)
    return {"duration": len(samples) / rate,"avg_volume": np.mean(np.abs(samples)),"max_volume": np.max(np.abs(samples)),"samples": samples}


def transcribe(data, rate, width, filename="transcript.txt"):
    recognizer = sr.Recognizer()
    try:
        audio = AudioData(data, rate, width)
        text = recognizer.recognize_google(audio)

        with open(filename, "w") as f:
            f.write(text)
        print(f"Transcript saved to {filename}")
        return text
    except Exception as e:
        print(f"Error: {e}")
        return "[Transcription failed]"


def display_stats(stats, text, label):
    print(f"\n{'-' * 40}")
    print(f"{label}")
    print(f"{'-' * 40}")

    print(f"Duration:        "f"{stats['duration']:.2f} seconds")

    print(f"Average Amplitude:        "f"{stats['avg_volume']:.0f}")

    print(f"Max Amplitude:        "f"{stats['max_volume']:.0f}")

    print(f"Transcription:        "f"{text}")


def compare(stats1, stats2):
    print("\n" + "=" * 40)
    print("COMPARISON RESULTS")
    print("=" * 40)

    if stats1["duration"] > stats2["duration"]:
        longer = "Recording 1"

        if stats2["duration"] != 0:
            diff = ((stats1["duration"] - stats2["duration"])/ stats2["duration"]) * 100
        else:
            diff = 0

    else:
        longer = "Recording 2"

        if stats1["duration"] != 0:
            diff = ((stats2["duration"] - stats1["duration"])/ stats1["duration"]) * 100
        else:
            diff = 0

    print(f"{longer} is longer by "f"{diff:.1f}%")

    if stats1["avg_volume"] > stats2["avg_volume"]:
        louder = "Recording 1"

        if stats2["avg_volume"] != 0:
            diff = ((stats1["avg_volume"] - stats2["avg_volume"])/ stats2["avg_volume"]) * 100
        else:
            diff = 0

    else:
        louder = "Recording 2"

        if stats1["avg_volume"] != 0:
            diff = ((stats2["avg_volume"] - stats1["avg_volume"])/ stats1["avg_volume"]) * 100
        else:
            diff = 0

    print(f"{louder} is louder by "f"{diff:.1f}%")


def plot_both(stats1, stats2, rate):
    fig, (ax1, ax2) = plt.subplots(2, 1,figsize=(12, 6))
    t1 = np.linspace(0,len(stats1["samples"]) / rate,len(stats1["samples"]))
    ax1.plot(t1,stats1["samples"],color="blue",linewidth=0.5)
    ax1.set_title(f"Recording 1 (Normal) - "f"Duration: {stats1['duration']:.2f}s, "f"Avg: {stats1['avg_volume']:.0f}")
    ax1.set_ylabel("Amplitude")
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(-35000, 35000)

    t2 = np.linspace(0,len(stats2["samples"]) / rate,len(stats2["samples"]))
    ax2.plot(t2,stats2["samples"],color="red",linewidth=0.5)
    ax2.set_title(f"Recording 2 (Modified) - "f"Duration: {stats2['duration']:.2f}s, "f"Avg: {stats2['avg_volume']:.0f}")
    ax2.set_xlabel("Time (seconds)")
    ax2.set_ylabel("Amplitude")
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(-35000, 35000)

    plt.tight_layout()
    plt.show()


def main():
    print("=" * 40)
    print("VOICE ANALYSIS LAB")
    print("=" * 40)
    print("Record twice and compare your voice!")

    audio1, rate, width = record_audio("Recording 1: Speak NORMALLY")
    stats1 = analyze_audio(audio1, rate)
    text1 = transcribe(audio1, rate, width, "transcript1.txt")
    display_stats(stats1,text1,"Recording 1 Results")
    input("\n Press Enter, then speak ""LOUDER or FASTER...")
    audio2, rate, width = record_audio("Recording 2: CHANGE your voice!")
    stats2 = analyze_audio(audio2, rate)
    text2 = transcribe(audio2, rate, width, "transcript2.txt")
    display_stats( stats2, text2, "Recording 2 Results")
    compare(stats1, stats2)
    plot_both(stats1, stats2, rate)


if __name__ == "__main__":
    main()