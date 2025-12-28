# ==========================================================
# Inclined Barrel SIDE VIEW Animation + Live Graph (FINAL FIXED - Correct Tilt & Volume)
# Author: Mahmud Tijani
# ==========================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.animation import FuncAnimation, PillowWriter

# ==========================================================
# USER INPUTS / CONFIGURATION
# ==========================================================
excel_file = r"C:\Users\Mahmud Tijani\Downloads\Documents\My Document\IMT-Atlantique\Scientific Project\Task1 Mahmud.xlsx"
sheet_name = "Task 4"
gif_output = "inclined_barrel_sideview_corrected_task4_by_Mahmud_Tijani.gif"
gif_duration_ms = 800

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
# GRAPH SETTINGS (vs Alpha - as you set)
# ==========================================================
x_axis_col = alpha_col
y_axis_col = k_eff_col
plot_title = "k_eff vs Alpha (degrees) - Inclined Fuel by Mahmud Tijani"

# ==========================================================
# READ DATA
# ==========================================================
df = pd.read_excel(excel_file, sheet_name=sheet_name)

alphas_deg   = df[alpha_col].to_numpy()
radii        = df[radius_col].to_numpy()
volumes_cm3  = df[volume_cm3_col].to_numpy()
k_effs       = df[k_eff_col].to_numpy()
ms           = df[m_col].to_numpy()
bs           = df[b_col].to_numpy()

R = radii[0]
H_barrel = 100
width = 2 * R   # horizontal span

# ==========================================================
# SETUP FIGURE
# ==========================================================
fig, (ax_barrel, ax_graph) = plt.subplots(1, 2, figsize=(14, 7), gridspec_kw={'width_ratios': [1, 1.5]})

ax_barrel.set_xlim(-width/2 * 1.2, width/2 * 1.2)
ax_barrel.set_ylim(0, H_barrel * 1.2)
ax_barrel.set_aspect('equal')
ax_barrel.set_title("Barrel Side View - Inclined Fuel (Corrected Tilt)\n(by Mahmud Tijani)", fontsize=12)

barrel_rect = plt.Rectangle((-width/2, 0), width, H_barrel,
                            edgecolor='black', facecolor='none', linewidth=3)
ax_barrel.add_patch(barrel_rect)
ax_barrel.hlines(0, -width/2, width/2, color='black', linewidth=3)
ax_barrel.hlines(H_barrel, -width/2, width/2, color='black', linewidth=3)

fuel_poly = Polygon([[0,0]], facecolor='deeppink', alpha=0.7, edgecolor='red', linewidth=2)
ax_barrel.add_patch(fuel_poly)

info_text = ax_barrel.text(-width/2 * 1.05, H_barrel * 1.1, "", fontsize=11, ha='left', va='top',
                           bbox=dict(facecolor='white', alpha=0.9, edgecolor='gray'))

# Graph
line_plot, = ax_graph.plot([], [], 'o-', color='blue', linewidth=2.5, markersize=7)
ax_graph.set_xlim(alphas_deg.min() * 0.95, alphas_deg.max() * 1.05)
ax_graph.set_ylim(k_effs.min() * 0.99, k_effs.max() * 1.01)
ax_graph.set_xlabel("Alpha (degrees)")
ax_graph.set_ylabel("k_eff")
ax_graph.set_title(plot_title)
ax_graph.grid(True, alpha=0.4)

# ==========================================================
# UPDATE FUNCTION - CORRECT TILT DIRECTION
# ==========================================================
def update(frame):
    alpha = alphas_deg[frame]
    m_val = ms[frame]
    b_val = bs[frame]
    vol = volumes_cm3[frame]
    keff = k_effs[frame]
    
    # Liquid height at walls: y = m*x + b  (x from -R left to +R right)
    y_left  = m_val * (-R) + b_val   # left wall
    y_right = m_val * ( R) + b_val   # right wall
    
    # Clip to barrel
    y_left  = np.clip(y_left,  0, H_barrel)
    y_right = np.clip(y_right, 0, H_barrel)
    
    # Polygon vertices: clockwise or counterclockwise for proper fill
    # Bottom left → bottom right → right top (liquid level) → left top (liquid level)
    points = np.array([
        [-R, 0],
        [ R, 0],
        [ R, y_right],
        [-R, y_left]
    ])
    
    fuel_poly.set_xy(points)
    
    info_text.set_text(
        f"Frame: {frame+1}/{len(df)}\n"
        f"α = {alpha:.2f}°\n"
        f"Volume = {vol:,.0f} cm³\n"
        f"k_eff = {keff:.5f}\n"
        f"m = {m_val:.4f}\n"
        f"b = {b_val:.3f} cm\n"
        f"Left height: {y_left:.1f} cm | Right: {y_right:.1f} cm"
    )
    
    # Graph vs alpha
    line_plot.set_data(alphas_deg[:frame+1], k_effs[:frame+1])
    
    return fuel_poly, info_text, line_plot

# ==========================================================
# SAVE ANIMATION
# ==========================================================
anim = FuncAnimation(fig, update, frames=len(df), interval=gif_duration_ms, blit=False, repeat=True)

fps = max(1, round(1000 / gif_duration_ms))
writer = PillowWriter(fps=fps)
anim.save(gif_output, writer=writer)

print(f"✅ Final corrected GIF saved: {gif_output}")
print(f"   Now with PROPER tilt direction for high α (89.9° → fuel piles on right edge for high volume)")
print(f"   Graph correctly vs Alpha as you wanted")

plt.close(fig)