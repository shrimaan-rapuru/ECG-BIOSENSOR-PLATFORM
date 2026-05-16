# ECG Biosensor System

Real-time ECG monitoring system with signal processing dashboard.

**Builder:** Shrimaan Rapuru  
**Timeline:** Summer 2026  
**Stack:** Arduino, Python, Streamlit, SciPy, EasyEDA  

## Results So Far
- BPM: 81.3 (4.2% error vs manual count)
- SDNN: 34.46ms
- RMSSD: 58.9ms
- Sampling rate: 533Hz

## Hardware
- SparkFun AD8232 ECG Sensor (SEN-12650)
- Arduino Uno R4 Minima
- Kendall Ag/AgCl Electrodes (CAB-12970)

## Features
- Real-time ECG signal acquisition at 500Hz
- 3-stage filter pipeline (Butterworth + 60Hz notch)
- R-peak detection and BPM calculation
- HRV analysis (SDNN, RMSSD)
- Algorithm comparison (Moving Average vs Butterworth vs Butterworth+Notch)

## Status
Week 2 of 6 — Signal processing complete
