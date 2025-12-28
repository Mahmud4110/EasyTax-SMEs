import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

# ====================================================
# Fixed geometry
# ====================================================
R = 37.5        # cm
H = 100.0       # cm
alpha_deg = 0.1  # <<< SET SINGLE ALPHA HERE
m = np.tan(np.deg2rad(alpha_deg))

# Example volumes (V1 → V10)
V_list = [
    58315.81, 55165.81, 52015.81, 48865.81, 45715.81,
    42565.81, 39415.81, 36265.81, 33115.81, 29965.81
]

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
# Exact inclined-cylinder volume
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
# Solve b for each volume
# ====================================================
print(f"alpha = {alpha_deg:.2f} deg")
print(f"{'V_target (cm^3)':>18} | {'b (cm)':>12} | {'V_check (cm^3)':>16}")
print("-" * 52)

for V_target in V_list:

    if V_target <= 0:
        b_sol = -R - 1
    elif V_target >= V_full:
        b_sol = R + m * H + 1
    else:
        b_min = -R
        b_max = R + m * H

        def F(b):
            return exact_volume(b, R, H, m) - V_target

        b_sol = brentq(F, b_min, b_max)

    V_check = exact_volume(b_sol, R, H, m)

    print(f"{V_target:18.1f} | {b_sol:12.6f} | {V_check:16.2f}")
