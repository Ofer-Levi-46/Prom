import numpy as np
import scipy.io.wavfile as wavfile
from base.helper import *


def generate_signal(arr: np.ndarray, filename: str) -> None:
    """
    Generates a wave signal from a given array of bits, appends start and end keys, 
    and saves it as a .wav file.

    Args:
        arr (numpy.ndarray): The array of bits to be converted into a wave signal.
        filename (str): The name of the output .wav file to be saved in the 'recordings' directory.

    Returns:
        None
    """
    
    arr = np.concatenate((string_to_bits(record_start_key), arr, string_to_bits(record_end_key)))
    signal = generate_wave(arr)
    wavfile.write(f'records/{filename}', fs, (signal * 32767).astype(np.int16))