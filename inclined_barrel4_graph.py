# ==========================================================
# 3D Inclined Barrel + K_eff vs Alpha Animation (Task 4)
# Author: Mahmud Tijani
# ==========================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from mpl_toolkits.mplot3d import Axes3D

# ==========================================================
# USER CONFIGURATION
# ==========================================================
excel_file = r"C:\Users\Mahmud Tijani\Downloads\Documents\My Document\IMT-Atlantique\Scientific Project\Task1 Mahmud.xlsx"
sheet_name = "Task 4"
gif_output = "task4_inclined_barrel_3D.gif"
gif_duration = 1500  # ms per frame

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
# READ DATA
# ==========================================================
df = pd.read_excel(excel_file, sheet_name=sheet_name)

alpha_vals   = np.deg2rad(df[alpha_col].to_numpy())   # radians
k_eff_vals   = df[k_eff_col].to_numpy()
heights      = df[height_col].to_numpy()
radii        = df[radius_col].to_numpy()
volumes      = df[volume_octave_col].to_numpy()

# Barrel constants
BARREL_HEIGHT = df[height_col].max()   # P6 constant
FUEL_DENSITY  = 1.0                    # P3 placeholder (adjust if needed)

# ==========================================================
# FIGURE SETUP
# ==========================================================
fig = plt.figure(figsize=(14, 7))

# ---- 3D Barrel ----
ax3d = fig.add_subplot(121, projection="3d")
ax3d.set_title("Inclined 3D Barrel (Isometric View)")
ax3d.set_box_aspect((1, 1, 2))
ax3d.set_axis_off()

# ---- Graph ----
ax2 = fig.add_subplot(122)
ax2.set_title("k_eff vs Alpha")
ax2.set_xlabel("Alpha (degrees)")
ax2.set_ylabel("k_eff")
line_plot, = ax2.plot([], [], "b-o")

ax2.set_xlim(np.rad2deg(alpha_vals).min(), np.rad2deg(alpha_vals).max())
ax2.set_ylim(k_eff_vals.min()*0.98, k_eff_vals.max()*1.02)

# ==========================================================
# CYLINDER GENERATOR
# ==========================================================
def draw_cylinder(ax, radius, height, alpha, fill_height):

    ax.cla()
    ax.set_title("Inclined 3D Barrel (Isometric View)")
    ax.set_box_aspect((1, 1, 2))
    ax.set_axis_off()

    theta = np.linspace(0, 2*np.pi, 50)
    z = np.linspace(0, height, 50)
    theta_grid, z_grid = np.meshgrid(theta, z)

    x = radius * np.cos(theta_grid)
    y = radius * np.sin(theta_grid)

    # Inclination rotation
    x_rot = x
    y_rot = y*np.cos(alpha) - z_grid*np.sin(alpha)
    z_rot = y*np.sin(alpha) + z_grid*np.cos(alpha)

    # Barrel surface
    ax.plot_surface(x_rot, y_rot, z_rot,
                    color="lightgrey", alpha=0.25, linewidth=0)

    # ======================
    # Fuel (filled volume)
    # ======================
    zf = np.linspace(0, fill_height, 40)
    theta_f, zf_grid = np.meshgrid(theta, zf)

    xf = radius * np.cos(theta_f)
    yf = radius * np.sin(theta_f)

    xf_rot = xf
    yf_rot = yf*np.cos(alpha) - zf_grid*np.sin(alpha)
    zf_rot = yf*np.sin(alpha) + zf_grid*np.cos(alpha)

    ax.plot_surface(xf_rot, yf_rot, zf_rot,
                    color="pink", alpha=0.85, linewidth=0)

    # View angle
    ax.view_init(elev=20, azim=40)

# ==========================================================
# ANIMATION UPDATE
# ==========================================================
def update(frame):

    draw_cylinder(
        ax3d,
        radius=radii[frame],
        height=BARREL_HEIGHT,
        alpha=alpha_vals[frame],
        fill_height=heights[frame]
    )

    line_plot.set_data(
        np.rad2deg(alpha_vals[:frame+1]),
        k_eff_vals[:frame+1]
    )

    return line_plot,

# ==========================================================
# CREATE & SAVE ANIMATION
# ==========================================================
anim = FuncAnimation(
    fig,
    update,
    frames=len(df),
    interval=gif_duration,
    blit=False
)

writer = PillowWriter(fps=1000/gif_duration)
anim.save(gif_output, writer=writer)

plt.close(fig)
print(f"GIF saved successfully: {gif_output}")
