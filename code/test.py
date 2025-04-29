from base.helper import string_to_bits
from base.send_signal import generate_signal
from base.read_signal import read_signal
from base.record import record
import numpy as np
import wave
import matplotlib.pyplot as plt

# ENCODE
# data = string_to_bits("Hello World! My name is QPSK")
# generate_signal(data, "output.wav")

# record("record.wav", 5)  # Record audio for 5 seconds

# # DECODE
data = read_signal("record.wav")
decoded_string = ''.join(str(bit) for bit in data)
decoded_string = ''.join(chr(int(decoded_string[i:i+8], 2)) for i in range(0, len(decoded_string), 8))
print(f"Final: {decoded_string}")