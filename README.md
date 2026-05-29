# Development and Evaluation of a Low-Cost Real-Time ECG Biosensing Platform

> Integrating Signal Processing, Robustness Analysis, and Physiological Visualization

**Shrimaan Rapuru** | The Early College at Guilford | Summer 2026  
[Live Dashboard](https://share.streamlit.io) | [Technical Report](report/) | [Results](results/)

---

## Abstract

This project investigates whether consumer-grade biosensing hardware can produce 
physiologically meaningful cardiac metrics through optimized signal processing — 
motivated by observed healthcare access inequality at Open Door Ministries, a 
homeless shelter where I volunteer. Using a SparkFun AD8232 ECG module and Arduino 
Uno R4 Minima ($102 total), I designed and validated a complete real-time ECG 
acquisition and analysis pipeline. A 4th-order Butterworth bandpass filter 
(0.5–40Hz) with IIR notch (60Hz) achieved visible PQRST morphology and 96.3% 
mean R-peak detection accuracy across five validated resting trials. Three 
structured experiments evaluated physiological response (resting vs. exercise vs. 
recovery), electrode placement robustness, and comparative filter algorithm 
performance. A key finding — that Moving Average filtering achieves higher SNR 
but lower detection reliability than Butterworth filtering — reveals that SNR 
alone is insufficient to evaluate ECG filter quality. Results suggest low-cost 
ECG acquisition is viable with careful signal processing methodology.

---

## Hero Figure

![PQRST Wave Analysis](results/experiment_1/pqrst_trial_3.png)

*Real-time ECG signal captured at 533Hz. All 5 PQRST waves clearly identified. 
BPM: 89.5 | SDNN: 17.63ms | RMSSD: 23.65ms | 42 peaks detected.*

---

## Why This Matters

Standard clinical ECG systems cost $1,000–$10,000, placing cardiac monitoring 
out of reach for many individuals and resource-limited settings. This project 
asks a practical engineering question: can a $102 consumer-grade system produce 
physiologically meaningful cardiac metrics with careful signal processing?

The answer — supported by validated experiments — is yes. Beyond the technical 
finding, this work demonstrates a broader principle: accessibility and rigor are 
not mutually exclusive. The same engineering discipline that produces expensive 
medical devices can be applied to low-cost hardware to yield credible, 
reproducible physiological measurements.

This project was motivated by direct observation of healthcare access inequality 
at Open Door Ministries, where I coordinate volunteer scheduling. Every system 
I build asks the same question I first asked there: how do we build tools that 
actually reach the people who need them most?

---

## Overview

Using a SparkFun AD8232 ECG module and Arduino Uno R4 Minima ($102 total), I 
designed and validated a complete real-time ECG acquisition and analysis pipeline. 
The system achieves 96.3% mean R-peak detection accuracy, visible PQRST 
morphology, and real-time HRV analysis through a Streamlit web dashboard.

**Key findings:**
- 96.3% mean R-peak detection accuracy across 5 validated resting trials
- 20% post-exercise BPM elevation (90 → 108 BPM) with parasympathetic rebound confirmed
- All 5 PQRST waves visible — Q-wave: 7.9% of R, S-wave: 28.0% of R
- Single electrode displacement (±2cm) has minimal BPM impact; combined displacement degrades accuracy by 6.3%
- Moving Average achieves higher SNR but lower detection reliability than Butterworth — confirming SNR alone is insufficient to evaluate ECG filter quality

---

## System Architecture

![Block Diagram](hardware/block_diagram.png)

| Layer | Components |
|---|---|
| Hardware | AD8232 AFE → Arduino R4 Minima (14-bit ADC, 533Hz) → USB Serial |
| Signal Processing | Butterworth Bandpass (0.5–40Hz) + IIR Notch (60Hz) + Peak Detection |
| Analysis | BPM calculation, HRV (SDNN/RMSSD), PQRST morphology |
| Visualization | Streamlit live dashboard + Matplotlib experimental plots |

---

## Hardware

### Bill of Materials

| Component | Part Number | Cost | Purpose |
|---|---|---|---|
| SparkFun AD8232 | SEN-12650 | $24.41 | ECG analog front-end |
| Electrode Cable | CAB-12970 | $9.60 | 3-lead electrode connection |
| Arduino Uno R4 Minima | — | $19.99 | 14-bit ADC + USB serial |
| Ag/AgCl Electrodes (100pk) | Kendall | $15.30 | Skin contact |
| Breadboard + jumpers | — | $8.99 | Prototyping |
| Alcohol prep pads | — | $7.00 | Skin preparation |
| Header pins | HiLetgo 40-pin | $5.49 | AD8232 connection |
| **Total** | | **$90.78** | |

### Wiring

| AD8232 Pin | Arduino Pin | Function |
|---|---|---|
| 3.3V | 3.3V | Power |
| GND | GND | Ground |
| OUTPUT | A0 | ECG signal |
| LO+ | D10 | Lead-off detect + |
| LO- | D11 | Lead-off detect - |

### Electrode Placement
- **Red** → Right chest (below collarbone)
- **Blue** → Left chest (below collarbone)
- **Black** → Right lower abdomen (ground)

### PCB Design
Custom PCB designed in EasyEDA featuring AD8232, decoupling capacitors (2×100nF, 
1×10µF), bias resistors (2×10kΩ), 3.5mm PJ-320A electrode jack, and Arduino pin 
headers. All components selected from JLCPCB assembly library.

![Schematic](hardware/ecg_schematic.png)

---

## Signal Processing Pipeline

### Filter Specifications

| Filter | Type | Cutoff | Order | Purpose |
|---|---|---|---|---|
| High-pass | Butterworth | 0.5 Hz | 4 | Baseline drift removal |
| Low-pass | Butterworth | 40 Hz | 4 | EMG artifact removal |
| Notch | IIR | 60 Hz | Q=30 | Powerline interference |

**Implementation:** Zero-phase filtering (scipy filtfilt) eliminates phase 
distortion for accurate RR interval timing. This is critical for HRV analysis 
where millisecond-level timing precision determines metric validity.

**Design decision:** The 0.5 Hz lower cutoff was deliberately calibrated to 
preserve the low-amplitude P-wave rather than aggressively filtering baseline 
drift. Residual baseline ripple visible in single-beat analysis represents a 
conscious tradeoff — prioritizing physiological completeness over visual 
cleanliness.

### Sampling Architecture

| Parameter | Value |
|---|---|
| Sampling frequency | 533.3 Hz (validated — not assumed) |
| ADC resolution | 14-bit |
| Serial baud rate | 115200 bps |
| Timing jitter | 3.61ms |
| Recording duration | 30 seconds (16,000 samples) |
| Signal inversion | Applied (electrode polarity correction) |

### Peak Detection
Adaptive threshold: `median + 0.5 × std`  
Minimum R-R distance: `0.6 × fs` (prevents double detection)  
Mean accuracy: **96.3%** (range: 89.4%–100.0%, N=5 trials)

### Key Signal Processing Insight

A critical finding from Experiment 3: Moving Average filtering achieved higher 
mean SNR (0.63 ± 1.99 dB) compared to Butterworth bandpass (-10.14 ± 3.58 dB), 
yet demonstrated inferior BPM consistency across trials.

This apparent paradox reveals a fundamental limitation of SNR as an ECG filter 
evaluation metric:

- Moving Average smooths broadband noise but preserves 60Hz powerline interference 
  and distorts QRS morphology
- Butterworth bandpass selectively removes non-physiological frequency content 
  while preserving the 0.5–40Hz ECG signal band
- Visually cleaner signals (higher SNR) are not necessarily physiologically 
  superior — morphology preservation matters more than signal power ratio for 
  reliable cardiac event detection
- The negative SNR for Butterworth reflects DC energy attenuation penalizing the 
  metric, not actual signal degradation

This finding motivates future work on morphology-specific evaluation metrics 
such as peak sharpness ratio and waveform distortion index.

![Filter Comparison](results/experiment_3/filter_visual_comparison_trial_3.png)

### PQRST Morphology

All 5 cardiac waves clearly identified on Trial 3:

| Wave | Amplitude | % of R | Physiological meaning |
|---|---|---|---|
| P | visible | — | Atrial depolarization |
| Q | -18.0 ADC | 7.9% | Septal depolarization |
| R | 228.3 ADC | 100% | Ventricular depolarization |
| S | -64.0 ADC | 28.0% | Late ventricular depolarization |
| T | ~50 ADC | ~22% | Ventricular repolarization |

Q/S ratios confirm the negative deflections are physiological features, not 
filtering artifacts — demonstrating morphological fidelity of the pipeline.

---

## Experiments

### Experiment 1 — Resting vs Exercise vs Recovery

**Protocol:** 5 resting trials (30s each) + 3 exercise blocks  
(2 min jumping jacks → immediate BPM check → 5 min rest → recovery recording)

| State | BPM | SDNN | RMSSD |
|---|---|---|---|
| Resting avg | 91.0 | 41.31ms | 45.93ms |
| Pre-exercise | 90 | — | — |
| Post-exercise | 108 | — | — |
| Recovery 1 | 86.7 | 54.33ms | 45.45ms |
| Recovery 2 | 92.1 | 20.18ms | 9.91ms |
| Recovery 3 | 95.7 | 9.24ms | 9.42ms |

**Key findings:**
- 20% post-exercise BPM elevation (+18 BPM above baseline)
- Parasympathetic rebound in Recovery Trial 1 (SDNN 54.33ms > resting 41.31ms)
- Progressive HRV suppression across recovery trials suggests continued autonomic 
  recovery beyond the measurement window
- Post-exercise motion artifact prevented filtered-pipeline recording — raw 
  signal adaptive threshold used instead (documented limitation)

### Experiment 2 — Electrode Placement Robustness

**Protocol:** 4 conditions × 3 trials  
Standard → RA shifted 2cm → LA shifted 2cm → both shifted 2cm

| Condition | Avg BPM | vs Standard |
|---|---|---|
| Standard | 82.2 | baseline |
| RA off 2cm | 81.6 | -0.7% |
| LA off 2cm | 83.0 | +1.0% |
| Both off 2cm | 87.4 | +6.3% |

**Key finding:** Single electrode displacement (±2cm) has minimal BPM impact. 
Combined displacement degrades detection accuracy by 6.3%, indicating that 
individual electrode placement tolerance of ±2cm is acceptable for reliable 
R-peak detection in this system.

### Experiment 3 — Filter Algorithm Comparison

**Protocol:** 3 algorithms × 5 resting trials

| Algorithm | SNR (mean±SD) | BPM (mean±SD) | Time |
|---|---|---|---|
| Moving Average | 0.63 ± 1.99 dB | 88.02 ± 8.08 | 0.69ms |
| Butterworth | -10.14 ± 3.58 dB | 80.14 ± 22.04 | 4.4ms |
| Butterworth+Notch | -10.16 ± 3.58 dB | 79.7 ± 22.92 | 2.11ms |

See Signal Processing section for full interpretation of the SNR paradox finding.

---

## Live Dashboard

![Dashboard](hardware/dashboard_screenshots/dashboard_live.png)

**Features:**
- Real-time ECG waveform with R-peak markers
- Live BPM display (color-coded red if >100 BPM)
- SDNN and RMSSD updating in real time
- Raw vs filtered signal toggle
- Lead-off detection alert
- CSV export for offline analysis
- Filter settings displayed in sidebar

**Run locally:**
```bash
cd dashboard
pip install -r requirements.txt
streamlit run ecg_dashboard.py
```

> ⚠️ Not a medical device. For educational and research purposes only.

---

## Installation

### Requirements

```bash
pip install streamlit pandas numpy scipy pyserial plotly matplotlib
```

Or install from requirements file:
```bash
pip install -r dashboard/requirements.txt
```

### Arduino Setup
1. Install Arduino IDE 2.x
2. Select board: Arduino UNO R4 Minima
3. Upload `hardware/arduino_ecg.ino`
4. Set baud rate: 115200
5. Close Serial Monitor/Plotter before running Python scripts

### Running Signal Processing Scripts
```bash
cd signal_processing

# Record a trial
python serial_reader.py

# Analyze recorded data
python peak_detection.py

# Generate PQRST visualization
python pqrst_analysis.py

# Run filter comparison
python filter_visual_comparison.py

# Validate peak accuracy
python validation.py
```

### Running the Dashboard
```bash
cd dashboard
streamlit run ecg_dashboard.py
# Opens at http://localhost:8501
```

**Serial port:** Default COM3 (Windows). Change in sidebar if different.  
**Prerequisites:** Arduino connected, Serial Plotter closed, electrodes attached.

---

## Results Summary

| Metric | Value |
|---|---|
| R-peak detection accuracy | 96.3% mean (89.4–100%) |
| Resting BPM (best trial) | 89.5 |
| Post-exercise BPM elevation | +20% (90 → 108 BPM) |
| Parasympathetic rebound | Confirmed (SDNN 54.33ms > baseline 41.31ms) |
| PQRST waves visible | All 5 (P, Q, R, S, T) |
| Q-wave amplitude | -18.0 ADC (7.9% of R) — within normal range |
| S-wave amplitude | -64.0 ADC (28.0% of R) — within normal range |
| Sampling rate (validated) | 533.3 Hz |
| System cost | $90.78 |

---

## Repository Structure

```
ecg-biosensor/
├── signal_processing/          # Python analysis scripts
│   ├── serial_reader.py        # Arduino serial data capture
│   ├── filters.py              # Butterworth + notch filter pipeline
│   ├── peak_detection.py       # R-peak detection + HRV analysis
│   ├── pqrst_analysis.py       # PQRST wave visualization
│   ├── raw_vs_filtered.py      # Normalized comparison plots
│   ├── negative_deflection.py  # Q/S wave investigation
│   ├── filter_visual_comparison.py  # 4-panel algorithm comparison
│   ├── experiment_3.py         # Algorithm benchmarking
│   ├── quick_bpm_check.py      # 10-second live BPM check
│   └── validation.py           # Peak accuracy validation
├── dashboard/                  # Streamlit live dashboard
│   ├── ecg_dashboard.py
│   └── requirements.txt
├── results/                    # All experimental data and plots
│   ├── experiment_1/           # Resting/exercise/recovery (10 trials)
│   ├── experiment_2/           # Electrode placement (12 trials)
│   └── experiment_3/           # Filter comparison (15 trials)
├── hardware/                   # PCB design and documentation
│   ├── ecg_schematic.png       # EasyEDA schematic
│   ├── block_diagram.png       # System architecture
│   └── dashboard_screenshots/  # Live dashboard photos
└── report/                     # Technical report
    └── references/             # 5 peer-reviewed papers (PDF)
```

---

## Limitations

- **Single subject:** All data from one subject — findings cannot be generalized
- **Short HRV windows:** 30-second recordings are below the 5-minute clinical standard for reliable HRV metrics
- **Motion artifact:** Post-exercise filtered-pipeline recordings were unreliable; raw signal adaptive threshold used for exercise BPM — documented as methodological adaptation
- **SNR methodology:** Standard SNR definition penalizes DC attenuation — may not accurately reflect ECG morphology preservation quality; motivates future morphology-specific metrics
- **Breadboard connections:** Mechanical instability during movement limits exercise recording quality — primary motivation for PCB fabrication

---

## Future Work

- [ ] Custom PCB fabrication via JLCPCB (schematic complete, routing pending)
- [ ] Multi-subject validation study (N≥10)
- [ ] Streamlit Cloud deployment (CSV playback demo for sharing)
- [ ] 5-minute HRV recording windows for clinical-grade metrics
- [ ] lfilter implementation for true causal real-time filtering
- [ ] Bland-Altman agreement analysis vs commercial pulse oximeter
- [ ] Peak sharpness ratio metric for morphology-specific filter evaluation
- [ ] Journal of Student Research submission (target: August 2026)

---

## References

1. Pan, J. & Tompkins, W.J. (1985). A real-time QRS detection algorithm. *IEEE Transactions on Biomedical Engineering*, 32(3), 230–236.
2. Task Force of ESC & NASPE (1996). Heart rate variability: Standards of measurement, physiological interpretation, and clinical use. *Circulation*, 93(5), 1043–1065.
3. Serhani, M.A. et al. (2020). ECG monitoring systems: Review, architecture, processes, and key challenges. *Sensors*, 20(6), 1796.
4. Kohler, B.U. et al. (2002). The principles of software QRS detection. *IEEE Engineering in Medicine and Biology Magazine*, 21(1), 42–57.
5. Christov, I.I. (2004). Real time electrocardiogram QRS detection using combined adaptive threshold. *BioMedical Engineering OnLine*, 3(1), 28.

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

## About

This project was motivated by observations at Open Door Ministries, a homeless 
shelter where I volunteer as scheduling coordinator. Witnessing healthcare access 
inequality firsthand raised a question that drove this research: can low-cost 
consumer hardware produce clinically meaningful cardiac metrics with careful 
signal processing?

The answer — supported by validated experiments — is yes.

> *"Every project I pursue asks the same question I first asked at Open Door: 
> how do we build systems that actually reach the people who need them most?"*

*Shrimaan Rapuru | The Early College at Guilford, NC*