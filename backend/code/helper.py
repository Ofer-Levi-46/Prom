import numpy as np
import json
import os


# Read JSON file
# Construct the path to the JSON file
current_dir = os.path.dirname(__file__)
json_file_path = os.path.join(current_dir, '../../frontend/public/data.json')
with open(json_file_path, 'r') as f:
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
