import numpy as np
import matplotlib.pyplot as plt

def poincare_plot(peaks, fs=533):
    """
    Poincaré plot — standard HRV visualization.
    Plots RR(n) vs RR(n+1) to show HRV pattern.
    """
    rr = np.diff(peaks) / fs * 1000  # RR intervals in ms
    plt.figure(figsize=(6, 6))
    plt.scatter(rr[:-1], rr[1:], alpha=0.5, color='blue', s=20)
    plt.xlabel('RR(n) ms')
    plt.ylabel('RR(n+1) ms')
    plt.title('Poincaré Plot — HRV Analysis')
    plt.grid(True)
    plt.savefig('../results/experiment_1/poincare_plot.png', dpi=150)
    plt.show()

def hrv_recovery_curve(resting_hrv, exercise_hrv, recovery_hrv):
    """
    Plot HRV recovery across physiological states.
    """
    states = ['Resting', 'Post-Exercise', 'Recovery']
    sdnn = [resting_hrv['SDNN_ms'], 
            exercise_hrv['SDNN_ms'], 
            recovery_hrv['SDNN_ms']]
    rmssd = [resting_hrv['RMSSD_ms'], 
             exercise_hrv['RMSSD_ms'], 
             recovery_hrv['RMSSD_ms']]

    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.plot(states, sdnn, 'bo-', linewidth=2, markersize=8)
    plt.title('SDNN Across States')
    plt.ylabel('SDNN (ms)')
    plt.grid(True)

    plt.subplot(1, 2, 2)
    plt.plot(states, rmssd, 'ro-', linewidth=2, markersize=8)
    plt.title('RMSSD Across States')
    plt.ylabel('RMSSD (ms)')
    plt.grid(True)

    plt.tight_layout()
    plt.savefig('../results/experiment_1/hrv_recovery_curve.png', dpi=150)
    plt.show()