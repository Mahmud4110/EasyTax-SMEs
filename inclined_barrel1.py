import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

# ====================================================
# Geometry & target volume
# ====================================================
R = 37.5       # cm
H = 100.0       # cm
V_target = 41840.46  # cm^3

alpha_list = [89.9, 80, 70, 60, 50, 40, 30, 20, 10, 0.1]

V_full = np.pi * R**2 * H


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
# Exact inclined cylinder volume
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
# Solve for b for each alpha
# ====================================================
results = []

for alpha_deg in alpha_list:
    m = np.tan(np.deg2rad(alpha_deg))

    b_min = -R
    b_max = R + m * H

    if V_target <= 0:
        b_solution = b_min - 1
    elif V_target >= V_full:
        b_solution = b_max + 1
    else:
        def F(b):
            return exact_volume(b, R, H, m) - V_target

        b_solution = brentq(F, b_min, b_max)

    V_check = exact_volume(b_solution, R, H, m)
    results.append((alpha_deg, b_solution, V_check))


# ====================================================
# Display results
# ====================================================
print(f"{'Alpha (deg)':>12} | {'b (cm)':>14} | {'Volume (cm^3)':>15}")
print("-" * 47)

for alpha, b, V in results:
    print(f"{alpha:12.1f} | {b:14.8f} | {V:15.6f}")
