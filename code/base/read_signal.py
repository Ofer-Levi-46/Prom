import numpy as np
import scipy.io.wavfile as wavfile
import matplotlib.pyplot as plt
from base.helper import *
from scipy.signal import butter, filtfilt, hilbert
from scipy.signal import find_peaks


def read_signal(filename: str) -> list[int]:
    """
    Reads a signal from a WAV file, demodulates it, and extracts bits encoded in the signal.

    Args:
        filename (str): The name of the WAV file to read. The file is expected to be located
                        in the 'records/' directory.

    Returns:
        list[int]: A list of bits (0s and 1s) extracted from the demodulated signal.

    The function performs the following steps:
    1. Loads the WAV file and normalizes the signal.
    2. Demodulates the signal using a carrier wave.
    3. Identifies the start and end markers in the signal using correlation with predefined waves.
    4. Extracts the portion of the signal between the start and end markers.
    5. Divides the signal into blocks corresponding to symbols and determines the bit value
       for each block based on the average of the highest values in the block.
    """

    # === Load WAV ===
    data = wavfile.read(f'records/{filename}')[1]
    signal = (data / 32767.0).astype(np.float32)

    # Demodulate the signal
    time = np.arange(len(signal)) / fs
    carrier = np.cos(2 * np.pi * fc * time)
    demodulated_signal =  -1 *  signal * carrier
    demodulated_signal[demodulated_signal < 0] = 0

    start_wave = generate_wave(string_to_bits(record_start_key))
    end_wave = generate_wave(string_to_bits(record_end_key))
    len_start_wave = len(start_wave)
    len_end_wave = len(end_wave)
    start_wave = start_wave * carrier[0:len_start_wave] - 1
    start_wave[start_wave < 0] = 0
    end_wave = end_wave * carrier[len(signal)-len_end_wave:len(signal)] - 1
    end_wave[end_wave < 0] = 0

    # normalize the start and end waves
    # start_wave = (start_wave - np.min(start_wave)) / np.max(np.abs(start_wave - np.min(start_wave)))
    end_wave = (end_wave - np.min(end_wave)) / np.max(np.abs(end_wave - np.min(end_wave)))
    # normalize the demodulated signal
    demodulated_signal = (demodulated_signal - np.min(demodulated_signal)) / np.max(np.abs(demodulated_signal - np.min(demodulated_signal)))

    start = np.argmax(np.correlate(demodulated_signal, start_wave, mode='valid'))
    end = np.argmax(np.correlate(demodulated_signal, end_wave, mode='valid'))
    demodulated_signal = demodulated_signal[start+len_start_wave : end]

    bits = []

    # extract the bits
    for i in range(0, len(demodulated_signal), samples_per_symbol):
        block = demodulated_signal[i:i + samples_per_symbol]
        if len(block) < samples_per_symbol:
            continue

        # calculate the average of the 10 highest values
        avg_value = np.mean(np.sort(block)[-10:])
        bits.append(1 if avg_value > 0.35 else 0)

    return bits