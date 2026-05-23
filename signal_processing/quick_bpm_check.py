import serial
import time
import numpy as np
from scipy.signal import find_peaks

PORT = 'COM3'
BAUD_RATE = 115200

ser = serial.Serial(PORT, BAUD_RATE, timeout=1)
time.sleep(2)
print('Counting peaks for 10 seconds... sit still!')

data = []
start = time.time()
while time.time() - start < 10:
    line = ser.readline().decode('utf-8').strip()
    try:
        data.append(int(line))
    except:
        pass

ser.close()

if len(data) > 0:
    peaks, _ = find_peaks(data, distance=300, height=max(data)*0.85)
    bpm = len(peaks) * 6
    print(f'Peaks counted: {len(peaks)}')
    print(f'Estimated BPM: {bpm}')
else:
    print('No data received — check connections')