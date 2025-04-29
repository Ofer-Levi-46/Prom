from base.helper import string_to_bits
from base.send_signal import generate_signal
from base.read_signal import read_signal
from base.record import record
import numpy as np
import wave
import matplotlib.pyplot as plt
from base.bps_test import generate_signal_bps
from base.bps_test import read_signal_bps


# ENCODE
# data = string_to_bits("Hello World")
# generate_signal_bps(data, "output.wav")

# record("record.wav", 5)  # Record audio for 5 seconds

# DECODE
string = string_to_bits("Hello World")
data = read_signal_bps("record.wav")

# count how many bits in data are different from string
diff_count = sum(1 for i in range(len(data)) if data[i] != string[i])
print(f"Number of differing bits: {diff_count}")
# print(f"Success rate: {100 - (diff_count / len(data) * 100)}%")

decoded_string = ''.join(str(bit) for bit in data)
decoded_string = ''.join(chr(int(decoded_string[i:i+8], 2)) for i in range(0, len(decoded_string), 8))
print(f"Final string: {decoded_string}")