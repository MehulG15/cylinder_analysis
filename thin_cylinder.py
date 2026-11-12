import numpy as np
import matplotlib.pyplot as plt
import math

def calculate_cylinder_stresses(pressure, diameter, thickness):
    """
    Calculates hoop and longitudinal stresses for a thin-walled cylinder.
    """
    hoop_stress = (pressure * diameter) / (2 * thickness)
    longitudinal_stress = (pressure * diameter) / (4 * thickness)
    return hoop_stress, longitudinal_stress

def calculate_dimension_changes(pressure, diameter, length, thickness, E, mu):
    """
    Calculates the change in diameter, length, and volume for a thin cylinder.
    Formulas based on provided reference image.
    """
    # Change in Diameter (Delta d)
    delta_d = (pressure * diameter**2) / (4 * thickness * E) * (2 - mu)
    
    # Change in Length (Delta l)
    delta_l = (pressure * diameter * length) / (4 * thickness * E) * (1 - 2 * mu)
    
    # Original internal volume (v)
    v = (math.pi / 4) * (diameter**2) * length
    
    # Change in Volume (Delta v)
    delta_v = (pressure * diameter * v) / (4 * thickness * E) * (5 - 4 * mu)
    
    return delta_d, delta_l, delta_v

if __name__ == "__main__":
    print("--- Thin Cylinder Stress & Dimension Calculator ---")
    try:
        # Take user input for geometric and loading conditions
        diameter = float(input("Enter the internal diameter (in mm, e.g., 1000): "))
        length = float(input("Enter the cylinder length (in mm, e.g., 3000): "))
        base_thickness = float(input("Enter the wall thickness (in mm, e.g., 10): "))
        base_pressure = float(input("Enter the internal pressure (in N/mm², e.g., 0.5): "))
        
        # Material properties
        youngs_modulus = float(input("Enter Young's Modulus (E) (in N/mm², e.g., 200000 for steel): "))
        poissons_ratio = float(input("Enter Poisson's ratio (μ) (e.g., 0.3): "))
        
        # Calculate stresses 
        hoop_base, long_base = calculate_cylinder_stresses(base_pressure, diameter, base_thickness)
        
        # Calculate dimension changes
        delta_d, delta_l, delta_v = calculate_dimension_changes(
            base_pressure, diameter, length, base_thickness, youngs_modulus, poissons_ratio
        )
        
        # Display the calculated values
        print("\n--- Calculated Stresses ---")
        print(f"Hoop Stress:         {hoop_base:.3f} N/mm²")
        print(f"Longitudinal Stress: {long_base:.3f} N/mm²")
        
        print("\n--- Calculated Dimension Changes ---")
        print(f"Change in Diameter (Δd): {delta_d:.5f} mm")
        print(f"Change in Length (Δl):   {delta_l:.5f} mm")
        print(f"Change in Volume (Δv):   {delta_v:.2f} mm³")
        print("----------------------------------------------\n")
        
        # Generate ranges based on user inputs to show variations (Stress only)
        pressures = np.linspace(0, base_pressure * 2, 100)
        hoop_stress_p, long_stress_p = calculate_cylinder_stresses(pressures, diameter, base_thickness)

        thicknesses = np.linspace(base_thickness * 0.2, base_thickness * 2, 100)
        hoop_stress_t, long_stress_t = calculate_cylinder_stresses(base_pressure, diameter, thicknesses)

        # --- Plotting the Results ---

        # Plot : Stresses vs Internal Pressure
        plt.plot(pressures, hoop_stress_p, label='Hoop Stress', color='blue', linewidth=2)
        plt.plot(pressures, long_stress_p, label='Longitudinal Stress', color='red', linestyle='--', linewidth=2)
        plt.title(f'Stress vs Internal Pressure\n(Diameter={diameter}mm, Thickness={base_thickness}mm)')
        plt.xlabel('Internal Pressure (N/mm²)')
        plt.ylabel('Stress (N/mm²)')
        plt.grid(True, linestyle=':', alpha=0.7)
        plt.legend()
        plt.tight_layout()
        plt.show()

    except ValueError:
        print("Invalid input detected. Please run the code again and enter numerical values only.")
