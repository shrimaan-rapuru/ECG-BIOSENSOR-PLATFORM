import streamlit as st
import serial
import serial.tools.list_ports
import numpy as np
import pandas as pd
import time
import csv
from datetime import datetime
from collections import deque
from scipy.signal import butter, filtfilt, find_peaks
import plotly.graph_objects as go

# ── PAGE CONFIG ───────────────────────────────────────────
st.set_page_config(
    page_title="ECG Biosensor Dashboard",
    page_icon="❤️",
    layout="wide"
)

# ── CUSTOM CSS ────────────────────────────────────────────
st.markdown("""
<style>
    .bpm-display {
        font-size: 80px;
        font-weight: bold;
        color: #e74c3c;
        text-align: center;
    }
    .hrv-display {
        font-size: 40px;
        font-weight: bold;
        color: #2ecc71;
        text-align: center;
    }
    .metric-label {
        font-size: 18px;
        color: #888888;
        text-align: center;
    }
    .lead-off {
        font-size: 24px;
        font-weight: bold;
        color: white;
        background-color: #e74c3c;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
    }
    .connected {
        font-size: 18px;
        color: #2ecc71;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ── FILTER FUNCTIONS ──────────────────────────────────────
def butter_bandpass(data, lowcut=0.5, highcut=40.0, fs=533, order=4):
    nyq = 0.5 * fs
    b, a = butter(order, [lowcut/nyq, highcut/nyq], btype='band')
    return filtfilt(b, a, data)

def full_pipeline(data, fs=533):
    from scipy.signal import iirnotch
    nyq = 0.5 * fs
    b_notch, a_notch = iirnotch(60/nyq, 30)
    filtered = butter_bandpass(data, fs=fs)
    filtered = filtfilt(b_notch, a_notch, filtered)
    return filtered

def detect_peaks(filtered, fs=533):
    if len(filtered) < int(fs * 2):
        return np.array([])
    peaks, _ = find_peaks(filtered,
                          distance=int(0.6 * fs),
                          height=np.median(filtered) + 0.5 * np.std(filtered))
    return peaks

def calculate_bpm(peaks, fs=533):
    if len(peaks) < 2:
        return 0
    rr = np.diff(peaks) / fs
    return round(60 / np.mean(rr), 1)

def calculate_hrv(peaks, fs=533):
    if len(peaks) < 3:
        return 0, 0
    rr = np.diff(peaks) / fs * 1000
    sdnn = round(np.std(rr), 2)
    rmssd = round(np.sqrt(np.mean(np.diff(rr)**2)), 2)
    return sdnn, rmssd

# ── SIDEBAR ───────────────────────────────────────────────
st.sidebar.title("⚙️ Settings")

# Port selection
ports = [p.device for p in serial.tools.list_ports.comports()]
if not ports:
    ports = ["COM3"]
selected_port = st.sidebar.selectbox("Serial Port", ports, index=0)

fs = st.sidebar.number_input("Sampling Rate (Hz)", value=533, min_value=100, max_value=1000)
window_size = st.sidebar.slider("Display Window (seconds)", 5, 30, 10)
show_raw = st.sidebar.checkbox("Show Raw Signal", value=False)
subject_name = st.sidebar.text_input("Subject ID", value="Subject 2")

st.sidebar.markdown("---")
st.sidebar.markdown("**Filter Settings:**")
st.sidebar.markdown("- Butterworth Bandpass: 0.5–40 Hz")
st.sidebar.markdown("- IIR Notch: 60 Hz")
st.sidebar.markdown("- Order: 4")
st.sidebar.markdown("- Zero-phase (filtfilt)")

# ── MAIN TITLE ────────────────────────────────────────────
st.title("❤️ Real-Time ECG Biosensor Dashboard")
st.markdown("**Low-Cost ECG Signal Acquisition & HRV Analysis Platform**")
st.markdown(f"*Subject: {subject_name} | Port: {selected_port} | fs: {fs}Hz*")

# ── LEAD OFF ALERT (placeholder) ─────────────────────────
lead_off_placeholder = st.empty()

# ── METRICS ROW ───────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<p class="metric-label">Heart Rate</p>', unsafe_allow_html=True)
    bpm_placeholder = st.empty()

with col2:
    st.markdown('<p class="metric-label">SDNN</p>', unsafe_allow_html=True)
    sdnn_placeholder = st.empty()

with col3:
    st.markdown('<p class="metric-label">RMSSD</p>', unsafe_allow_html=True)
    rmssd_placeholder = st.empty()

with col4:
    st.markdown('<p class="metric-label">Peaks Detected</p>', unsafe_allow_html=True)
    peaks_placeholder = st.empty()

st.markdown("---")

# ── ECG CHART ─────────────────────────────────────────────
st.subheader("📈 ECG Waveform")
chart_placeholder = st.empty()

st.markdown("---")

# ── CONTROLS ──────────────────────────────────────────────
col_start, col_stop, col_save = st.columns(3)

with col_start:
    start_btn = st.button("▶️ Start Recording", type="primary")
with col_stop:
    stop_btn = st.button("⏹️ Stop Recording")
with col_save:
    save_btn = st.button("💾 Save CSV")

# ── SESSION STATE ─────────────────────────────────────────
if 'recording' not in st.session_state:
    st.session_state.recording = False
if 'raw_buffer' not in st.session_state:
    st.session_state.raw_buffer = deque(maxlen=int(fs * 35))
if 'time_buffer' not in st.session_state:
    st.session_state.time_buffer = deque(maxlen=int(fs * 35))
if 'start_time' not in st.session_state:
    st.session_state.start_time = time.time()
if 'lead_off' not in st.session_state:
    st.session_state.lead_off = False

if start_btn:
    st.session_state.recording = True
    st.session_state.raw_buffer.clear()
    st.session_state.time_buffer.clear()
    st.session_state.start_time = time.time()

if stop_btn:
    st.session_state.recording = False

if save_btn and len(st.session_state.raw_buffer) > 0:
    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"../results/dashboard_recording_{timestamp_str}.csv"
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'ecg_value'])
        for t, v in zip(st.session_state.time_buffer,
                        st.session_state.raw_buffer):
            writer.writerow([round(t, 4), v])
    st.success(f"Saved to {filename}")

# ── LIVE RECORDING LOOP ───────────────────────────────────
if st.session_state.recording:
    try:
        ser = serial.Serial(selected_port, 115200, timeout=1)
        time.sleep(1)

        for _ in range(int(fs * window_size)):
            line = ser.readline().decode('utf-8').strip()

            if line == '!':
                st.session_state.lead_off = True
                lead_off_placeholder.markdown(
                    '<p class="lead-off">⚠️ LEADS DISCONNECTED — Check electrode placement</p>',
                    unsafe_allow_html=True
                )
                continue
            else:
                st.session_state.lead_off = False
                lead_off_placeholder.empty()

            try:
                value = int(line)
                elapsed = time.time() - st.session_state.start_time
                st.session_state.raw_buffer.append(value)
                st.session_state.time_buffer.append(elapsed)
            except ValueError:
                continue

            # Process when enough data
            if len(st.session_state.raw_buffer) >= int(fs * 4):
                raw = np.array(st.session_state.raw_buffer)
                times = np.array(st.session_state.time_buffer)

                # Preprocess
                raw_proc = np.clip(raw, np.percentile(raw, 1),
                                   np.percentile(raw, 99))
                raw_proc = -raw_proc

                # Filter
                try:
                    filtered = full_pipeline(raw_proc, fs=fs)
                except Exception:
                    filtered = raw_proc

                # Display window
                display_samples = int(fs * window_size)
                disp_raw = raw[-display_samples:]
                disp_filtered = filtered[-display_samples:]
                disp_times = times[-display_samples:]

                # Detect peaks
                peaks = detect_peaks(filtered, fs=fs)
                bpm = calculate_bpm(peaks, fs=fs)
                sdnn, rmssd = calculate_hrv(peaks, fs=fs)

                # Update metrics
                bpm_color = "#e74c3c" if bpm > 100 else "#2ecc71"
                bpm_placeholder.markdown(
                    f'<p class="bpm-display" style="color:{bpm_color}">{bpm}</p>'
                    f'<p class="metric-label">BPM</p>',
                    unsafe_allow_html=True
                )
                sdnn_placeholder.markdown(
                    f'<p class="hrv-display">{sdnn}</p>'
                    f'<p class="metric-label">ms</p>',
                    unsafe_allow_html=True
                )
                rmssd_placeholder.markdown(
                    f'<p class="hrv-display">{rmssd}</p>'
                    f'<p class="metric-label">ms</p>',
                    unsafe_allow_html=True
                )
                peaks_in_window = peaks[peaks >= len(filtered) - display_samples]
                peaks_in_window = peaks_in_window - (len(filtered) - display_samples)
                peaks_placeholder.markdown(
                    f'<p class="hrv-display">{len(peaks_in_window)}</p>'
                    f'<p class="metric-label">in window</p>',
                    unsafe_allow_html=True
                )

                # Build chart
                fig = go.Figure()

                if show_raw:
                    raw_norm = (disp_raw - np.mean(disp_raw)) / (np.std(disp_raw) + 1e-8)
                    fig.add_trace(go.Scatter(
                        x=disp_times, y=raw_norm,
                        mode='lines',
                        name='Raw Signal',
                        line=dict(color='gray', width=1),
                        opacity=0.5
                    ))

                fig.add_trace(go.Scatter(
                    x=disp_times, y=disp_filtered,
                    mode='lines',
                    name='Filtered ECG',
                    line=dict(color='#2ecc71', width=1.5)
                ))

                if len(peaks_in_window) > 0:
                    peak_times = disp_times[peaks_in_window]
                    peak_vals = disp_filtered[peaks_in_window]
                    fig.add_trace(go.Scatter(
                        x=peak_times, y=peak_vals,
                        mode='markers',
                        name='R-peaks',
                        marker=dict(color='red', size=10,
                                   symbol='triangle-down')
                    ))

                fig.update_layout(
                    height=400,
                    showlegend=True,
                    xaxis_title="Time (seconds)",
                    yaxis_title="ADC Value",
                    plot_bgcolor='#0e1117',
                    paper_bgcolor='#0e1117',
                    font=dict(color='white'),
                    xaxis=dict(gridcolor='#333333'),
                    yaxis=dict(gridcolor='#333333'),
                    legend=dict(
                        bgcolor='#1e2130',
                        bordercolor='#333333'
                    ),
                    margin=dict(l=60, r=20, t=20, b=60)
                )

                chart_placeholder.plotly_chart(fig, use_container_width=True)

        ser.close()
        st.session_state.recording = False

    except serial.SerialException as e:
        st.error(f"Serial connection error: {e}")
        st.info("Make sure Arduino is connected and Serial Plotter is closed")
        st.session_state.recording = False

else:
    # Show placeholder chart when not recording
    fig = go.Figure()
    fig.add_annotation(
        text="Press ▶️ Start Recording to begin",
        xref="paper", yref="paper",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=20, color="gray")
    )
    fig.update_layout(
        height=400,
        plot_bgcolor='#0e1117',
        paper_bgcolor='#0e1117',
        xaxis=dict(showgrid=False, showticklabels=False),
        yaxis=dict(showgrid=False, showticklabels=False)
    )
    chart_placeholder.plotly_chart(fig, use_container_width=True)

# ── FOOTER ────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; font-size: 12px;'>
ECG Biosensor Platform — Shrimaan Rapuru | Summer 2026<br>
4th-order Butterworth Bandpass (0.5–40Hz) + IIR Notch (60Hz) | fs = 533Hz<br>
<i>Not a medical device. For educational and research purposes only.</i>
</div>
""", unsafe_allow_html=True)