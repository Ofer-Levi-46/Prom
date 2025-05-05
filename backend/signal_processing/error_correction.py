import numpy as np

def encode(data: list[float]) -> list[float]:
    """
    Encodes the given binary array with Hamming SECDED error correction encoding.
    This function takes a binary NumPy array as input and applies an error correction
    encoding mechanism to produce a new binary array with redundancy for error detection/correction.

    Args:
        data (np.ndarray): The binary array to be encoded.
    Returns:
        np.ndarray: The encoded binary array with error correction.
    """
   
    encoded_data = []

    for i in range(0, len(data), 4):
        block = data[i:i + 4]
        d1 = block[0] if len(block) > 0 else 0
        d2 = block[1] if len(block) > 1 else 0
        d3 = block[2] if len(block) > 2 else 0
        d4 = block[3] if len(block) > 3 else 0

        # Calculate parity bits
        p1 = d1 ^ d2 ^ d3
        p2 = d1 ^ d2 ^ d4
        p3 = d2 ^ d3 ^ d4
        p_global = p1 ^ p2 ^ p3 ^ d1 ^ d2 ^ d3 ^ d4

        # Construct encoded block
        encoded_block = [p1, p2, d1, p3, d2, d3, d4, p_global]
        encoded_data.extend(encoded_block)

    return np.array(encoded_data, dtype=int)


def decode(data: list[float]) -> list[float]:
    """
    Decodes the given binary array with Hamming SECDED error correction decoding,
    tries to guess two-bit errors if detected.

    Args:
        encoded_data (np.ndarray): The binary array to be decoded.
    Returns:
        np.ndarray: The decoded binary array with the original data.
    """
    
    decoded_data = []

    for i in range(0, len(data), 8):
        block = data[i:i + 8]
        if len(block) < 8:
            continue

        p1, p2, d1, p3, d2, d3, d4, p_global = block

        # Recalculate parity bits
        p1_calc = d1 ^ d2 ^ d3
        p2_calc = d1 ^ d2 ^ d4
        p3_calc = d2 ^ d3 ^ d4
        p_global_calc = p1_calc ^ p2_calc ^ p3_calc ^ d1 ^ d2 ^ d3 ^ d4

        # Check for errors
        error_syndrome = (p1 != p1_calc) << 2 | (p2 != p2_calc) << 1 | (p3 != p3_calc)

        if p_global != p_global_calc:
            if error_syndrome > 0 and error_syndrome <= 7:
                block[error_syndrome - 1] ^= 1  # Correct the single-bit error
            else:
                # Two-bit error detected, cannot correct
                pass

        # Extract original data bits
        decoded_data.extend([block[2], block[4], block[5], block[6]])

    return np.array(decoded_data, dtype=int)
