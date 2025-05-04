from helper import fs, record_start_key, record_end_key, string_to_bits
from signal import generate_wave, read_signal
import sounddevice as sd
import numpy as np


class Listener:
    """
    A class to listen for a specific key signal in real-time audio input and process the detected signal.
    """

    def __init__(self, sampling_rate: int, start_key: str, end_key: str, duration=0.1):
        """
        Initializes the real-time listening object.

        Args:
            sampling_rate (int): The sampling rate for audio processing in Hz.
            start_key (str): The key that triggers the start of the listening process.
            end_key (str): The key that triggers the end of the listening process.
            duration (float, optional): The duration of each audio frame in seconds. Defaults to 0.1.
        """

        self.sampling_rate = sampling_rate
        self.start_key = start_key
        self._key_wave = generate_wave(string_to_bits(start_key))
        self._is_interested = False
        self._frames = int(sampling_rate * duration)

    def start_listening(self):
        """
        Starts listening to an audio input stream and processes the incoming audio data.
        """

        print("Listening for key...")

        with sd.InputStream(samplerate=self.sampling_rate, channels=1, blocksize=self._frames) as stream:
            while True:
                data = stream.read(self._frames)[0]
                signal = data.flatten()
                self._check_interest(signal)

    def _on_start_interest(self, signal):
        print("Key detected! Start recording...")
        self._record = signal
    
    def _while_interest(self, signal):
        self._record = np.concatenate((self._record, signal))

    def _on_end_interest(self, signal):
        # write the record to a file
        self._record = np.concatenate((self._record, signal))

        data = read_signal(self._record)
        decoded_string = ''.join(str(bit) for bit in data)
        decoded_string = ''.join(chr(int(decoded_string[i:i+8], 2)) for i in range(0, len(decoded_string), 8))
        print(f"Final string: {decoded_string}")

    def _check_interest(self, signal):
        if not self._is_interested and self._detect_key(signal):
            self._is_interested = True
            self._on_start_interest(signal)
        elif self._is_interested and self._detect_key(signal):
            self._while_interest(signal)
        elif self._is_interested and not self._detect_key(signal):
            self._is_interested = False
            self._on_end_interest(signal)

    def _detect_key(self, signal):
        # Perform correlation
        correlation = np.correlate(signal, self._key_wave, mode='valid')
        threshold = 5

        return np.any(correlation > threshold)


if __name__ == "__main__":
    listener = Listener(fs, record_start_key, record_end_key)
    listener.start_listening()