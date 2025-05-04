from base.helper import string_to_bits, fs, record_start_key, record_end_key
from base.signal import generate_wave
from scipy.io.wavfile import write
import errors.error_correction as ec
import numpy as np


data = "Hello, World!"
filename = "encoded.wav"


if __name__ == "__main__":
    message = record_start_key + data + record_end_key
    encoded_data = ec.encode(string_to_bits(message))
    wave = generate_wave(encoded_data)

    # Save the wave to a file
    write("records/" + filename, fs, (wave * 32767).astype(np.int16))