import random


def encode_mvp(data: list[int]) -> list[int]:
    """
    Encodes the given binary array with naive error correction encoding.
    This function takes a binary array as input and applies an error correction
    encoding mechanism to produce a new binary array with redundancy for error detection/correction.
    Args:
        data (list[int]): The binary array to be encoded.
    Returns:
        list[int]: The encoded binary array with error correction.
    """

    encoded_data = []
    for i in range(0, len(data), 2):
        bit_pair = [data[i], data[i+1]]
        encoded_data.extend(bit_pair)
        encoded_data.extend(bit_pair)
        encoded_data.extend(bit_pair)
    return encoded_data


def decode_mvp(encoded_data: list[int]) -> list[int]:
    """
    Decodes the given binary array with naive error correction decoding.
    This function takes a binary array as input and applies an error correction
    decoding mechanism to produce a new binary array with the original data.
    Args:
        data (list[int]): The binary array to be decoded.
    Returns:
        list[int]: The decoded binary array with the original data.
    """
    data = []
    for i in range(0, len(encoded_data), 6):
        pair_1 = [encoded_data[i], encoded_data[i+1]]
        pair_2 = [encoded_data[i+2], encoded_data[i+3]]
        pair_3 = [encoded_data[i + 4], encoded_data[i + 5]]
        if pair_1 == pair_2:
            data.extend(pair_1)
        else:
            if pair_1 == pair_3:
                data.extend(pair_1)
            elif pair_2 == pair_3:
                data.extend(pair_2)
            else:
                random_pair = random.choice([pair_1, pair_2, pair_3])
                data.extend(random_pair)
    return data


def encode_hamming(data: list[int]) -> list[int]:
    """
    Encodes the given binary array with hamming SECDED error correction encoding.
    This function takes a binary array as input and applies an error correction
    encoding mechanism to produce a new binary array with redundancy for error detection/correction.
    Args:
        data (list[int]): The binary array to be encoded.
    Returns:
        list[int]: The encoded binary array with error correction.
    """
    encoded_data = []
    for i in range(0, len(data), 4):
        # data bits
        d1 = data[i]
        d2 = data[i+1]
        d3 = data[i + 2]
        d4 = data[i + 3]

        # parity bits
        p1 = d1 ^ d2 ^ d3
        p2 = d1 ^ d2 ^ d4
        p3 = d4 ^ d2 ^ d3

        # global parity bit
        p_global = d1 ^ d2 ^ d3 ^ d4 ^ p1 ^ p2 ^ p3

        encoded_bits = [p1, p2, d1, p3, d2, d3, d4, p_global]
        encoded_data.extend(encoded_bits)

    return encoded_data


def decode_hamming(encoded_data: list[int]) -> list[int]:
    """
    Decodes the given binary array with hamming SECDED error correction decoding,
    tries to guess two-bit errors if detected.
    """
    decoded_data = []

    syndrome_table = {
        (0, 0, 0): None,  # no error
        (1, 0, 0): 0,     # p1
        (0, 1, 0): 1,     # p2
        (0, 0, 1): 3,     # p3
        (1, 1, 0): 2,     # d1
        (1, 0, 1): 4,     # d2
        (0, 1, 1): 5,     # d3
        (1, 1, 1): 6,     # d4
    }

    for i in range(0, len(encoded_data), 8):
        block = encoded_data[i:i+8]

        p1 = block[0]
        p2 = block[1]
        d1 = block[2]
        p3 = block[3]
        d2 = block[4]
        d3 = block[5]
        d4 = block[6]
        p_global = block[7]

        # Check parities
        p1_calc = d1 ^ d2 ^ d3
        p2_calc = d1 ^ d2 ^ d4
        p3_calc = d2 ^ d3 ^ d4
        p_global_calc = p1 ^ p2 ^ p3 ^ d1 ^ d2 ^ d3 ^ d4

        p1_wrong = p1 != p1_calc
        p2_wrong = p2 != p2_calc
        p3_wrong = p3 != p3_calc
        p_global_wrong = p_global != p_global_calc

        syndrome = (p1_wrong, p2_wrong, p3_wrong)

        if not p_global_wrong:
            # Single bit error → correct it
            error_bit = syndrome_table.get(syndrome)
            if error_bit is not None:
                block[error_bit] ^= 1  # flip the wrong bit
        else:
            # Double bit error detected
            print(f"Double bit error detected between bits {i} and {i+8} — guessing...")

            # Try educated guesses for two-bit flips
            if syndrome == (1, 0, 0):
                # Maybe d3 and d4 flipped
                block[5] ^= 1  # d3
                block[6] ^= 1  # d4
            elif syndrome == (0, 1, 0):
                # Maybe d2 and d4 flipped
                block[4] ^= 1  # d2
                block[6] ^= 1  # d4
            elif syndrome == (0, 0, 1):
                # Maybe d1 and d2 flipped
                block[2] ^= 1  # d1
                block[4] ^= 1  # d2
            elif syndrome == (1, 1, 0):
                # Maybe d1 and d3 flipped
                block[2] ^= 1  # d1
                block[5] ^= 1  # d3
            elif syndrome == (1, 0, 1):
                # Maybe d1 and d4 flipped
                block[2] ^= 1  # d1
                block[6] ^= 1  # d4
            elif syndrome == (0, 1, 1):
                # Maybe d2 and d3 flipped
                block[4] ^= 1  # d2
                block[5] ^= 1  # d3
            elif syndrome == (1, 1, 1):
                # Maybe p2 and p3 flipped
                block[1] ^= 1  # p2
                block[3] ^= 1  # p3
            else:
                print("Cannot guess the two flipped bits!")

        # Extract corrected data bits
        corrected_bits = [block[2], block[4], block[5], block[6]]
        decoded_data.extend(corrected_bits)

    return decoded_data