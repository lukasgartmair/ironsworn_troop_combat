#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 11:44:46 2025

@author: lukasgartmair
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.cm import viridis

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

roles = ["attacker", "defender"]

df = subset_df[["role", "numbers_attacker","ability_modifier","Miss_Percentage","Weak_Hit_Percentage","Strong_Hit_Percentage"]]

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap

# Assuming 'df' is your DataFrame with the relevant data

# Roles and categories
roles = df["role"].unique()
categories = df["numbers_attacker"].unique()

x = np.arange(len(categories))  # Base positions for categories
width = 0.2  # Bar width
space_between = 0.05  # Extra space between each category group

# Create subplots with one subplot for each role
fig, axs = plt.subplots(nrows=len(roles), ncols=1, figsize=(12, 6 * len(roles)))  # Adjust size for multiple subplots

# Create colormap
cmap = get_cmap("RdYlGn")

# Iterate over roles and plot each one on a separate subplot
for r, role in enumerate(roles):
    ax = axs[r]  # Get the corresponding axis for the role
    
    # Filter data by role
    for i, modifier in enumerate(sorted(df["ability_modifier"].unique())):
        sub_data = df[(df["role"] == role) & (df["ability_modifier"] == modifier)]
        
        # Normalize the data for color mapping (from 0 to 1)
        norm = plt.Normalize(vmin=sub_data["Miss_Percentage"].min(), vmax=sub_data["Miss_Percentage"].max())
        
        # Adjust bar positions for each role with space between the categories
        ax.bar(
            x + (i - 1) * width + r * width * 2 + x * space_between,  # Offset for each role + space between categories
            sub_data["Miss_Percentage"], 
            width, 
            label=f"{role.title()} - Miss (Mod {modifier})" if r == 0 and i == 0 else ""
        )
        ax.bar(
            x + (i - 1) * width + r * width * 2 + x * space_between, 
            sub_data["Weak_Hit_Percentage"], 
            width, 
            bottom=sub_data["Miss_Percentage"],
            label=f"{role.title()} - Weak Hit (Mod {modifier})" if r == 0 and i == 0 else ""
        )
        ax.bar(
            x + (i - 1) * width + r * width * 2 + x * space_between, 
            sub_data["Strong_Hit_Percentage"], 
            width, 
            bottom=sub_data["Miss_Percentage"] + sub_data["Weak_Hit_Percentage"],
            label=f"{role.title()} - Strong Hit (Mod {modifier})" if r == 0 and i == 0 else ""
        )
    
    # Customize the individual subplot
    ax.set_title(f"Combat Outcomes for {role.title()}")
    ax.set_xticks(x + (len(roles) - 1) * width * 2 / 2)  # Adjust xticks to center the categories
    ax.set_xticklabels(categories, rotation=45)
    ax.set_ylabel("Percentage")
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    ax.legend(ncol=1)

# Final adjustments
plt.tight_layout()
plt.show()
