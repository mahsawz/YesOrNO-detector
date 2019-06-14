#!/usr/bin/env python3
from scipy.io import wavfile as wav
import pyaudio
import wave
import numpy as np
import matplotlib.pyplot as plt

while True :
    FORMAT = pyaudio.paInt16  # format of sampling 16 bit int
    CHANNELS = 1  # number of channels it means number of sample in every sampling
    RATE = 44100  # number of sample in 1 second sampling
    CHUNK = 1024  # length of every chunk
    RECORD_SECONDS = 1  # time of recording in seconds
    WAVE_OUTPUT_FILENAME = "file.wav"  # file name

    audio = pyaudio.PyAudio()

    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    print("recording...")
    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("finished recording")

    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # storing voice
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

    # reading voice
    rate, data = wav.read('file.wav')

    fftList = np.fft.fft(data)
    half_fftList = []
    for item in range(10, int(len(fftList) / 2)):
        half_fftList.append(abs(fftList[item]))

    low = 0
    for i in range(0, 2000):
        low += half_fftList[i]

    high = 0
    for i in range(2000, len(half_fftList)):
        high += half_fftList[i]

    energy = np.sum(half_fftList)
    lowRate = low / energy
    highRate = high / energy

    if 1.0 > lowRate > 0.85 and 0.1 > highRate > 0.0:
        print("NO")
    elif 0.7 > highRate > 0.6 and 0.4 > lowRate > 0.2:
        print("MUTE")
    else:
        print("YES")

    # plt.plot(half_fftList)
    # plt.show()
