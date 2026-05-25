import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from filters import full_pipeline
from scipy.signal import find_peaks

def plot_raw_vs_filtered(trial_num, fs=533):
    df = pd.read_csv(f'../results/experiment_1/resting_trial_{trial_num}.csv')
    raw = df['ecg_value'].values.astype(float)
    timestamps = df['timestamp'].values
    skip = int(2 * fs)
    raw = raw[skip:]
    timestamps = timestamps[skip:]
    raw = np.clip(raw, np.percentile(raw, 1), np.percentile(raw, 99))
    raw = -raw
    filtered = full_pipeline(raw, fs=fs)
    filtered = (filtered - np.mean(filtered)) / np.std(filtered)
    peaks, _ = find_peaks(filtered, distance=int(0.6*fs), height=np.median(filtered)+0.5*np.std(filtered))
    samples = fs * 10
    t = timestamps[:samples]
    peaks_in_window = peaks[peaks < samples]
    fig, axes = plt.subplots(2, 1, figsize=(14, 8))
    axes[0].plot(t, raw[:samples], color='gray', linewidth=0.8, label='Raw Signal')
    axes[0].set_title(f'Trial {trial_num} - Raw Signal')
    axes[0].set_ylabel('ADC Value')
    axes[0].grid(True)
    axes[0].legend()
    axes[1].plot(t, filtered[:samples], color='green', linewidth=0.8, label='Filtered+Normalized')
    if len(peaks_in_window) > 0:
        axes[1].plot(timestamps[peaks_in_window], filtered[peaks_in_window], 'rv', markersize=10, label='R-peaks')
    axes[1].set_title(f'Trial {trial_num} - Filtered+Normalized with R-Peaks')
    axes[1].set_ylabel('Normalized Amplitude')
    axes[1].set_xlabel('Time in seconds')
    axes[1].grid(True)
    axes[1].legend()
    plt.suptitle(f'Resting Trial {trial_num} - Raw vs Filtered', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f'../results/experiment_1/raw_vs_filtered_trial_{trial_num}.png', dpi=150)
    print(f'Trial {trial_num} complete')
    plt.show()

for trial in range(1, 6):
    try:
        plot_raw_vs_filtered(trial)
    except Exception as e:
        print(f'Trial {trial} error: {e}')
