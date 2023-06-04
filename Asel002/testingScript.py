import socket
import threading
import pyaudio

client = socket.socket()

host = "35.164.39.119"
port = 5000

client.connect((host, port))

pyAudioIns = pyaudio.PyAudio()

Format = pyaudio.paInt16
Chunks = 4096
Channels = 2
Rate = 44100

inputStream = pyAudioIns.open(format=Format, channels=Channels, rate=Rate, input=True, frames_per_buffer=Chunks)

outputStream = pyAudioIns.open(format=Format, channels=Channels, rate=Rate, output=True, frames_per_buffer=Chunks)


def send():
    while True:
        try:
            data = inputStream.read(Chunks)
            client.send(data)
        except:
            break


def receive():
    while True:
        try:
            data = client.recv(Chunks)
            outputStream.write(data)
        except:
            break


t1 = threading.Thread(target=send)
t2 = threading.Thread(target=receive)

t1.start()
t2.start()

t1.join()
t2.join()

inputStream.stop()
inputStream.close()
outputStream.stop()
outputStream.close()
pyAudioIns.terminate()
