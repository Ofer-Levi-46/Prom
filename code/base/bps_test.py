import numpy as np
from base.helper import string_to_bits
from base.helper import *
import scipy.io.wavfile as wavfile


def read_signal_bps(filename: str) -> list[int]:
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
    signal = signal[start + len(start_wave):end]

    t = np.linspace(0, symbol_time, samples_per_symbol, endpoint=False)
    ref_f0 = np.cos(2 * np.pi * (fc - (fc / 4)) * t)
    ref_f1 = np.cos(2 * np.pi * (fc + (fc / 4)) * t)
    ref_f2 = np.cos(2 * np.pi * (fc - (fc / 8)) * t)
    ref_f3 = np.cos(2 * np.pi * (fc + (fc / 8)) * t)


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


        # Decide symbol based on higher correlation
        chosen_freq = tuple(max( correlation_f0, correlation_f1, correlation_f2, correlation_f3))
        symbol = freq_dict[chosen_freq]
        signal_bits = [symbol[0], symbol[1]]
        bits.extend(signal_bits)
    print(bits)
    return np.array(bits)


def generate_wave_bps(arr):
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
    distance = len(arr) % 4
    if distance != 0:
        arr = np.append(arr, np.zeros(distance))  # zero padding
        """add a mechanism of transmitting number of zeros added"""

    # Generate time vector for one symbol
    t = np.linspace(0, symbol_time, samples_per_symbol, endpoint=False)

    # Define frequencies for FSK modulation
    f0 = fc - (fc / 4)  # Frequency for binary 10
    f1 = fc + (fc / 4)  # Frequency for binary 11
    f2 = fc - (fc / 8)  # Frequency for binary 01
    f3 = fc + (fc / 8)  # Frequency for binary 00

    # symbol dictionary
    symbol_dict = {
        (0, 1): f2,
        (0, 0): f3,
        (1, 1): f1,
        (1, 0): f0
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


def generate_signal_bps(arr: np.ndarray, filename: str) -> None:
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
    signal = generate_wave_bps(arr)
    wavfile.write(f'records/{filename}', fs, (signal * 32767).astype(np.int16))
