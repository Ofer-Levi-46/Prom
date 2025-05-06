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

def decode(data: np.ndarray) -> np.ndarray:
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
        # print(f"Processing block {i//8}")
        block = data[i:i + 8]
        if len(block) < 8:
            continue

        # Make a copy of the block to avoid modifying the original bits
        block = block.copy()

        # assign bits to variables
        p1, p2, d1, p3, d2, d3, d4, p_global = block
        

        # Recalculate parity bits
        p1_calc = d1 ^ d2 ^ d3
        p2_calc = d1 ^ d2 ^ d4
        p3_calc = d2 ^ d3 ^ d4
        p_global_calc = p1_calc ^ p2_calc ^ p3_calc ^ d1 ^ d2 ^ d3 ^ d4

        # Check for errors
        s1 = int(p1 != p1_calc)
        s2 = int(p2 != p2_calc)
        s3 = int(p3 != p3_calc)
        error_syndrome = (s1, s2, s3)
        syndrome_to_index = {
        (0, 0, 1): 0,  # p3
        (0, 1, 0): 1,  # p2
        (0, 1, 1): 2,  # d4
        (1, 0, 0): 3,  # p1
        (1, 0, 1): 4,  # d3
        (1, 1, 0): 5,  # d1
        (1, 1, 1): 6,   # d2
        (0, 0, 0): 7   # p global
        }
        # Correct single-bit errors
        if p_global != p_global_calc:
            error_index = syndrome_to_index[error_syndrome]
            block[error_index] ^= 1
        #guess two-bit errors
        else:
            if error_syndrome == (0, 0, 0):
                pass
            elif error_syndrome == (1, 0, 0):
                block[6] ^= 1  # d4
                block[4] ^= 1  # d2
            elif error_syndrome == (0, 1, 0):
                block[5] ^= 1  # d3
                block[4] ^= 1  # d2
            elif error_syndrome == (0, 0, 1):
                block[2] ^= 1  # d1
                block[4] ^= 1  # d2
            elif error_syndrome == (1, 1, 0):
                block[5] ^= 1  # d3
                block[6] ^= 1  # d4
            elif error_syndrome == (1, 0, 1):
                block[2] ^= 1  # d1
                block[4] ^= 1  # d2              
            elif error_syndrome == (0, 1, 1):
                block[2] ^= 1  # d1
                block[5] ^= 1  # d3
            else:
                pass  # no guess possible
            
        # Extract original data bits
        # print("Decoded block:",[block[2], block[4], block[5], block[6]]) 
        decoded_data.extend([block[2], block[4], block[5], block[6]])
        # print("Decoded data:", decoded_data)
    
    return np.array(decoded_data, dtype=int)