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
# Surface area estimator
# ====================================================
def mc_surface_area(b, m):
    """
    Approximate surface area of the fuel inside the cylinder for given b and m.
    """
    # Only points inside the fuel (y <= b - m*x)
    inside = y <= (b - m*x)
    y_in = y[inside]
    x_in = x[inside]
    
    if len(x_in) == 0:
        return 0.0
    
    # Approximate top surface as convex hull area in 2D projection (x-y plane)
    # Here we just approximate using lateral + mean top segment
    lateral = 2 * np.pi * R * np.mean(np.clip(b - m * x_in, 0, R))
    
    # Top segment area (numerical, average of circular segments)
    y_top = np.clip(b - m * x_in, -R, R)
    theta = np.arccos(-y_top/R)
    top_area = np.mean(R**2 * theta - y_top * np.sqrt(R**2 - y_top**2))
    
    return lateral + top_area

# ====================================================
# Monte Carlo-safe bisection solver
# ====================================================
def solve_b_mc(m, tol_vol=50.0, max_iter=80):
    """
    Returns b, volume, surface area for given slope m.
    """
    b_lo = -R
    b_hi = R + m * H

    for _ in range(max_iter):
        b_mid = 0.5 * (b_lo + b_hi)
        V_mid = mc_volume(b_mid, m)

        if abs(V_mid - V_target) < tol_vol:
            SA_mid = mc_surface_area(b_mid, m)
            return b_mid, V_mid, SA_mid

        if V_mid < V_target:
            b_lo = b_mid
        else:
            b_hi = b_mid

    # best effort if not converged
    SA_mid = mc_surface_area(b_mid, m)
    return b_mid, V_mid, SA_mid

# ====================================================
# Solve for each alpha
# ====================================================
results = []

for alpha_deg in alpha_list:
    m = np.tan(np.deg2rad(alpha_deg))
    b_sol, V_check, SA = solve_b_mc(m)
    results.append((alpha_deg, b_sol, V_check, SA))

# ====================================================
# Output
# ====================================================
print("\n Alpha (deg) |        b (cm) |   MC Volume (cm^3) |  Surface Area (cm^2)")
print("--------------------------------------------------------------------------")
for a, b, V, SA in results:
    print(f"{a:10.1f} | {b:14.6f} | {V:18.2f} | {SA:18.2f}")
