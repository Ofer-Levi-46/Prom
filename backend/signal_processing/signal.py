import numpy as np
from .helper import *
from .error_correction import encode

delta_f = symbols_per_second


def read_signal(signal: list[float]) -> list[int]:
    bits = []

    # Detect preamble
    start_wave = generate_wave(encode(string_to_bits(record_start_key)))
    end_wave = generate_wave(encode(string_to_bits(record_end_key)))

    start = np.argmax(np.correlate(signal, start_wave, mode='valid'))
    end = np.argmax(np.correlate(signal, end_wave, mode='valid'))
    signal = signal[start + len(start_wave):end]

    # Reference tones
    t = np.linspace(0, symbol_time, samples_per_symbol, endpoint=False)
    frequencies = [
        np.cos(2 * np.pi * (fc - 1.5 * delta_f) * t),
        np.cos(2 * np.pi * (fc - 0.5 * delta_f) * t),
        np.cos(2 * np.pi * (fc + 0.5 * delta_f) * t),
        np.cos(2 * np.pi * (fc + 1.5 * delta_f) * t),
    ]
    bit_pairs = [(1, 0), (1, 1), (0, 1), (0, 0)]

    def normalized_dot(a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    # Symbol decoding loop
    for i in range(0, len(signal), samples_per_symbol):
        chunk = signal[i:i + samples_per_symbol]
        if len(chunk) < samples_per_symbol:
            continue

        correlations = [normalized_dot(chunk, f) for f in frequencies]
        bits.append(bit_pairs[np.argmax(correlations)])

    return np.array(bits).reshape(-1)



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
