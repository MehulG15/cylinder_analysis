import os
import sys
import io
import math
import base64
from flask import Flask, send_from_directory, request, jsonify

# Set writable matplotlib config dir
os.environ['MPLCONFIGDIR'] = os.path.join(os.path.dirname(__file__), '.mplconfig')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

import thin_cylinder

app = Flask(__name__, static_folder='.')

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

@app.route('/api/calculate', methods=['POST'])
def api_calculate():
    data = request.get_json() or {}
    try:
        diameter = float(data.get('diameter', 1000.0))
        length = float(data.get('length', 3000.0))
        base_thickness = float(data.get('base_thickness', 10.0))
        base_pressure = float(data.get('base_pressure', 0.5))
        youngs_modulus = float(data.get('youngs_modulus', 200000.0))
        poissons_ratio = float(data.get('poissons_ratio', 0.3))
        
        # Calculate stresses
        hoop_base, long_base = thin_cylinder.calculate_cylinder_stresses(base_pressure, diameter, base_thickness)
        
        # Calculate dimension changes
        delta_d, delta_l, delta_v = thin_cylinder.calculate_dimension_changes(
            base_pressure, diameter, length, base_thickness, youngs_modulus, poissons_ratio
        )
        
        # Format terminal stdout exactly matching code.md
        terminal_output = (
            "--- Thin Cylinder Stress & Dimension Calculator ---\n"
            f"Internal diameter: {diameter} mm\n"
            f"Cylinder length: {length} mm\n"
            f"Wall thickness: {base_thickness} mm\n"
            f"Internal pressure: {base_pressure} N/mm²\n"
            f"Young's Modulus (E): {youngs_modulus} N/mm²\n"
            f"Poisson's ratio (μ): {poissons_ratio}\n\n"
            "--- Calculated Stresses ---\n"
            f"Hoop Stress:         {hoop_base:.3f} N/mm²\n"
            f"Longitudinal Stress: {long_base:.3f} N/mm²\n\n"
            "--- Calculated Dimension Changes ---\n"
            f"Change in Diameter (Δd): {delta_d:.5f} mm\n"
            f"Change in Length (Δl):   {delta_l:.5f} mm\n"
            f"Change in Volume (Δv):   {delta_v:.2f} mm³\n"
            "----------------------------------------------\n"
        )
        
        return jsonify({
            'diameter': diameter,
            'length': length,
            'base_thickness': base_thickness,
            'base_pressure': base_pressure,
            'youngs_modulus': youngs_modulus,
            'poissons_ratio': poissons_ratio,
            'hoop_base': hoop_base,
            'long_base': long_base,
            'delta_d': delta_d,
            'delta_l': delta_l,
            'delta_v': delta_v,
            'terminal_output': terminal_output
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/plot', methods=['POST'])
def api_plot():
    data = request.get_json() or {}
    try:
        diameter = float(data.get('diameter', 1000.0))
        base_thickness = float(data.get('base_thickness', 10.0))
        base_pressure = float(data.get('base_pressure', 0.5))
        
        pressures = np.linspace(0, base_pressure * 2, 100)
        hoop_stress_p, long_stress_p = thin_cylinder.calculate_cylinder_stresses(pressures, diameter, base_thickness)
        
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(pressures, hoop_stress_p, label='Hoop Stress', color='blue', linewidth=2)
        ax.plot(pressures, long_stress_p, label='Longitudinal Stress', color='red', linestyle='--', linewidth=2)
        ax.set_title(f'Stress vs Internal Pressure\n(Diameter={diameter}mm, Thickness={base_thickness}mm)')
        ax.set_xlabel('Internal Pressure (N/mm²)')
        ax.set_ylabel('Stress (N/mm²)')
        ax.grid(True, linestyle=':', alpha=0.7)
        ax.legend()
        plt.tight_layout()
        
        img_buf = io.BytesIO()
        plt.savefig(img_buf, format='png', dpi=120)
        plt.close(fig)
        img_buf.seek(0)
        img_b64 = base64.b64encode(img_buf.read()).decode('utf-8')
        
        return jsonify({'image': f'data:image/png;base64,{img_b64}'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting server on http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)
