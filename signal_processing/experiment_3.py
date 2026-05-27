import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, iirnotch, find_peaks
import time

def butter_bandpass(data, lowcut=0.5, highcut=40.0, fs=533, order=4):
    nyq = 0.5 * fs
    b, a = butter(order, [lowcut/nyq, highcut/nyq], btype='band')
    return filtfilt(b, a, data)

def notch_filter(data, freq=60.0, fs=533, quality=30):
    nyq = 0.5 * fs
    b, a = iirnotch(freq/nyq, quality)
    return filtfilt(b, a, data)

def moving_average(data, window=5):
    return np.convolve(data, np.ones(window)/window, mode='same')

def full_pipeline(data, fs=533):
    return notch_filter(butter_bandpass(data, fs=fs), fs=fs)

def compute_snr(raw, filtered):
    signal_power = np.var(filtered)
    noise_power = np.var(raw - filtered)
    if noise_power == 0:
        return float('inf')
    return round(10 * np.log10(signal_power / noise_power), 2)

def compute_bpm(filtered, fs=533):
    peaks, _ = find_peaks(filtered,
                          distance=int(0.6*fs),
                          height=np.median(filtered)+0.5*np.std(filtered))
    if len(peaks) < 2:
        return 0, len(peaks)
    bpm = round(60 / (np.mean(np.diff(peaks)) / fs), 1)
    return bpm, len(peaks)

def analyze_trial(trial_num, fs=533):
    df = pd.read_csv(f'../results/experiment_1/resting_trial_{trial_num}.csv')
    raw = df['ecg_value'].values.astype(float)
    skip = int(2 * fs)
    raw = raw[skip:]
    raw = np.clip(raw, np.percentile(raw, 1), np.percentile(raw, 99))
    raw = -raw

    results = {}

    # Algorithm 1 — Moving Average
    t1 = time.time()
    ma = moving_average(raw, window=5)
    ma_time = round((time.time() - t1) * 1000, 2)
    ma_snr = compute_snr(raw, ma)
    ma_bpm, ma_peaks = compute_bpm(ma, fs)
    results['Moving Average'] = {
        'SNR_dB': ma_snr,
        'BPM': ma_bpm,
        'Peaks': ma_peaks,
        'Time_ms': ma_time
    }

    # Algorithm 2 — Butterworth only
    t2 = time.time()
    butter_only = butter_bandpass(raw, fs=fs)
    butter_time = round((time.time() - t2) * 1000, 2)
    butter_snr = compute_snr(raw, butter_only)
    butter_bpm, butter_peaks = compute_bpm(butter_only, fs)
    results['Butterworth'] = {
        'SNR_dB': butter_snr,
        'BPM': butter_bpm,
        'Peaks': butter_peaks,
        'Time_ms': butter_time
    }

    # Algorithm 3 — Full pipeline
    t3 = time.time()
    full = full_pipeline(raw, fs=fs)
    full_time = round((time.time() - t3) * 1000, 2)
    full_snr = compute_snr(raw, full)
    full_bpm, full_peaks = compute_bpm(full, fs)
    results['Butterworth+Notch'] = {
        'SNR_dB': full_snr,
        'BPM': full_bpm,
        'Peaks': full_peaks,
        'Time_ms': full_time
    }

    return results

def main():
    print("Experiment 3 — Filter Algorithm Comparison")
    print("=" * 60)

    all_results = {}
    for trial in range(1, 6):
        print(f"\nAnalyzing Trial {trial}...")
        results = analyze_trial(trial)
        all_results[trial] = results
        for algo, metrics in results.items():
            print(f"  {algo:20s} SNR: {metrics['SNR_dB']:6.2f}dB | "
                  f"BPM: {metrics['BPM']:5.1f} | "
                  f"Peaks: {metrics['Peaks']:3d} | "
                  f"Time: {metrics['Time_ms']:5.2f}ms")

    # Summary table
    print("\n" + "=" * 60)
    print("SUMMARY — Mean ± SD across 5 trials")
    print("=" * 60)

    algorithms = ['Moving Average', 'Butterworth', 'Butterworth+Notch']
    summary = {}

    for algo in algorithms:
        snrs = [all_results[t][algo]['SNR_dB'] for t in range(1, 6)]
        bpms = [all_results[t][algo]['BPM'] for t in range(1, 6)]
        times = [all_results[t][algo]['Time_ms'] for t in range(1, 6)]
        summary[algo] = {
            'SNR_mean': round(np.mean(snrs), 2),
            'SNR_std': round(np.std(snrs), 2),
            'BPM_mean': round(np.mean(bpms), 2),
            'BPM_std': round(np.std(bpms), 2),
            'Time_mean': round(np.mean(times), 2),
        }
        print(f"{algo:22s} | SNR: {summary[algo]['SNR_mean']} ± {summary[algo]['SNR_std']}dB | "
              f"BPM: {summary[algo]['BPM_mean']} ± {summary[algo]['BPM_std']} | "
              f"Time: {summary[algo]['Time_mean']}ms")

    # Save results
    rows = []
    for trial in range(1, 6):
        for algo in algorithms:
            m = all_results[trial][algo]
            rows.append({
                'Trial': trial,
                'Algorithm': algo,
                'SNR_dB': m['SNR_dB'],
                'BPM': m['BPM'],
                'Peaks': m['Peaks'],
                'Time_ms': m['Time_ms']
            })

    df_results = pd.DataFrame(rows)
    df_results.to_csv('../results/experiment_3/algorithm_comparison.csv', index=False)
    print("\nSaved to results/experiment_3/algorithm_comparison.csv")

    # Plot
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    colors = ['orange', 'blue', 'green']
    metrics_to_plot = ['SNR_dB', 'BPM_mean', 'Time_mean']
    titles = ['SNR (dB)', 'Mean BPM', 'Processing Time (ms)']
    ylabels = ['dB', 'BPM', 'ms']

    snr_vals = [summary[a]['SNR_mean'] for a in algorithms]
    snr_stds = [summary[a]['SNR_std'] for a in algorithms]
    bpm_vals = [summary[a]['BPM_mean'] for a in algorithms]
    bpm_stds = [summary[a]['BPM_std'] for a in algorithms]
    time_vals = [summary[a]['Time_mean'] for a in algorithms]

    short_names = ['Moving\nAverage', 'Butterworth\nOnly', 'Butterworth\n+Notch']

    axes[0].bar(short_names, snr_vals, yerr=snr_stds,
                color=colors, alpha=0.8, capsize=5)
    axes[0].set_title('SNR Comparison (dB)\nHigher is better')
    axes[0].set_ylabel('SNR (dB)')
    axes[0].grid(True, alpha=0.3)

    axes[1].bar(short_names, bpm_vals, yerr=bpm_stds,
                color=colors, alpha=0.8, capsize=5)
    axes[1].set_title('Mean BPM Comparison\nCloser to 91.0 is better')
    axes[1].set_ylabel('BPM')
    axes[1].axhline(y=91.0, color='red', linestyle='--',
                    alpha=0.7, label='True resting BPM')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    axes[2].bar(short_names, time_vals, color=colors, alpha=0.8)
    axes[2].set_title('Processing Time (ms)\nLower is better')
    axes[2].set_ylabel('Time (ms)')
    axes[2].grid(True, alpha=0.3)

    plt.suptitle('Experiment 3 — Filter Algorithm Comparison\n'
                 '5 Resting Trials | Subject 2 | Summer 2026',
                 fontsize=13, fontweight='bold')
    plt.tight_layout()
    plt.savefig('../results/experiment_3/algorithm_comparison_plot.png',
                dpi=150, bbox_inches='tight')
    print("Plot saved to results/experiment_3/algorithm_comparison_plot.png")
    plt.show()

if __name__ == "__main__":
    main()