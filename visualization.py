#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 11:11:37 2025

@author: lukasgartmair
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

roles = ["attacker", "defender"]

df = subset_df[["role", "numbers_attacker","ability_modifier","Miss_Percentage","Weak_Hit_Percentage","Strong_Hit_Percentage"]]

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.cm import viridis


# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# from matplotlib.cm import viridis

# # Roles and categories
# roles = df["role"].unique()
# categories = df["numbers_attacker"].unique()

# x = np.arange(len(categories))  # Base positions for categories
# width = 0.25  # Bar width

# fig, ax = plt.subplots(figsize=(24, 6))

# # Iterate over roles
# for r, role in enumerate(roles):
#     # Filter data by role
#     for i, modifier in enumerate(sorted(df["ability_modifier"].unique())):
#         sub_data = df[(df["role"] == role) & (df["ability_modifier"] == modifier)]
        
#         # Adjust bar positions for each role
#         ax.bar(
#             x + (i - 1) * width + r * width * 2,  # Offset for each role
#             sub_data["Miss_Percentage"], 
#             width, 
#             label=f"{role.title()} - Miss (Mod {modifier})" if r == 0 and i == 0 else ""
#         )
#         ax.bar(
#             x + (i - 1) * width + r * width * 2, 
#             sub_data["Weak_Hit_Percentage"], 
#             width, 
#             bottom=sub_data["Miss_Percentage"],
#             label=f"{role.title()} - Weak Hit (Mod {modifier})" if r == 0 and i == 0 else ""
#         )
#         ax.bar(
#             x + (i - 1) * width + r * width * 2, 
#             sub_data["Strong_Hit_Percentage"], 
#             width, 
#             bottom=sub_data["Miss_Percentage"] + sub_data["Weak_Hit_Percentage"],
#             label=f"{role.title()} - Strong Hit (Mod {modifier})" if r == 0 and i == 0 else ""
#         )

# # Customize plot
# ax.set_title("Combat Outcomes by Role, Numbers Attacker, and Ability Modifier")
# ax.set_xticks(x)
# ax.set_xticklabels(categories, rotation=45, ha="right")
# ax.set_ylabel("Percentage")
# ax.grid(axis='y', linestyle='--', alpha=0.7)
# ax.legend(ncol=2)

# plt.tight_layout()
# plt.show()


# categories = df["numbers_attacker"].unique()
# x = np.arange(len(categories))
# width = 0.25

# fig, ax = plt.subplots(figsize=(24, 6))

# for i, modifier in enumerate(sorted(df["ability_modifier"].unique())):
#     sub_data = df[df["ability_modifier"] == modifier]
#     ax.bar(
#         x + (i - 1) * width, sub_data["Miss_Percentage"], width, label=f"Miss (Mod {modifier})"
#     )
#     ax.bar(
#         x + (i - 1) * width, sub_data["Weak_Hit_Percentage"], width, bottom=sub_data["Miss_Percentage"],
#         label=f"Weak Hit (Mod {modifier})"
#     )
#     ax.bar(
#         x + (i - 1) * width, sub_data["Strong_Hit_Percentage"], width, bottom=sub_data["Miss_Percentage"] + sub_data["Weak_Hit_Percentage"],
#         label=f"Strong Hit (Mod {modifier})"
#     )

# # Customize plot
# ax.set_title("Combat Outcomes by Numbers Attacker and Ability Modifier")
# ax.set_xticks(x)
# ax.set_xticklabels(categories, rotation=45, ha="right")
# ax.set_ylabel("Percentage")
# ax.grid(axis='y', linestyle='--', alpha=0.7)

# plt.tight_layout()
# plt.show()
