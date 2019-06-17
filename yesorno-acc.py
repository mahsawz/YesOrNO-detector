#!/usr/bin/env python3
from scipy.io import wavfile as wav
import pyaudio
import wave
import os
import numpy as np
import matplotlib.pyplot as plt


def YesNo(data):
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

    if 1.0 > lowRate > 0.6 and 0.3 > highRate > 0.1:
        return 'NO'
    elif 0.7 > lowRate > 0.3 and 0.8 > highRate > 0.3:
        return 'YES'
    else:
        return 'MUTE'


countAll = 0
countYes = 0
countNo = 0
fileNum = 0
fileNumber1 = 0
fileNumber2 = 0

di = 'train/'
for i in range(300):
    s = 'NO' + str(i) + '.wav'
    try:
        rate, data = wav.read(di + s)
        data = [item[0] for item in data]
        if YesNo(data) == 'NO':
            countNo += 1
        fileNumber1 += 1
    except:
        os.system('sox ' + di + s + ' corrected/' + s)

for i in range(300):
    s = 'YES' + str(i) + '.wav'
    try:
        rate, data = wav.read(di + s)
        data = [item[0] for item in data]
        if YesNo(data) == 'YES':
            countYes += 1
        fileNumber2 += 1
    except:
        os.system('sox ' + di + s + ' corrected/' + s)

print('NO: ', str(countNo / fileNumber1))
print('YES: ', str(countYes / fileNumber2))
print('ALL: ', str((countNo + countYes) / (fileNumber1 + fileNumber2)))
