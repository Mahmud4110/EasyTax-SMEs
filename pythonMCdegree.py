import numpy as np

# ====================================================
# Geometry (FIXED)
# ====================================================
R = 37.5
H = 100.0
V_target = 58315.81

alpha_list = [89.9, 80, 70, 60, 50, 40, 30, 20, 10, 0.1]

V_cyl = np.pi * R**2 * H

# ====================================================
# Monte Carlo parameters
# ====================================================
N_MC = 1_000_000
np.random.seed(123)

print("Generating Monte Carlo samples...")

x = np.random.uniform(0.0, H, N_MC)
r = R * np.sqrt(np.random.uniform(0.0, 1.0, N_MC))
theta = np.random.uniform(0.0, 2*np.pi, N_MC)
y = r * np.cos(theta)

print("Sampling complete.")

# ====================================================
# Monte Carlo volume estimator
# ====================================================
def mc_volume(b, m):
    return np.mean(y <= (b - m * x)) * V_cyl

# ====================================================
# Monte Carlo-safe bisection solver
# ====================================================
def solve_b_mc(m, tol_vol=50.0, max_iter=80):
    """
    tol_vol: acceptable volume error in cm^3
    """
    b_lo = -R
    b_hi = R + m * H

    for _ in range(max_iter):
        b_mid = 0.5 * (b_lo + b_hi)
        V_mid = mc_volume(b_mid, m)

        if abs(V_mid - V_target) < tol_vol:
            return b_mid, V_mid

        if V_mid < V_target:
            b_lo = b_mid
        else:
            b_hi = b_mid

    return b_mid, V_mid  # best effort

# ====================================================
# Solve for each alpha
# ====================================================
results = []

for alpha_deg in alpha_list:
    m = np.tan(np.deg2rad(alpha_deg))
    b_sol, V_check = solve_b_mc(m)
    results.append((alpha_deg, b_sol, V_check))

# ====================================================
# Output
# ====================================================
print("\n Alpha (deg) |        b (cm) |   MC Volume (cm^3)")
print("---------------------------------------------------")

for a, b, V in results:
    print(f"{a:10.1f} | {b:14.6f} | {V:18.2f}")
