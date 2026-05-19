# Real-Time Low-Cost ECG Biosensing & Signal Analysis Platform

**Builder:** Shrimaan Rapuru — The Early College at Guilford  
**Timeline:** Summer 2026  
**Status:** Week 2 of 6 — Signal processing complete, experiments in progress  
**GitHub:** github.com/shrimaan-rapuru/ECG-BIOSENSOR

---

## Abstract

Access to electrocardiogram (ECG) monitoring is largely limited to clinical 
settings due to the high cost of medical-grade devices. This project 
investigates whether a low-cost, open-source biosensing platform ($102 total) 
can achieve physiologically meaningful ECG signal quality through optimized 
signal processing pipelines.

The system acquires real-time cardiac electrical signals using a SparkFun 
AD8232 analog front-end and Arduino Uno R4 Minima microcontroller at 533Hz, 
transmits data via USB serial to a Python-based processing pipeline, and 
applies a three-stage filter cascade (Butterworth bandpass, 60Hz IIR notch, 
baseline drift correction) before performing R-peak detection and Heart Rate 
Variability (HRV) analysis.

Initial validation achieved 81.3 BPM detection within 4.2% of manual ground 
truth, with SDNN of 34.46ms and RMSSD of 58.9ms — both within clinically 
reported resting HRV ranges. Structured experiments comparing three filtering 
algorithms and evaluating electrode placement effects are ongoing.

The project is framed as an open-source biomedical engineering investigation 
into signal reliability and accessible physiological monitoring — not a 
clinical diagnostic tool.

---

## System Architecture
