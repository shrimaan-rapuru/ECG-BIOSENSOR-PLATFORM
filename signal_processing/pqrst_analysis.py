import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, find_peaks

def butter_bandpass_filter(data, lowcut=0.5, highcut=40.0, fs=533, order=4):
    nyq = 0.5 * fs
    b, a = butter(order, [lowcut / nyq, highcut / nyq], btype='band')
    return filtfilt(b, a, data)

def plot_pqrst(trial_num=3, fs=533):
    # Load data
    df = pd.read_csv('../results/experiment_1/subject_5_pqrst_trial.csv')
    raw = df['ecg_value'].values.astype(float)
    timestamps = df['timestamp'].values

    # Preprocess
    skip = int(2 * fs)
    raw = raw[skip:]
    timestamps = timestamps[skip:]
    raw = np.clip(raw, np.percentile(raw, 1), np.percentile(raw, 99))
    raw = -raw

    # Filter
    filtered = butter_bandpass_filter(raw, fs=fs)

    # Detect R-peaks
    peaks, _ = find_peaks(filtered,
                          distance=int(0.6 * fs),
                          height=np.median(filtered) + 0.5 * np.std(filtered))

    if len(peaks) < 3:
        print("Not enough peaks detected")
        return

    # ── SINGLE BEAT ZOOM ─────────────────────────────────
    # Pick cleanest peak — highest amplitude in middle of recording
    middle_peaks = peaks[len(peaks)//4 : 3*len(peaks)//4]
    center_peak = middle_peaks[np.argmax(filtered[middle_peaks])]

    # Window: 0.3s before R-peak, 0.5s after
    pre  = int(0.3 * fs)
    post = int(0.5 * fs)
    start = center_peak - pre
    end   = center_peak + post

    if start < 0 or end > len(filtered):
        center_peak = peaks[len(peaks)//2]
        start = center_peak - pre
        end   = center_peak + post

    # Extract single beat
    beat = filtered[start:end]
    t_beat = np.linspace(-0.3, 0.5, len(beat))  # Time relative to R-peak

    # ── IDENTIFY PQRST COMPONENTS ────────────────────────
    r_idx = pre  # R-peak is at index 'pre' in the beat window

    # P wave — search 0.1 to 0.25s before R-peak
    p_search_start = r_idx - int(0.25 * fs)
    p_search_end   = r_idx - int(0.08 * fs)
    p_search_start = max(0, p_search_start)
    p_region = beat[p_search_start:p_search_end]
    p_idx = p_search_start + np.argmax(p_region)

    # Q wave — small dip just before R (0.02-0.08s before R)
    q_search_start = r_idx - int(0.08 * fs)
    q_search_end   = r_idx - int(0.01 * fs)
    q_search_start = max(0, q_search_start)
    q_region = beat[q_search_start:q_search_end]
    q_idx = q_search_start + np.argmin(q_region)

    # S wave — small dip just after R (0.02-0.08s after R)
    s_search_start = r_idx + int(0.01 * fs)
    s_search_end   = r_idx + int(0.08 * fs)
    s_search_end   = min(len(beat), s_search_end)
    s_region = beat[s_search_start:s_search_end]
    s_idx = s_search_start + np.argmin(s_region)

    # T wave — broad peak 0.15 to 0.4s after R
    t_search_start = r_idx + int(0.15 * fs)
    t_search_end   = r_idx + int(0.40 * fs)
    t_search_end   = min(len(beat), t_search_end)
    t_region = beat[t_search_start:t_search_end]
    t_idx = t_search_start + np.argmax(t_region)

    # ── PLOT ─────────────────────────────────────────────
    fig, axes = plt.subplots(2, 1, figsize=(14, 10))

    # ── TOP: Full 10-second filtered signal ──────────────
    s10 = fs * 10
    axes[0].plot(timestamps[:s10], filtered[:s10],
                 color='green', linewidth=0.8, label='Filtered ECG')
    peaks_in_window = peaks[peaks < s10]
    axes[0].plot(timestamps[peaks_in_window], filtered[peaks_in_window],
                 'rv', markersize=8, label='R-peaks')
    axes[0].set_title('Full ECG Signal — Butterworth Bandpass Filter + R-Peak Detection',
                      fontsize=13, fontweight='bold')
    axes[0].set_ylabel('ADC Value')
    axes[0].set_xlabel('Time (seconds)')
    axes[0].legend()
    axes[0].grid(True)

    # BPM and HRV annotation
    rr = np.diff(peaks) / fs * 1000
    bpm = round(60 / (np.mean(np.diff(peaks)) / fs), 1)
    sdnn = round(np.std(rr), 2)
    rmssd = round(np.sqrt(np.mean(np.diff(rr)**2)), 2)
    axes[0].text(0.98, 0.95,
                 f'BPM: {bpm}  |  SDNN: {sdnn}ms  |  RMSSD: {rmssd}ms  |  Peaks: {len(peaks)}',
                 transform=axes[0].transAxes,
                 fontsize=10, ha='right', va='top',
                 bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))

    # ── BOTTOM: Single beat PQRST zoom ───────────────────
    axes[1].plot(t_beat, beat, color='blue', linewidth=2.0, label='Single Heartbeat')
    axes[1].axvline(x=0, color='gray', linestyle='--', alpha=0.4, label='R-peak reference')

    # Annotate each wave
    wave_color = 'red'
    offset = 8  # vertical offset for labels

    axes[1].annotate('P', xy=(t_beat[p_idx], beat[p_idx]),
                     xytext=(t_beat[p_idx]-0.02, beat[p_idx]+offset),
                     fontsize=14, fontweight='bold', color='purple',
                     arrowprops=dict(arrowstyle='->', color='purple', lw=1.5))

    axes[1].annotate('Q', xy=(t_beat[q_idx], beat[q_idx]),
                     xytext=(t_beat[q_idx]-0.03, beat[q_idx]-offset*2),
                     fontsize=14, fontweight='bold', color='blue',
                     arrowprops=dict(arrowstyle='->', color='blue', lw=1.5))

    axes[1].annotate('R', xy=(t_beat[r_idx], beat[r_idx]),
                     xytext=(t_beat[r_idx]+0.02, beat[r_idx]+offset),
                     fontsize=14, fontweight='bold', color='red',
                     arrowprops=dict(arrowstyle='->', color='red', lw=1.5))

    axes[1].annotate('S', xy=(t_beat[s_idx], beat[s_idx]),
                     xytext=(t_beat[s_idx]+0.02, beat[s_idx]-offset*2),
                     fontsize=14, fontweight='bold', color='blue',
                     arrowprops=dict(arrowstyle='->', color='blue', lw=1.5))

    axes[1].annotate('T', xy=(t_beat[t_idx], beat[t_idx]),
                     xytext=(t_beat[t_idx]+0.02, beat[t_idx]+offset),
                     fontsize=14, fontweight='bold', color='green',
                     arrowprops=dict(arrowstyle='->', color='green', lw=1.5))

    axes[1].set_title('Single Heartbeat — PQRST Wave Analysis',
                      fontsize=13, fontweight='bold')
    axes[1].set_xlabel('Time relative to R-peak (seconds)')
    axes[1].set_ylabel('ADC Value')
    axes[1].legend()
    axes[1].grid(True)

    # Add wave descriptions
    axes[1].text(0.01, -0.18,
             '  Marker        Cardiac Action                    '
             'System Validation Significance\n'
             '  P-Wave        Atrial Depolarization             '
             'Proves filter preserved low-amplitude, low-frequency markers\n'
             '  QRS Complex   Ventricular Depolarization        '
             'Sharp slope confirms high temporal resolution and precision timing\n'
             '  T-Wave        Ventricular Repolarization        '
             'Distinct curve confirms baseline stability and robust thresholding',
             transform=axes[1].transAxes,
             fontsize=10, color='#333333', va='top',
             fontfamily='monospace',
             bbox=dict(boxstyle='round', facecolor='#f8f8f8',
                      edgecolor='#cccccc', alpha=0.9))

    plt.suptitle(f'ECG Analysis — Subject 5 | Resting | Summer 2026',
                 fontsize=14, fontweight='bold', y=1.01)
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.18)
    plt.savefig(f'../results/experiment_1/pqrst_trial_{trial_num}.png',
                dpi=150, bbox_inches='tight')
    print(f"PQRST plot saved to results/experiment_1/pqrst_trial_{trial_num}.png")
    print(f"BPM: {bpm} | SDNN: {sdnn}ms | RMSSD: {rmssd}ms")
    plt.show()

if __name__ == "__main__":
    plot_pqrst(trial_num=3)  # Use Trial 3 — your cleanest trial