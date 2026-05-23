import numpy as np
from scipy.signal import butter, filtfilt, find_peaks
import pandas as pd
import matplotlib.pyplot as plt

def butter_bandpass_filter(data, lowcut=0.5, highcut=40.0, fs=533, order=4):
    nyq = 0.5 * fs
    b, a = butter(order, [lowcut / nyq, highcut / nyq], btype='band')
    return filtfilt(b, a, data)

# Load data
df = pd.read_csv('../results/experiment_1/resting_trial_3.csv')
raw = df['ecg_value'].values.astype(float)
timestamps = df['timestamp'].values

# Preprocess
skip = int(2 * 533)
raw = -np.clip(raw[skip:], np.percentile(raw[skip:], 1), np.percentile(raw[skip:], 99))
timestamps = timestamps[skip:]

# Filter
filtered = butter_bandpass_filter(raw)

# Detect R-peaks
peaks, _ = find_peaks(filtered, distance=int(0.6 * 533),
                      height=np.median(filtered) + 0.5 * np.std(filtered))

# Plot — first 10 seconds
s = 533 * 10
plt.figure(figsize=(14, 5))
plt.plot(timestamps[:s], filtered[:s], color='green', linewidth=1.0, label='Filtered ECG')
plt.plot(timestamps[peaks[peaks < s]], filtered[peaks[peaks < s]],
         'rv', markersize=10, label='R-peaks')
plt.title('ECG Signal — Butterworth Bandpass Filter + R-Peak Detection')
plt.xlabel('Time (seconds)')
plt.ylabel('ADC Value')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('ecg_filtered_peaks.png', dpi=150)
plt.show()