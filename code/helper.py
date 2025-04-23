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
    if len(arr) % 2 != 0: arr.insert(0, 0)  # Pad with zero if odd length
    reshaped = np.reshape(arr, (len(arr) // 2, 2))
    f = lambda x: 2*x[0] + x[1]
    new_arr = np.apply_along_axis(f, arr=reshaped, axis=1)

    data = np.zeros(len(new_arr) * samples_per_symbol)
    t_symbol = np.arange(0, symbol_time, 1/fs)

    for i, x in enumerate(new_arr):
        data[i * samples_per_symbol : (i + 1) * samples_per_symbol] = np.cos(2 * np.pi * fc * t_symbol + np.pi * (x+1/2)/2)

    return data