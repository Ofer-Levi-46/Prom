import base.QPSK as qpsk
import errors.error_correction as ec
from base.record import record
import random


# ENCODE
# data = qpsk.string_to_bits("Hello World! My name is QPSK")
# print(f"Original: {data}")
# encoded = ec.encode_hamming(data)
# qpsk.generate_signal(encoded, "output.wav")

# record("record.wav", 5)  # Record audio for 5 seconds

# DECODE
data = qpsk.read_signal("record.wav")
decoded_data = ec.decode_hamming(data)
decoded_string = ''.join(str(bit) for bit in decoded_data)
decoded_string = ''.join(chr(int(decoded_string[i:i+8], 2)) for i in range(0, len(decoded_string), 8))
print(f"Final: {decoded_string}")