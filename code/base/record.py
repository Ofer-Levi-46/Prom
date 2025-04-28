import sounddevice as sd
from scipy.io.wavfile import write
from base.helper import fs


def record(filename: str, duration: int = 5) -> None:
    """
    Records audio from the microphone and saves it as a WAV file.

    Args:
        filename (str): The file path where the recorded audio will be saved.
    """

    print("Recording started... Speak now!")

    # === Record ===
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()  # Wait until recording is finished

    print(f"Recording finished. Saving to {filename}")

    # === Save as WAV ===
    write("records/" + filename, fs, audio)

    print("File saved successfully!")
