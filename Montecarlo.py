import numpy as np
from scipy.optimize import brentq

# ====================================================
# Geometry and inclination
# ====================================================
R = 37.5        # cm
H = 100.0       # cm
alpha_deg = 10.0
m = np.tan(np.deg2rad(alpha_deg))

# ====================================================
# Target volume (INPUT)
# ====================================================
V_target = 58315.81  # cm^3

# ====================================================
# Monte Carlo settings
# ====================================================
N_MC = 2_000_000   # increase for higher accuracy
np.random.seed(1)

V_cyl = np.pi * R**2 * H

# ====================================================
# Monte Carlo volume estimator
# ====================================================
def monte_carlo_volume(b):
    # Sample x along cylinder axis
    x = np.random.uniform(0.0, H, N_MC)

    # Sample (y,z) uniformly in circle
    r = R * np.sqrt(np.random.uniform(0.0, 1.0, N_MC))
    theta = np.random.uniform(0.0, 2*np.pi, N_MC)
    y = r * np.cos(theta)

    # Plane condition
    below = y <= (b - m * x)

    frac = np.mean(below)
    return frac * V_cyl

# ====================================================
# Root function: MC volume - target
# ====================================================
def F(b):
    return monte_carlo_volume(b) - V_target

# ====================================================
# Solve for b
# ====================================================
b_min = -R
b_max = R + m * H

b_solution = brentq(F, b_min, b_max, maxiter=50)

# ====================================================
# Final check
# ====================================================
V_check = monte_carlo_volume(b_solution)

print("Monte Carlo inverse solution")
print("--------------------------------")
print(f"alpha = {alpha_deg:.2f} deg")
print(f"Target V = {V_target:.2f} cm^3")
print(f"Solved b = {b_solution:.6f} cm")
print(f"MC Volume = {V_check:.2f} cm^3")
