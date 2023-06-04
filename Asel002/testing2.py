import pyaudio
import wave

# Path to your wav file
filename = 'twoOfUs.wav'

# Open the file
wf = wave.open(filename, 'rb')

# Create a PyAudio instance
p = pyaudio.PyAudio()

# Open a stream
channels = 1
rate = 48000
Format = pyaudio.paInt16
chunks = 1024
stream = p.open(format=Format, channels=channels, rate=rate, output=True, frames_per_buffer=chunks)

# Read data from the file
data = wf.readframes(1024)

# Play the file
while len(data) > 0:
    stream.write(data)
    data = wf.readframes(1024)

    print(data)

# Close the stream
stream.stop_stream()
stream.close()

# Close PyAudio
p.terminate()
