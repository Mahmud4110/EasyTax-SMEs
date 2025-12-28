# ==========================================================
# Barrel Tilt Animation and k_eff vs Alpha Plot
# ==========================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import Circle
from matplotlib import cm

# ===============================
# USER CONFIGURATION
# ===============================
excel_file = r"C:\Users\Mahmud Tijani\Downloads\Documents\My Document\IMT-Atlantique\Scientific Project\Task1 Mahmud.xlsx"
sheet_name = "Task 4"  # choose sheet
gif_output = "Task4_barrel_animation.gif"
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


# X-Y graph
x_axis_col = alpha_col
y_axis_col = k_eff_col
plot_title = "k_eff vs Alpha for Inclined Barrel"

# Barrel constants
barrel_height_const = 100  # From P6, constant height
# ===============================
# READ EXCEL DATA
# ===============================
df = pd.read_excel(excel_file, sheet_name=sheet_name)

alphas = df[alpha_col].to_numpy()
k_eff_vals = df[k_eff_col].to_numpy()
radii = df[radius_col].to_numpy()
octave_vols = df[volume_octave_col].to_numpy()
surface_areas = df[surface_area_col].to_numpy()

barrel_radius = radii[0]  # assume constant
barrel_height = barrel_height_const

# ===============================
# SETUP FIGURE
# ===============================
fig = plt.figure(figsize=(12, 6))
ax3d = fig.add_subplot(121, projection='3d')
ax2d = fig.add_subplot(122)

# Set limits for 3D barrel
ax3d.set_xlim(-barrel_radius*1.5, barrel_radius*1.5)
ax3d.set_ylim(-barrel_radius*1.5, barrel_radius*1.5)
ax3d.set_zlim(0, barrel_height*1.2)
ax3d.set_box_aspect([1,1,barrel_height/barrel_radius])  # proportional aspect
ax3d.set_title("Tilted Barrel with Fuel")

# 2D plot setup
ax2d.set_xlim(min(alphas)-5, max(alphas)+5)
ax2d.set_ylim(min(k_eff_vals)*0.95, max(k_eff_vals)*1.05)
ax2d.set_xlabel("Alpha (deg)")
ax2d.set_ylabel("k_eff")
ax2d.set_title(plot_title)
line_plot, = ax2d.plot([], [], 'b-o')

# ===============================
# CREATE BARREL MESH FUNCTION
# ===============================
def barrel_surface(radius, height, alpha_deg, n_theta=50, n_height=20):
    """
    Returns X, Y, Z coordinates of a tilted cylinder
    """
    theta = np.linspace(0, 2*np.pi, n_theta)
    z = np.linspace(0, height, n_height)
    Theta, Z = np.meshgrid(theta, z)
    X = radius * np.cos(Theta)
    Y = radius * np.sin(Theta)
    # Apply tilt about X-axis by alpha
    alpha_rad = np.deg2rad(alpha_deg)
    Z_tilted = Z * np.cos(alpha_rad) - Y * np.sin(alpha_rad)
    Y_tilted = Z * np.sin(alpha_rad) + Y * np.cos(alpha_rad)
    return X, Y_tilted, Z_tilted

# ===============================
# CREATE FUEL PATCH FUNCTION
# ===============================
def fuel_surface(radius, H, alpha_deg, vol):
    """
    Approximate fuel height for given Octave volume
    V = pi * r^2 * h for horizontal cylinder (approx)
    Then tilt with alpha
    """
    h_fuel = vol / (np.pi * radius**2)
    return barrel_surface(radius, h_fuel, alpha_deg)

# ===============================
# ANIMATION FUNCTION
# ===============================
def update(frame):
    ax3d.cla()
    # Plot tilted barrel (transparent)
    Xb, Yb, Zb = barrel_surface(barrel_radius, barrel_height, alphas[frame])
    ax3d.plot_surface(Xb, Yb, Zb, color='grey', alpha=0.2, linewidth=0, shade=True)

    # Plot fuel inside barrel
    Xf, Yf, Zf = fuel_surface(barrel_radius, barrel_height, alphas[frame], octave_vols[frame])
    ax3d.plot_surface(Xf, Yf, Zf, color='magenta', alpha=0.6, linewidth=0, shade=True)

    ax3d.set_xlim(-barrel_radius*1.5, barrel_radius*1.5)
    ax3d.set_ylim(-barrel_radius*1.5, barrel_radius*1.5)
    ax3d.set_zlim(0, barrel_height*1.2)
    ax3d.set_box_aspect([1,1,barrel_height/barrel_radius])
    ax3d.set_title(f"Barrel Tilt: {alphas[frame]:.1f} deg")

    # Update 2D line plot
    line_plot.set_data(alphas[:frame+1], k_eff_vals[:frame+1])
    return Xb, Yb, Zb, Xf, Yf, Zf, line_plot

# ===============================
# CREATE ANIMATION
# ===============================
anim = FuncAnimation(fig, update, frames=len(alphas), interval=gif_duration, blit=False)
writer = PillowWriter(fps=1000/gif_duration)
anim.save(gif_output, writer=writer)
print(f"GIF saved as {gif_output}")
plt.close(fig)
