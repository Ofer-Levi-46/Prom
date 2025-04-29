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
    bits = []

    
    start_wave = generate_wave(string_to_bits(record_start_key))
    end_wave = generate_wave(string_to_bits(record_end_key))
    # plot the correlation of the signal with the start and end waves
    
    start = np.argmax(np.correlate(signal, start_wave, mode='valid'))
    end = np.argmax(np.correlate(signal, end_wave, mode='valid'))
    signal = signal[start+len(start_wave):end]

    t = np.linspace(0, symbol_time, samples_per_symbol, endpoint=False)
    ref_f0 = np.cos(2 * np.pi * (fc - (fc / 4)) * t)
    ref_f1 = np.cos(2 * np.pi * (fc + (fc / 4)) * t)

    for i in range(0, len(signal), samples_per_symbol):
        chunk = signal[i:i + samples_per_symbol]

        if len(chunk) < samples_per_symbol:
            continue
        
        # Correlate with reference signals
        correlation_f0 = np.max(np.correlate(chunk, ref_f0, mode='valid'))
        correlation_f1 = np.max(np.correlate(chunk, ref_f1, mode='valid'))
        
        # Decide bit based on higher correlation
        if correlation_f1 > correlation_f0:
            bits.append(1)
        else:
            bits.append(0)

    return np.array(bits)