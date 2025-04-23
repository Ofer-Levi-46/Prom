import numpy as np
import scipy.io.wavfile as wavfile
from helper import *


def binary_to_signal(arr):
    arr = np.concatenate((string_to_bits(record_start_key), arr, string_to_bits(record_end_key)))
    return generate_wave(arr)


if __name__ == "__main__":
    arr = string_to_bits("Hello World! My name is John Doe. I am a software engineer. I love coding.\ndo you love coding too? \n yes I do.")
    signal = binary_to_signal(arr)
    # Save the generated signal as a WAV file
    wavfile.write('output.wav', fs, (signal * 32767).astype(np.int16))