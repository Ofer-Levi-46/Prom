import sounddevice as sd
from scipy.io.wavfile import write
from helper import fs

# === Parameters ===
duration = 5  # seconds
filename = 'recordings/recording.wav'

print("Recording started... Speak now!")

# === Record ===
audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
sd.wait()  # Wait until recording is finished

print(f"Recording finished. Saving to {filename}")

# === Save as WAV ===
write(filename, fs, audio)

print("File saved successfully!")
