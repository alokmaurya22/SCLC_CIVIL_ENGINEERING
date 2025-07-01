import streamlit as st
import math

st.set_page_config(page_title="Soil Liquefaction App", layout="centered")

st.title("🌍 Soil Classification & Liquefaction Analysis")

# Reset button
if st.button("🔁 Reset All Inputs"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.experimental_rerun()

# Initialize session state
if 'step1_complete' not in st.session_state:
    st.session_state.step1_complete = False
if 'step2_complete' not in st.session_state:
    st.session_state.step2_complete = False

# ---------------------------
# Step 1: Soil Classification
# ---------------------------
st.header("🧱 Step 1: Soil Classification")

with st.expander("ℹ️ What is Soil Classification?"):
    st.write("Soil classification helps in identifying the type of soil based on Atterberg limits and particle size. It's important to understand the soil behavior for geotechnical design.")

st.markdown("Provide Atterberg limits and grain size data:")

ll = st.number_input("Liquid Limit (LL) [%]", min_value=0.0, max_value=100.0, value=0.0, help="(0–100%) Water content at which soil changes from plastic to liquid")
pl = st.number_input("Plastic Limit (PL) [%]", min_value=0.0, max_value=100.0, value=0.0, help="(0–100%) Water content at which soil starts behaving plastically")
fines = st.number_input("Fines Content [% passing 75µm sieve]", min_value=0.0, max_value=100.0, value=0.0, help="(0–100%) Percentage of soil passing 75 micron sieve")

# Grain size data
st.markdown("Enter Particle Size Distribution Data:")
d10 = st.number_input("D10 (mm)", min_value=0.001, max_value=10.0, value=0.001, format="%.3f", help="(0.001–10 mm) Diameter at 10% finer")
d30 = st.number_input("D30 (mm)", min_value=0.001, max_value=10.0, value=0.001, format="%.3f", help="(0.001–10 mm) Diameter at 30% finer")
d60 = st.number_input("D60 (mm)", min_value=0.001, max_value=10.0, value=0.001, format="%.3f", help="(0.001–10 mm) Diameter at 60% finer")

if st.button("✅ Classify Soil"):
    PI = ll - pl
    cu = d60 / d10
    cc = (d30 ** 2) / (d10 * d60)

    if fines > 50:
        if PI > 7:
            soil_type = "CL (Clay with low plasticity)"
        else:
            soil_type = "ML (Silt with low plasticity)"
    elif fines > 12:
        soil_type = "SM (Silty Sand or Sandy Silt)"
    else:
        if cu > 4 and 1 < cc < 3:
            soil_type = "SW (Well-Graded Sand)"
        else:
            soil_type = "SP (Poorly graded Sand)"

    st.session_state.soil_type = soil_type
    st.session_state.step1_complete = True
    st.success(f"🔍 Soil Type Classified: **{soil_type}**")

# ---------------------------
# Step 2: amax Calculation (auto-determined by soil type)
# ---------------------------
if st.session_state.step1_complete:
    st.header("📈 Step 2: Peak Ground Acceleration (aₘₐₓ)")

    with st.expander("ℹ️ What is aₘₐₓ?"):
        st.write("aₘₐₓ is the peak ground acceleration during an earthquake. It depends on the seismic zone and amplification factor due to soil type.")

    soil_type = st.session_state.soil_type
    if "CL" in soil_type:
        seismic_zone = "Zone III"
    elif "ML" in soil_type:
        seismic_zone = "Zone IV"
    elif "SM" in soil_type:
        seismic_zone = "Zone IV"
    else:
        seismic_zone = "Zone II"

    zone_factors = {"Zone II": 0.10, "Zone III": 0.16, "Zone IV": 0.24, "Zone V": 0.36}
    Z = zone_factors[seismic_zone]

    if "CL" in soil_type or "ML" in soil_type:
        S = 1.5
    elif "SM" in soil_type:
        S = 1.2
    else:
        S = 1.0

    amax = Z * S * 9.81  # m/s²
    amax_g = amax / 9.81

    st.session_state.amax_g = amax_g
    st.session_state.step2_complete = True

    st.info(f"✅ Soil Type: {soil_type}, Mapped Seismic Zone: {seismic_zone}")
    st.success(f"Calculated aₘₐₓ = {amax:.2f} m/s²  →  aₘₐₓ/g = {amax_g:.2f}")

# ---------------------------
# Step 3: Liquefaction Analysis
# ---------------------------
if st.session_state.step2_complete:
    st.header("🌊 Step 3: Liquefaction Check")

    with st.expander("ℹ️ What is Liquefaction?"):
        st.write("Liquefaction occurs when saturated soil loses strength during seismic shaking. Factor of Safety (FS) helps determine whether liquefaction is likely.")

    depth = st.number_input("Depth of Soil Layer (m)", min_value=0.5, max_value=50.0, value=0.5, help="(0.5–50 m) Depth of interest below ground surface")
    gamma = st.number_input("Unit Weight of Soil (kN/m³)", min_value=10.0, max_value=25.0, value=10.0, help="(10–25 kN/m³) Unit weight of soil layer")
    gw_depth = st.number_input("Water Table Depth (m)", min_value=0.0, max_value=50.0, value=0.0, help="(0–50 m) Depth to groundwater table")

    n_value = st.number_input("SPT N-Value", min_value=1, max_value=100, value=1, help="(1–100) Standard Penetration Test blow count")

    σv = gamma * depth
    σv_eff = σv - 9.81 * (depth - gw_depth if depth > gw_depth else 0)
    rd = 1.0 - 0.00765 * depth
    rd = max(rd, 0.5)

    Cn = (100 / σv_eff) ** 0.5 if σv_eff > 0 else 0
    N1_60 = n_value * Cn

    if σv_eff > 0:
        CSR = 0.65 * st.session_state.amax_g * (σv / σv_eff) * rd
        CRR_7_5 = (1 / (34 - N1_60)) + (N1_60 / 135) + (50 / ((10 * N1_60 + 45) ** 2)) - 1 / 200
        CRR = CRR_7_5
        FS = CRR / CSR

        st.subheader("📊 Results:")
        st.markdown(f"- Total vertical stress σv = **{σv:.2f} kPa**")
        st.markdown(f"- Effective vertical stress σv' = **{σv_eff:.2f} kPa**")
        st.markdown(f"- Stress reduction factor rd = **{rd:.3f}**")
        st.markdown(f"- Overburden correction factor Cn = **{Cn:.3f}**")
        st.markdown(f"- Corrected N-value (N1_60) = **{N1_60:.2f}**")
        st.markdown(f"- CSR = **{CSR:.3f}**")
        st.markdown(f"- CRR = **{CRR:.3f}**")
        st.markdown(f"- **Factor of Safety = {FS:.2f}**")

        if FS < 1:
            st.error("❌ Liquefaction is **likely** at this location (FS < 1).")
        else:
            st.success("✅ Liquefaction is **not likely** at this location (FS ≥ 1).")
    else:
        st.error("❌ Invalid effective stress. Please check input values.")
