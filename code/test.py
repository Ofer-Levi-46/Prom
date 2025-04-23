import base.QPSK as qpsk
import errors.error_correction as ec


# ENCODE
data = qpsk.string_to_bits("Hello World")
encoded = ec.encode(data)
qpsk.generate_signal(encoded, "output.wav")


# DECODE
data = qpsk.read_signal("noisy_output.wav") # noisy_output.wav is a noisy version of output.wav. You can create it by recording the output.wav file with a microphone.
decoded = ec.decode(data)
print(f"Original: {data}")