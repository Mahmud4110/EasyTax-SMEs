# ==========================================================
# 3D Inclined Barrel + Plane-Defined Fuel + k_eff vs Alpha
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
gif_output = "task4_inclined_barrel_FINAL.gif"
gif_duration = 1500  # ms per frame

# ==========================================================
# COLUMN MAPPING (adjust if names differ slightly)
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
df.columns = df.columns.str.strip()  # safety

alpha_vals = np.deg2rad(df[alpha_col].to_numpy())  # radians
k_eff_vals = df[k_eff_col].to_numpy()
radii      = df[radius_col].to_numpy()
m_vals     = df[m_col].to_numpy()
b_vals     = df[b_col].to_numpy()

# Barrel height (constant – P6)
BARREL_HEIGHT = max(b_vals) + max(radii)

# ==========================================================
# FIGURE SETUP
# ==========================================================
fig = plt.figure(figsize=(14, 7))

# --- 3D Barrel ---
ax3d = fig.add_subplot(121, projection="3d")
ax3d.set_box_aspect((1, 1, 2))
ax3d.set_axis_off()

# --- Graph ---
ax2 = fig.add_subplot(122)
ax2.set_title("k_eff vs Alpha")
ax2.set_xlabel("Alpha (degrees)")
ax2.set_ylabel("k_eff")
line_plot, = ax2.plot([], [], "b-o")

ax2.set_xlim(np.rad2deg(alpha_vals).min(), np.rad2deg(alpha_vals).max())
ax2.set_ylim(k_eff_vals.min()*0.98, k_eff_vals.max()*1.02)

# ==========================================================
# GEOMETRY DRAWING FUNCTION
# ==========================================================
def draw_cylinder(ax, R, H, alpha, m, b):

    ax.cla()
    ax.set_box_aspect((1, 1, 2))
    ax.set_axis_off()
    ax.set_title("Inclined Barrel with Plane-Defined Spent Fuel")

    # ===============================
    # BARREL (transparent gray)
    # ===============================
    theta = np.linspace(0, 2*np.pi, 80)
    z = np.linspace(0, H, 80)
    theta_grid, z_grid = np.meshgrid(theta, z)

    X = R * np.cos(theta_grid)
    Y = R * np.sin(theta_grid)

    Xr = X
    Yr = Y*np.cos(alpha) - z_grid*np.sin(alpha)
    Zr = Y*np.sin(alpha) + z_grid*np.cos(alpha)

    ax.plot_surface(
        Xr, Yr, Zr,
        color="gray",
        alpha=0.25,
        linewidth=0,
        shade=True
    )

    # ===============================
    # FUEL (defined by plane z = m*x + b)
    # ===============================
    x = np.linspace(-R, R, 140)
    y = np.linspace(-R, R, 140)
    Xp, Yp = np.meshgrid(x, y)

    inside = Xp**2 + Yp**2 <= R**2

    Zp = m*Xp + b
    Zp = np.clip(Zp, 0, H)
    Zp[~inside] = np.nan

    Xpf = Xp
    Ypf = Yp*np.cos(alpha) - Zp*np.sin(alpha)
    Zpf = Yp*np.sin(alpha) + Zp*np.cos(alpha)

    ax.plot_surface(
        Xpf, Ypf, Zpf,
        color="pink",
        alpha=0.9,
        linewidth=0,
        shade=True
    )

    # ===============================
    # VIEW
    # ===============================
    ax.view_init(elev=22, azim=35)

# ==========================================================
# ANIMATION UPDATE
# ==========================================================
def update(frame):

    draw_cylinder(
        ax3d,
        R=radii[frame],
        H=BARREL_HEIGHT,
        alpha=alpha_vals[frame],
        m=m_vals[frame],
        b=b_vals[frame]
    )

    line_plot.set_data(
        np.rad2deg(alpha_vals[:frame+1]),
        k_eff_vals[:frame+1]
    )

    return line_plot,

# ==========================================================
# CREATE & SAVE GIF
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
print(f"✅ GIF successfully saved as: {gif_output}")
