import pandas as pd
import numpy as np
from scipy.signal import butter, filtfilt, iirnotch
import matplotlib.pyplot as plt

# ── FILTER FUNCTIONS ──────────────────────────────────────────

def butter_bandpass(data, lowcut=0.5, highcut=40.0, fs=500, order=4):
    """Butterworth bandpass filter — removes baseline drift and high-freq noise"""
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return filtfilt(b, a, data)

def notch_filter(data, freq=60.0, fs=500, quality=30):
    """60Hz notch filter — removes powerline interference"""
    b, a = iirnotch(freq / (0.5 * fs), quality)
    return filtfilt(b, a, data)

def moving_average(data, window=5):
    """Simple moving average — baseline comparison algorithm"""
    return np.convolve(data, np.ones(window)/window, mode='same')

def full_pipeline(data, fs=500):
    """Complete 3-stage filter pipeline"""
    step1 = butter_bandpass(data, fs=fs)
    step2 = notch_filter(step1, fs=fs)
    return step2

# ── NOISE METRIC ──────────────────────────────────────────────

def compute_snr(raw, filtered):
    """Signal-to-Noise Ratio in dB"""
    signal_power = np.var(filtered)
    noise_power = np.var(raw - filtered)
    if noise_power == 0:
        return float('inf')
    return round(10 * np.log10(signal_power / noise_power), 2)

# ── MAIN: LOAD + FILTER + PLOT ────────────────────────────────

def main():
    # Load CSV
    print("Loading data...")
    df = pd.read_csv('../results/experiment_1/resting_trial_1.csv')
    raw = df['ecg_value'].values
    timestamps = df['timestamp'].values
    fs = 500

    # Apply all three filters
    print("Applying filters...")
    filtered_ma = moving_average(raw, window=5)
    filtered_butter = butter_bandpass(raw, fs=fs)
    filtered_full = full_pipeline(raw, fs=fs)

    # Compute SNR for each
    snr_ma = compute_snr(raw, filtered_ma)
    snr_butter = compute_snr(raw, filtered_butter)
    snr_full = compute_snr(raw, filtered_full)

    print(f"SNR - Moving Average:      {snr_ma} dB")
    print(f"SNR - Butterworth only:    {snr_butter} dB")
    print(f"SNR - Butterworth + Notch: {snr_full} dB")

    # Plot — show first 5 seconds only for clarity
    samples = fs * 5
    t = timestamps[:samples]

    plt.figure(figsize=(14, 10))

    plt.subplot(4, 1, 1)
    plt.plot(t, raw[:samples], color='gray', linewidth=0.8)
    plt.title('Raw Signal (Unfiltered)')
    plt.ylabel('ADC Value')
    plt.grid(True)

    plt.subplot(4, 1, 2)
    plt.plot(t, filtered_ma[:samples], color='orange', linewidth=0.8)
    plt.title(f'Moving Average Filter (SNR: {snr_ma} dB)')
    plt.ylabel('ADC Value')
    plt.grid(True)

    plt.subplot(4, 1, 3)
    plt.plot(t, filtered_butter[:samples], color='blue', linewidth=0.8)
    plt.title(f'Butterworth Bandpass Only (SNR: {snr_butter} dB)')
    plt.ylabel('ADC Value')
    plt.grid(True)

    plt.subplot(4, 1, 4)
    plt.plot(t, filtered_full[:samples], color='green', linewidth=0.8)
    plt.title(f'Butterworth + Notch Filter (SNR: {snr_full} dB)')
    plt.ylabel('ADC Value')
    plt.xlabel('Time (seconds)')
    plt.grid(True)

    plt.tight_layout()
    plt.savefig('../results/experiment_3/filter_comparison.png', dpi=150)
    print("Plot saved to results/experiment_3/filter_comparison.png")
    plt.show()

if __name__ == "__main__":
    main()
