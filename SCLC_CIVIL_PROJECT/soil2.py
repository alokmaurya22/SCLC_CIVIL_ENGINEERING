import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# --- Soil Classification Function ---
def classify_soil(D10, D30, D60, LL, PL, percent_finer_200):
    Cu = D60 / D10
    Cc = (D30 ** 2) / (D10 * D60)
    PI = LL - PL

    if percent_finer_200 > 50:
        if PI < 7:
            return "ML (Silt with low plasticity)"
        elif PI >= 7:
            return "CL (Clay with low to medium plasticity)"
    else:
        if Cu > 4 and 1 < Cc < 3:
            return "GW (Well-graded gravel)"
        elif Cu <= 4 or not (1 < Cc < 3):
            return "GP (Poorly graded gravel)"
        elif percent_finer_200 > 12:
            return "SC/SM (Clayey or silty sand)"

    return "Check data again"

# --- Liquefaction Calculation Functions ---
def calculate_CSR(a_max, g, sigma_v0, sigma_v0_eff, rd):
    return 0.65 * (a_max / g) * (sigma_v0 / sigma_v0_eff) * rd

def calculate_CRR(N60, soil_type):
    if "CL" in soil_type or "ML" in soil_type:
        return 0.2  # For fine-grained soils (approximation)
    elif N60 <= 15:
        return (1 / 34.0) * N60 + (N60 ** 2 / 1260.0)
    elif N60 <= 30:
        return (N60 - 15) / 15.0 * (1.2 - (1 / 34.0) * 15 - (15 ** 2 / 1260.0)) + (1 / 34.0) * 15 + (15 ** 2 / 1260.0)
    else:
        return 1.2

def get_rd(z):
    return max(0.5, 1.0 - 0.015 * z)  # Minimum limit

# --- Streamlit UI ---
st.set_page_config(page_title="Liquefaction Calculator", layout="centered")

st.title("🧪 Soil Classification & Liquefaction Calculator")
st.write("This tool classifies the soil and evaluates liquefaction potential using CSR vs CRR method.")

with st.expander("📌 Step 1: Soil Classification Inputs"):
    col1, col2 = st.columns(2)
    with col1:
        D10 = st.number_input("D10 (mm)", value=0.1)
        D30 = st.number_input("D30 (mm)", value=0.25)
        D60 = st.number_input("D60 (mm)", value=0.6)
        percent_finer_200 = st.number_input("Passing 75 micron (%)", value=35)
    with col2:
        LL = st.number_input("Liquid Limit (LL)", value=40)
        PL = st.number_input("Plastic Limit (PL)", value=25)

soil_type = classify_soil(D10, D30, D60, LL, PL, percent_finer_200)
st.success(f"🧾 Classified Soil Type: **{soil_type}**")

with st.expander("📌 Step 2: Liquefaction Inputs"):
    col1, col2 = st.columns(2)
    with col1:
        a_max = st.number_input("Peak Ground Acceleration amax (m/s²)", value=3.0)
        sigma_v0 = st.number_input("Total Overburden Stress σv0 (kPa)", value=150.0)
        sigma_v0_eff = st.number_input("Effective Overburden Stress σ'v0 (kPa)", value=100.0)
        z = st.number_input("Depth (m)", value=5.0)
    with col2:
        N = st.number_input("SPT N-value", value=15)
        CN = 1.0 + (1.5 / (sigma_v0_eff / 100))  # Overburden correction
        N60 = N * CN

rd = get_rd(z)
CSR = calculate_CSR(a_max, 9.81, sigma_v0, sigma_v0_eff, rd)
CRR = calculate_CRR(N60, soil_type)
FS = CRR / CSR

st.write(f"🧮 Corrected N60 value: **{N60:.2f}**")
st.write(f"🔧 Stress Reduction Factor (rd): **{rd:.2f}**")
st.write(f"📉 CSR: **{CSR:.3f}**")
st.write(f"📈 CRR: **{CRR:.3f}**")

if FS < 1:
    st.error(f"🚨 Factor of Safety = {FS:.2f} ➤ Likely **Liquefaction**")
else:
    st.success(f"✅ Factor of Safety = {FS:.2f} ➤ **Safe** from Liquefaction")

# --- Table Summary ---
result_data = pd.DataFrame({
    "Parameter": ["Soil Type", "N60", "rd", "CSR", "CRR", "FS"],
    "Value": [soil_type, round(N60, 2), round(rd, 2), round(CSR, 3), round(CRR, 3), round(FS, 2)]
})
st.dataframe(result_data)

# --- Plot CSR vs CRR Chart ---
if st.checkbox("📊 Show CSR vs CRR Chart"):
    N60_range = np.linspace(1, 30, 100)
    CRR_curve = [(1 / 34.0) * n + (n ** 2 / 1260.0) if n <= 15 else 1.2 for n in N60_range]

    fig, ax = plt.subplots()
    ax.plot(N60_range, CRR_curve, label="CRR Curve (Clean Sand)", color='green')
    ax.hlines(CSR, xmin=1, xmax=30, colors='red', linestyles='--', label=f'CSR = {CSR:.3f}')
    ax.scatter(N60, CRR, color='blue', s=80, label=f'N60 = {N60:.2f}')
    ax.set_xlabel("Corrected N60")
    ax.set_ylabel("CRR")
    ax.set_title("CSR vs CRR Liquefaction Chart")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)

# --- Recommendation Section ---
st.subheader("📋 Recommendations")
if FS < 1:
    st.warning("Liquefaction risk is high. Consider soil densification, drainage improvement, ground reinforcement, or other mitigation methods.")
else:
    st.success("Liquefaction unlikely. Normal foundation design may proceed, but confirm with site-specific investigation.")
