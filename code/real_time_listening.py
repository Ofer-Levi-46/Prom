from base.helper import fs, record_start_key, record_end_key, string_to_bits
from base.bps_test import generate_wave_bps
import sounddevice as sd
import numpy as np

class Listener:
    def __init__(self, sampling_rate, start_key, end_key, duration=0.1):
        self.sampling_rate = sampling_rate
        self.start_key = start_key
        self.end_key = end_key
        self.frames = int(sampling_rate * duration)

    def start_listening(self):
        # graph the signal live from the microphone

        with sd.InputStream(samplerate=self.sampling_rate, channels=1, blocksize=self.frames) as stream:
            while True:
                data = stream.read(self.frames)[0]
                signal = data.flatten()
                self.check_interest(signal)


    def detect_key(self, signal, key):
        """
        Detects the presence of a specific key in the signal.

        Args:
            signal (numpy.ndarray): The audio signal to search.
            key (str): The key to detect.

        Returns:
            bool: True if the key is detected, False otherwise.
        """
        # Convert the key to bits
        key_bits = string_to_bits(key)
        # Generate the wave for the key
        key_wave = generate_wave_bps(key_bits)

        # Perform correlation
        correlation = np.correlate(signal, key_wave, mode='valid')
        threshold = 5

        return np.any(correlation > threshold)


if __name__ == "__main__":
    listener = Listener(fs, record_start_key, record_end_key)
    listener.start_listening()