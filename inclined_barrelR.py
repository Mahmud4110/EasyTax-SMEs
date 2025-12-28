import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

# ====================================================
# Input parameters
# ====================================================
V_barrel = 441786.4669     # total cylinder volume (cm^3) – fixed
V_fuel = 58315.8136      # spent fuel volume (cm^3) – fixed
alpha_deg = 0.1       # fixed inclination
m = np.tan(np.deg2rad(alpha_deg))

# List of barrel radii to explore
R_list = np.array([35.25, 36.00, 36.75, 37.50, 38.25, 39.00, 39.75, 40.50, 41.25, 42.00])  # 10 barrel radii

# ====================================================
# Circular segment area
# ====================================================
def segment_area(h, R):
    h = np.clip(h, -R, R)
    if h >= R:
        return np.pi * R**2
    elif h <= -R:
        return 0.0
    else:
        return R**2 * np.arccos(-h / R) - h * np.sqrt(R**2 - h**2)

# ====================================================
# Exact inclined cylinder volume (liquid)
# ====================================================
def exact_volume(b, R, H, m):
    if abs(m) < 1e-12:
        return H * segment_area(b, R)
    else:
        h1 = b - m * H
        h2 = b
        V, _ = quad(lambda h: segment_area(h, R), h1, h2)
        return V / m

# ====================================================
# Solve for b for each radius
# ====================================================
results = []

for R in R_list:
    # Compute barrel height to keep total volume constant
    H = V_barrel / (np.pi * R**2)

    # Brackets for b
    b_min = -R
    b_max = R + m * H

    # Solve b for the spent fuel volume
    if V_fuel <= 0:
        b_solution = b_min - 1
    elif V_fuel >= V_barrel:
        b_solution = b_max + 1
    else:
        def F(b):
            return exact_volume(b, R, H, m) - V_fuel
        b_solution = brentq(F, b_min, b_max)

    # Verification
    V_check = exact_volume(b_solution, R, H, m)
    results.append((R, H, b_solution, V_check))

# ====================================================
# Display results
# ====================================================
print(f"{'Radius (cm)':>12} | {'Height (cm)':>12} | {'b (cm)':>14} | {'Fuel Vol (cm^3)':>15}")
print("-" * 65)
for R, H, b, V in results:
    print(f"{R:12.2f} | {H:12.4f} | {b:14.8f} | {V:15.6f}")
