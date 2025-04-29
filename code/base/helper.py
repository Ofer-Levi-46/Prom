import numpy as np
import json


# Read JSON file
with open('data.json', 'r') as f:
    json_data = json.load(f)

# Parameters
fc = json_data['frequency']
fs = json_data['sampling_rate']
symbols_per_second = json_data['symbols_per_second']
symbol_time = 1 / symbols_per_second
samples_per_symbol = fs // symbols_per_second

record_start_key = json_data["record_start"]
record_end_key = json_data["record_end"]

def string_to_bits(s):
    """
    Converts a string into an array of bits.

    This function takes a string, encodes it in UTF-8, and converts each character
    into its binary representation. The binary representation of each character
    is then split into individual bits, which are stored in a NumPy array.

    Args:
        s (str): The input string to be converted into bits.

    Returns:
        numpy.ndarray: A NumPy array containing the bits (0s and 1s) representing the input string.
    """
    return np.array([int(bit) for char in s.encode('utf-8') for bit in format(char, '08b')])

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

    Notes:
        - The modulation scheme used is cosine-based with a phase shift 
          determined by the input binary symbols.
    """

    # Ensure the input array is a NumPy array
    arr = np.array(arr)

    # Pad the array with a zero if its length is odd
    if len(arr) % 2 != 0:
        arr = np.append(arr, 0)

    # Generate time vector for the entire signal
    t = np.arange(0, len(arr) * symbol_time, 1 / fs)

    # Generate carrier wave at fc
    carrier = np.cos(2 * np.pi * fc * t)

    # Generate modulated signal
    modulated_signal = np.zeros_like(t)
    for i, bit in enumerate(arr):
        start_idx = int(i * samples_per_symbol)
        end_idx = int((i + 1) * samples_per_symbol)
        modulated_signal[start_idx:end_idx] = (1 + bit) * carrier[start_idx:end_idx]

    return modulated_signal