# ==========================================================
# 2D Standing Cylinder + Fuel Volume + k_eff vs Alpha
# Author: Mahmud Tijani
# ==========================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.animation import FuncAnimation, PillowWriter

# ==========================================================
# USER CONFIGURATION
# ==========================================================
excel_file = r"C:\Users\Mahmud Tijani\Downloads\Documents\My Document\IMT-Atlantique\Scientific Project\Task1 Mahmud.xlsx"
sheet_name = "Task 4"
gif_output = "task4_2D_cylinder_FINAL.gif"
gif_duration = 1500  # ms per frame

# ==========================================================
# ==========================================================
serial_col           = "S/N"   # or "Serial_No"
height_col           = "Height_of_liquid (cm)"   # Height of liquid (cm) - average or reference
k_eff_col            = "K_eff"   # k_eff
alpha_col            = "Alpha"   # alpha (degrees)
volume_cm3_col       = "Volume(cm^3)"   # Target volume (cm³)
radius_col           = "Radius"   # Radius (cm) - same for barrel and liquid
volume_liters_col    = "Volume(litres)"   # Volume in Liters
volume_octave_col    = "Volume in Octave (cm^3)"   # Volume from Octave/Serpent (cm³)
surface_area_col     = "Surface(cm^2)"   # Surface area (cm²)
surface_ratio_col    = "surface_area_vol_ratio (cm ^ -1)"   # Surface-to-volume ratio
m_col                = "m"   # slope m = tan(alpha)
b_col                = "b"   # intercept b (cm)


# ==========================================================
# READ EXCEL
# ==========================================================
df = pd.read_excel(excel_file, sheet_name=sheet_name)
df.columns = df.columns.str.strip()

# Sort correctly (1 → 30)
df = df.sort_values(by=serial_col).reset_index(drop=True)

alpha_vals = df[alpha_col].to_numpy()
k_eff_vals = df[k_eff_col].to_numpy()
radii      = df[radius_col].to_numpy()
volumes    = df[volume_octave_col].to_numpy()

# ==========================================================
# BARREL CONSTANT
# ==========================================================
BARREL_HEIGHT = max(volumes / (np.pi * radii**2)) * 1.1

# ==========================================================
# FIGURE SETUP
# ==========================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))

# -----------------------------
# LEFT: 2D CYLINDER
# -----------------------------
ax1.set_aspect("equal")
ax1.set_xlim(-max(radii)*1.3, max(radii)*1.3)
ax1.set_ylim(0, BARREL_HEIGHT*1.1)
ax1.set_title("2D Standing Cylinder (Fuel Volume)")
ax1.set_axis_off()

# Barrel outline
barrel_outline = Rectangle(
    (-radii[0], 0),
    2*radii[0],
    BARREL_HEIGHT,
    linewidth=2,
    edgecolor="gray",
    facecolor="none"
)
ax1.add_patch(barrel_outline)

# Fuel patch
fuel_patch = Rectangle(
    (-radii[0], 0),
    2*radii[0],
    0,
    linewidth=0,
    facecolor="pink",
    alpha=0.85
)
ax1.add_patch(fuel_patch)

# -----------------------------
# RIGHT: GRAPH
# -----------------------------
ax2.set_title("k_eff vs Alpha")
ax2.set_xlabel("Alpha (degrees)")
ax2.set_ylabel("k_eff")
line_plot, = ax2.plot([], [], "b-o")

ax2.set_xlim(min(alpha_vals), max(alpha_vals))
ax2.set_ylim(k_eff_vals.min()*0.98, k_eff_vals.max()*1.02)

# ==========================================================
# UPDATE FUNCTION
# ==========================================================
def update(frame):

    R = radii[frame]
    V = volumes[frame]

    # Compute fuel height from volume
    h_fuel = V / (np.pi * R**2)
    h_fuel = min(h_fuel, BARREL_HEIGHT)

    # Update barrel
    barrel_outline.set_xy((-R, 0))
    barrel_outline.set_width(2*R)
    barrel_outline.set_height(BARREL_HEIGHT)

    # Update fuel
    fuel_patch.set_xy((-R, 0))
    fuel_patch.set_width(2*R)
    fuel_patch.set_height(h_fuel)

    # Update graph
    line_plot.set_data(
        alpha_vals[:frame+1],
        k_eff_vals[:frame+1]
    )

    return fuel_patch, line_plot

# ==========================================================
# CREATE & SAVE GIF
# ==========================================================
anim = FuncAnimation(
    fig,
    update,
    frames=len(df),
    interval=gif_duration,
    blit=True
)

writer = PillowWriter(fps=1000/gif_duration)
anim.save(gif_output, writer=writer)

plt.close(fig)
print(f"✅ 2D cylinder GIF saved as: {gif_output}")
