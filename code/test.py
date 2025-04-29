import base.QPSK as qpsk
import errors.error_correction as ec
from base.record import record
import numpy as np
import wave


# ENCODE
# data = qpsk.string_to_bits("Hello World! My name is QPSK")
# qpsk.generate_signal(data, "output.wav")

# record("record.wav", 5)  # Record audio for 5 seconds

# DECODE
data = qpsk.read_signal("record.wav")
decoded_string = ''.join(str(bit) for bit in data)
decoded_string = ''.join(chr(int(decoded_string[i:i+8], 2)) for i in range(0, len(decoded_string), 8))
print(f"Final: {decoded_string}")