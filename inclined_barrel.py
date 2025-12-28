import math
from scipy.integrate import quad
from scipy.optimize import brentq  # robust root finder (better than fzero in extreme cases)

def segment_area(h, R):
    h = max(min(h, R), -R)
    if h >= R:
        return math.pi * R**2
    elif h <= -R:
        return 0.0
    else:
        return R**2 * math.acos(-h / R) - h * math.sqrt(R**2 - h**2)

def exact_volume(b, R, H, m):
    if abs(m) < 1e-12:
        return H * segment_area(b, R)
    else:
        h1 = b - m * H
        h2 = b
        h_low = min(h1, h2)
        h_high = max(h1, h2)
        integrand = lambda h: segment_area(h, R)
        integral, _ = quad(integrand, h_low, h_high)
        return abs(integral / m)  # abs for safety on direction

# ====================================================
# Parameters - change these as needed
# ====================================================
R = 37.5        # cm
H = 100.0       # cm
alpha_deg = 50.0  # degrees
V_target = 58315.81  # cm³

m = math.tan(math.radians(alpha_deg))
V_full = math.pi * R**2 * H

b_min = -R
b_max = R + m * H

if V_target <= 0:
    b = b_min - 1
elif V_target >= V_full:
    b = b_max + 1
else:
    def F(b):
        return exact_volume(b, R, H, m) - V_target
    b = brentq(F, b_min, b_max)  # very reliable solver

# Results
print(f"alpha = {alpha_deg:.4f} deg")
print(f"Solution: b = {b:.8f} cm")
print(f"Verification: V = {exact_volume(b, R, H, m):.6f} cm³")