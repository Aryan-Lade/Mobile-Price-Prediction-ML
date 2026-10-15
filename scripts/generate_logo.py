import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Create a clean, crisp circular emblem for Ramdeobaba University
fig, ax = plt.subplots(figsize=(3, 3), dpi=300)
ax.set_aspect('equal')
ax.axis('off')

# Outer gold ring
circle_gold = plt.Circle((0.5, 0.5), 0.48, color='#c97a2b', fill=False, lw=3)
ax.add_patch(circle_gold)

# Inner blue ring
circle_blue = plt.Circle((0.5, 0.5), 0.44, color='#174375', fill=False, lw=16)
ax.add_patch(circle_blue)

# Text inside blue ring
# We can place "RAMDEOBABA UNIVERSITY" on arc or nicely styled
ax.text(0.5, 0.88, "RAMDEOBABA UNIVERSITY", color='white', fontsize=7.5, fontweight='bold',
        ha='center', va='center', fontname='Arial')
ax.text(0.5, 0.12, "ESTD. 1984 • NAGPUR", color='white', fontsize=6.5, fontweight='bold',
        ha='center', va='center', fontname='Arial')

# Center orange/gold background
center_bg = plt.Circle((0.5, 0.5), 0.36, color='#fef0de', ec='#c97a2b', lw=1.5)
ax.add_patch(center_bg)

# Temple / Emblem icon in center
# Saffron inner circle
inner_sun = plt.Circle((0.5, 0.5), 0.28, color='#ea7317', alpha=0.9)
ax.add_patch(inner_sun)

# Temple tower / rays stylized
rays = 12
for i in range(rays):
    angle = i * (2 * np.pi / rays)
    r1 = 0.29
    r2 = 0.34
    x1, y1 = 0.5 + r1 * np.cos(angle), 0.5 + r1 * np.sin(angle)
    x2, y2 = 0.5 + r2 * np.cos(angle), 0.5 + r2 * np.sin(angle)
    ax.plot([x1, x2], [y1, y2], color='#ea7317', lw=1.5)

# Center temple motif (white / gold temple outline)
temple_x = [0.42, 0.5, 0.58, 0.55, 0.55, 0.45, 0.45]
temple_y = [0.45, 0.62, 0.45, 0.45, 0.38, 0.38, 0.45]
ax.fill(temple_x, temple_y, color='white', ec='#c97a2b', lw=1)

# Center flame / kalash top
flame = plt.Circle((0.5, 0.635), 0.02, color='#ffd166', ec='#ea7317', lw=0.8)
ax.add_patch(flame)

# Ribbon / banner at bottom
ribbon_x = [0.3, 0.7, 0.65, 0.5, 0.35]
ribbon_y = [0.22, 0.22, 0.18, 0.19, 0.18]

plt.xlim(0, 1)
plt.ylim(0, 1)
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

logo_path = Path("c:/Users/wwa90/OneDrive/Desktop/MLProject/reports/report_figures/university_logo.png")
plt.savefig(logo_path, dpi=300, transparent=True)
plt.close()
print("University logo generated at:", logo_path)
