import numpy as np
from base.helper import *
import errors.error_correction as ec

delta_f = samples_per_symbol


def read_signal(signal: list[float]) -> list[int]:
    """
    Reads a signal from an array, demodulates it, and extracts bits encoded in the signal.

    Args:
        signal (list[float]): The input signal as a list of float values.

    Returns:
        list[int]: A list of decoded bits represented as integers (0 or 1).
    """

    bits = []
    
    start_wave = generate_wave(ec.encode(string_to_bits(record_start_key)))
    end_wave = generate_wave(ec.encode(string_to_bits(record_end_key)))
    # plot the correlation of the signal with the start and end waves

    start = np.argmax(np.correlate(signal, start_wave, mode='valid'))
    end = np.argmax(np.correlate(signal, end_wave, mode='valid'))
    signal = signal[start + len(start_wave):end]

    t = np.linspace(0, symbol_time, samples_per_symbol, endpoint=False)
    ref_f0 = np.cos(2 * np.pi * (fc - 1.5 * delta_f) * t)
    ref_f1 = np.cos(2 * np.pi * (fc - 0.5 * delta_f) * t)
    ref_f2 = np.cos(2 * np.pi * (fc + 0.5 * delta_f) * t)
    ref_f3 = np.cos(2 * np.pi * (fc + 1.5 * delta_f) * t)


    for i in range(0, len(signal), samples_per_symbol):
        chunk = signal[i:i + samples_per_symbol]

        if len(chunk) < samples_per_symbol:
            continue

        # Correlate with reference signals
        correlation_f0 = np.max(np.correlate(chunk, ref_f0, mode='valid'))
        correlation_f1 = np.max(np.correlate(chunk, ref_f1, mode='valid'))
        correlation_f2 = np.max(np.correlate(chunk, ref_f2, mode='valid'))
        correlation_f3 = np.max(np.correlate(chunk, ref_f3, mode='valid'))

         # frequency dictionary
        freq_dict = {
            correlation_f0: (1, 0),
            correlation_f1: (1, 1),
            correlation_f2: (0, 1),
            correlation_f3: (0, 0)
        }

        # choose the correlation with the highest maximum
        max_correlation = max(correlation_f0, correlation_f1, correlation_f2, correlation_f3)
        bits.append(freq_dict[max_correlation])
    
    # reshape bits to a 1-D array
    bits = np.array(bits).reshape(-1)

    return bits


def generate_wave(arr):
    """
    Generates a modulated wave signal based on the input binary array.

    The function takes an input binary array, processes it to create a sequence of
    symbols, and generates a waveform by modulating these symbols. If the
    input array has an odd length, it is padded with a zero to make its
    length even.

    Args:
        arr (list or numpy.ndarray): Input binary array (0s and 1s) representing
            the data to be modulated.

    Returns:
        numpy.ndarray: A 1D array representing the generated modulated wave
        signal.
    """

    # Ensure the input array is a NumPy array
    arr = np.array(arr)

    # Pad the array with a zero if its length is odd
    distance = len(arr) % 4
    if distance != 0:
        arr = np.append(arr, np.zeros(distance))  # zero padding

    # Generate time vector for one symbol
    t = np.linspace(0, symbol_time, samples_per_symbol, endpoint=False)

    # Define frequencies for FSK modulation
    f0 = fc - 1.5 * delta_f  # Frequency for binary 10
    f1 = fc - 0.5 * delta_f  # Frequency for binary 11
    f2 = fc + 0.5 * delta_f # Frequency for binary 01
    f3 = fc + 1.5 * delta_f  # Frequency for binary 00

    # symbol dictionary
    symbol_dict = {
        (1, 0): f0,
        (1, 1): f1,
        (0, 1): f2,
        (0, 0): f3,
    }

    # Generate the modulated wave
    wave_freq = []
    for i in range(0, len(arr), 2):
        symbol = (arr[i], arr[i+1])
        chosen_freq = symbol_dict[symbol]
        wave_chunk = np.cos(2 * np.pi * chosen_freq * t)
        wave_freq.extend(wave_chunk)
    wave = np.array(wave_freq)

    return wave
