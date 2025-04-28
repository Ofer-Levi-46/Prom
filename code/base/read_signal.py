import numpy as np
import scipy.io.wavfile as wavfile
import matplotlib.pyplot as plt
from base.helper import *


def read_signal(filename: str) -> str:
    """
    Reads a signal from a WAV file, decodes it using quadrature amplitude modulation (QAM),
    and extracts the embedded message as a string.
    Args:
        filename (str): The file name of the WAV file containing the encoded signal.
    Returns:
        str: The decoded message extracted from the signal.
    The function performs the following steps:
        1. Reads the WAV file and normalizes the signal.
        2. Identifies the start and end markers in the signal using cross-correlation.
        3. Extracts the portion of the signal between the start and end markers.
        4. Decodes the signal using QAM by correlating it with reference sinusoids.
        5. Converts the decoded bits into a string representation of the message.
    """

    # === Load WAV ===
    data = wavfile.read(f'records/{filename}')[1]
    signal = (data / 32767.0).astype(np.float32)

    start_wave = generate_wave(string_to_bits(record_start_key))
    end_wave = generate_wave(string_to_bits(record_end_key))

    start = np.argmax(np.correlate(signal, start_wave, mode='valid'))
    end = np.argmax(np.correlate(signal, end_wave, mode='valid'))
    signal = signal[start+len(start_wave) : end]

    # decoded_bits is an empty array of type int
    decoded_bits = np.array([], dtype=int)
    num_symbols = len(signal) // samples_per_symbol
    t_symbol = np.arange(0, symbol_time, 1/fs)

    for i in range(num_symbols):
        # Extract one symbol period
        symbol_segment = signal[i * samples_per_symbol : (i + 1) * samples_per_symbol]
        
        # Reference sinusoids
        ref_cos = np.cos(2 * np.pi * fc * t_symbol)
        ref_sin = np.sin(2 * np.pi * fc * t_symbol)
        
        # Correlate with basis functions
        I_hat = np.trapezoid(2 * symbol_segment * ref_cos, t_symbol) / symbol_time
        Q_hat = np.trapezoid(2 * symbol_segment * ref_sin, t_symbol) / symbol_time
        
        # Make decision
        if I_hat > 0 and Q_hat > 0:
            b1, b2 = 1, 1
        elif I_hat > 0 and Q_hat < 0:   
            b1, b2 = 0, 0
        elif I_hat < 0 and Q_hat > 0:
            b1, b2 = 1, 0
        else:
            b1, b2 = 0, 1

        # append the bits to the decoded array
        decoded_bits = np.append(decoded_bits, [b1, b2])

    # === Output ===
    # Convert bits to string
    # decoded_string = ''.join(str(bit) for bit in decoded_bits)
    # decoded_string = ''.join(chr(int(decoded_string[i:i+8], 2)) for i in range(0, len(decoded_string), 8))
    # return decoded_string

    return decoded_bits