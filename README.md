# 🧪 Soil Classification & Liquefaction Analysis Web App

A professional web-based geotechnical tool for quick **soil classification** and **liquefaction potential evaluation** using well-established geotechnical engineering formulas. Designed with civil engineering students, researchers, and practitioners in mind, this app is fully interactive, mobile-optimized, and academically grounded.

🚀 **Live App:** [Click to Launch App](https://sclccivilengineering-bwpf44hnapprmuuxej69u6b.streamlit.app/)

---

## 🌟 Features

- ✅ Classify soil type based on **grain size and Atterberg limits**
- ✅ Calculate **Corrected N-value (N60)** from raw SPT data
- ✅ Compute:
  - `rd` – Stress Reduction Factor
  - `CSR` – Cyclic Stress Ratio
  - `CRR` – Cyclic Resistance Ratio
  - `FS` – Factor of Safety
- ✅ Interpret liquefaction risk using the FS value
- ✅ Generate CSR vs CRR curve with SPT data overlay
- ✅ Clean 2-step input interface with expandable sections
- ✅ Fully mobile-optimized for smartphones/tablets

---

## 📦 Technologies Used

| Component | Library |
|----------|---------|
| App Framework | Streamlit |
| Computation | Python (NumPy, Pandas) |
| Plotting | Matplotlib |
| Hosting | Streamlit Cloud |

---

## 📥 Inputs Description

### Step 1 – Soil Classification

| Parameter | Description |
|----------|-------------|
| D10, D30, D60 | Grain size diameters (in mm) |
| LL, PL | Liquid and plastic limits (%) |
| Passing 75 µm | Percentage of fines (by weight) |

### Step 2 – Liquefaction Inputs

| Parameter | Description |
|----------|-------------|
| amax | Peak ground acceleration (m/s²) |
| σv0 | Total vertical stress (kPa) |
| σ′v0 | Effective vertical stress (kPa) |
| z | Depth below ground (m) |
| N | Raw SPT value |

---

## 📊 Outputs Generated

| Output | Description |
|--------|-------------|
| N60 | Corrected SPT value using overburden correction |
| rd | Stress reduction factor based on depth |
| CSR | Cyclic stress ratio calculated via Seed & Idriss |
| CRR | Cyclic resistance ratio (estimated via empirical model) |
| FS | Factor of safety against liquefaction |
| Soil Type | Based on Unified Soil Classification System (USCS) |
| Chart | CSR vs CRR plot with site-specific point overlay |

---

## 🧠 Methodology & Equations

- **CSR**:  
  \[
  \text{CSR} = 0.65 \cdot \frac{a_{\text{max}}}{g} \cdot \frac{\sigma_{v0}}{\sigma_{v0}'} \cdot r_d
  \]

- **CRR**:  
  Based on **Seed & Idriss (1971)** empirical SPT-based relation for clean sand and modified for fine-grained soils.

- **Factor of Safety (FS)**:  
  \[
  FS = \frac{CRR}{CSR}
  \]

- **Soil Classification**:  
  Based on D10, D30, D60, LL, PL, and percent passing 75 μm per **IS 1498** and USCS logic.

---

## 🛠 How to Run This App Locally

### 1️⃣ Clone the Repo
```bash
git clone https://github.com/yourusername/soil-liquefaction-app.git
cd soil-liquefaction-app
