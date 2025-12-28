# ==========================================================
# Barrel Animation and Line Graph GIF Generator
# Author: Mahmud Tijani
# ==========================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.animation import FuncAnimation, PillowWriter

# ==========================================================
# USER INPUTS / CONFIGURATION
# ==========================================================
excel_file = r"C:\Users\Mahmud Tijani\Downloads\Documents\My Document\IMT-Atlantique\Scientific Project\Task1 Mahmud.xlsx"
sheet_name = "Task 4"  # Change this to move between sheets
gif_output = "barrel_animation_by_Mahmud_Tijani.gif"  # Output GIF file name
gif_duration = 1500  # milliseconds per frame (animation speed)

# Column mapping (change as needed for each sheet)
serial_col = "Serial_No"        # instead of A
height_col = "Height_of_liquid (cm)"        # instead of B (cm)
k_eff_col  = "K_eff"        # instead of C
alpha_col = "Alpha"        # instead of D
volume_cm_col = "Volume(cm^3)"     # instead of E (cm³)
radius_col = "Radius"        # instead of F (cm)
surface_col = "Surface Area (cm²)"       # instead of G (cm²)
surface_ratio_col = "Surface-to-Volume Ratio (cm⁻¹)" # instead of H (cm⁻¹)

# Columns for X–Y plot (change depending on what you want to plot)
x_axis_col = "Height_of_liquid (cm)"  # e.g., Liquid height
y_axis_col = "K_eff"  # e.g., K-effective
# Graph title
plot_title = "Barrel Height vs K_eff Iterations by Mahmud Tijani"

# ==========================================================
# READ EXCEL SHEET
# ==========================================================
df = pd.read_excel(excel_file, sheet_name=sheet_name)
# Extract relevant data as arrays
heights = df[height_col].to_numpy()
radii = df[radius_col].to_numpy()
x_vals = df[x_axis_col].to_numpy()
y_vals = df[y_axis_col].to_numpy()

# Barrel constants (assuming constant radius from first row)
barrel_radius = radii[0]
barrel_height = df[radius_col].iloc[0] * 2  # Approximation for visualization

# ==========================================================
# SETUP FIGURE AND AXES
# ==========================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

# ----- Left: Barrel animation -----
ax1.set_xlim(-barrel_radius * 1.2, barrel_radius * 1.2)
ax1.set_ylim(0, barrel_height * 1.2)
ax1.set_aspect('equal')
ax1.set_title("Barrel Fuel Animation")

# Barrel outline
barrel_outline = Rectangle((-barrel_radius, 0), 2 * barrel_radius, barrel_height,
                           linewidth=2, edgecolor='grey', facecolor='none')
ax1.add_patch(barrel_outline)

# Fuel patch (pink)
fuel_patch = Rectangle((-barrel_radius, 0), 2 * barrel_radius, heights[0],
                       linewidth=0, facecolor='pink')
ax1.add_patch(fuel_patch)

# ----- Right: X–Y line plot -----
line_plot, = ax2.plot([], [], 'b-o')
ax2.set_xlim(min(x_vals) - 1, max(x_vals) + 1)
ax2.set_ylim(min(y_vals) * 0.95, max(y_vals) * 1.05)
ax2.set_xlabel(x_axis_col)
ax2.set_ylabel(y_axis_col)
ax2.set_title(plot_title)

# ==========================================================
# ANIMATION FUNCTION
# ==========================================================
def update(frame):
    # Update pink fuel level
    fuel_patch.set_height(heights[frame])
    # Update line plot progression
    line_plot.set_data(x_vals[:frame + 1], y_vals[:frame + 1])
    return fuel_patch, line_plot

# ==========================================================
# CREATE ANIMATION
# ==========================================================
anim = FuncAnimation(fig, update, frames=len(heights),
                     interval=gif_duration, blit=True)

# Save animation as GIF
writer = PillowWriter(fps=1000 / gif_duration)
anim.save(gif_output, writer=writer)

print(f"GIF successfully saved as: {gif_output}")
plt.close(fig)
