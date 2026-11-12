# Thin Cylinder Stress & Dimension Calculator Web Application

This web application is a faithful, interactive web implementation of the exact Python code provided in `code.md`.

**The code from `code.md` is strictly preserved without any modifications.**

---

## 🚀 How to Run the Website

### Option 1: Double-Click or Open Directly in Browser (Zero Installation)
Simply open [index.html](file:///d:/Projects/anmolvmech2/index.html) in your browser (Google Chrome, Microsoft Edge, Firefox, Brave, Safari).
- Instant real-time interactivity.
- Sliders and numeric inputs for all parameters:
  - Internal Diameter ($d$) [mm] *(e.g., 1000)*
  - Cylinder Length ($l$) [mm] *(e.g., 3000)*
  - Wall Thickness ($t$) [mm] *(e.g., 10)*
  - Internal Pressure ($p$) [N/mm²] *(e.g., 0.5)*
  - Young's Modulus ($E$) [N/mm²] *(e.g., 200000 for steel)*
  - Poisson's ratio ($\mu$) *(e.g., 0.3)*

### Option 2: Run with Python Web Server
```bash
python app.py
```
Then visit **http://localhost:5000** in your browser.

---

## 📊 Features & Exact Code Faithfulness

1. **Calculated Stresses** (from `calculate_cylinder_stresses`):
   - **Hoop Stress**: $\sigma_h = \frac{\text{pressure} \times \text{diameter}}{2 \times \text{thickness}}$ (displayed in `N/mm²` to 3 decimals)
   - **Longitudinal Stress**: $\sigma_l = \frac{\text{pressure} \times \text{diameter}}{4 \times \text{thickness}}$ (displayed in `N/mm²` to 3 decimals)

2. **Calculated Dimension Changes** (from `calculate_dimension_changes`):
   - **Change in Diameter ($\Delta d$)**: $\frac{p \cdot d^2}{4 \cdot t \cdot E} \times (2 - \mu)$ (in `mm` to 5 decimals)
   - **Change in Length ($\Delta l$)**: $\frac{p \cdot d \cdot l}{4 \cdot t \cdot E} \times (1 - 2\mu)$ (in `mm` to 5 decimals)
   - **Original Internal Volume ($v$)**: $\frac{\pi}{4} \cdot d^2 \cdot l$ (in `mm³`)
   - **Change in Volume ($\Delta v$)**: $\frac{p \cdot d \cdot v}{4 \cdot t \cdot E} \times (5 - 4\mu)$ (in `mm³` to 2 decimals)

3. **The Single Graph**:
   - Exactly matches the Python code:
     - **Title**: `Stress vs Internal Pressure (Diameter={diameter}mm, Thickness={base_thickness}mm)`
     - **X-axis**: `Internal Pressure (N/mm²)` across range `[0, base_pressure * 2]`
     - **Y-axis**: `Stress (N/mm²)`
     - **Hoop Stress**: Solid Blue line
     - **Longitudinal Stress**: Red dashed line (`--`)
     - **Grid**: Dotted (`:`) with alpha 0.7
     - **Legend**: Included
