#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 20:37:24 2025

@author: lukasgartmair
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from utils import (
    d10,
    d6,
    determine_outcome,
    split_modifiers,
    apply_modifier_to_inverse_challenge_dice,
)

# def simulate():
n = 200000
data = []
results = []
hists = []
values = list(range(-4, 7))

outcomes = {0: "miss", 1: "weak_hit", 2: "strong_hit"}
outcome_order = {"miss": 0, "weak_hit": 1, "strong_hit": 2}

cases = {0: "Act_Die", 1: "Ch_Die_1", 2: "Ch_Die_2", 3: "Split", 4: "Split"}

# for j in range(4):
for j in [0, 4]:
    for v in values:
        for i in range(n):

            x = d6()
            a = d10()
            b = d10()

            apply_modifier_to_inverse_challenge_dice

            if j == 0:
                x = x + v
            elif j == 4:
                v1, v2 = split_modifiers(v)
                a, b = apply_modifier_to_inverse_challenge_dice(a, b, v1, v2)
            # elif j == 1:
            #     a = a + v
            # elif j == 2:
            #     b = b + v
            # elif j == 3:
            #     v1 = v // 2 + v % 2
            #     v2 = v // 2

            #     a = a + v1
            #     b = b + v2

            result = determine_outcome(a, b, x)

            data.append((cases[j], i, v, a, b, x, result))
            results.append(result)
        percentages, bin_edges = np.histogram(
            results, bins=3, weights=[1 / len(results)] * len(results)
        )
        percentages = percentages * 100
        results = []

        hists.append((cases[j], v, [np.round(q, 1) for q in list(percentages)]))

outcomes = {0: "miss", 1: "weak_hit", 2: "strong_hit"}

# Create DataFrame
df = pd.DataFrame(hists)
expanded_cols = pd.DataFrame(df[2].tolist(), columns=["miss", "weak_hit", "strong_hit"])

df_tmp = pd.concat([df.drop(columns=[2]), expanded_cols], axis=1).iloc[::-1]

melted_df = df_tmp.melt(
    id_vars=[0, 1],
    value_vars=["miss", "weak_hit", "strong_hit"],
    var_name="Outcome",
    value_name="prob",
)

melted_df["Case_Outcome"] = melted_df["Outcome"] + " (" + melted_df[0].astype(str) + ")"

outcome_order = {"miss": 0, "weak_hit": 1, "strong_hit": 2}
melted_df["Outcome_Num"] = melted_df["Outcome"].map(outcome_order)

melted_df["Case_Outcome"] = melted_df["Outcome"] + " (" + melted_df[0].astype(str) + ")"

heatmap_data = melted_df.pivot(index=1, columns="Case_Outcome", values="prob")
heatmap_data = heatmap_data.round()


# Plot Heatmap
fig, ax = plt.subplots(figsize=(12, 12))
sns.heatmap(
    heatmap_data, annot=True, fmt=".2f", cmap="Oranges", cbar_kws={"label": "prob"}
)
plt.title("Heatmap of Outcome Probabilities")
plt.xlabel("Case and Outcome")
plt.ylabel("Modification Value")
ax.tick_params(axis="x", rotation=45)
ax.invert_yaxis()
plt.show()

# Bin the 'prob' values into 5 categories
bins = [0, 10, 25, 45, 55, 75, 90, 100]
labels = [1, 2, 3, 4, 5, 6, 7]
label_mapping = {
    1: "extremely unlikely",
    2: "very unlikely",
    3: "less than equal",
    4: "about equal",
    5: "more than equal",
    6: "verly likely",
    7: "exremely likely",
}

heatmap_data_binned = heatmap_data.apply(
    lambda x: pd.cut(x, bins=bins, labels=labels, include_lowest=True)
)
heatmap_data_binned = heatmap_data_binned.astype(int)
heatmap_data_binned = heatmap_data_binned.round(0)

mapped_df = heatmap_data_binned.applymap(lambda x: label_mapping.get(x, x))

plt.figure(figsize=(12, 8))
ax = sns.heatmap(
    heatmap_data_binned, annot=mapped_df, fmt="s", cmap="Oranges", cbar=False
)
plt.title("Heatmap of Outcome Probabilities")
plt.xlabel("Case and Outcome")
plt.ylabel("Modification Value")
ax.invert_yaxis()
plt.xticks(rotation=25, ha="right")
plt.show()


# Initialize an empty list to collect rows for the new DataFrame
all_combinations = []

for idx in mapped_df.index:

    row = mapped_df.loc[idx]

    action_die_combination = {
        (
            row["miss (Act_Die)"],
            row["strong_hit (Act_Die)"],
            row["weak_hit (Act_Die)"],
        ): ("Action Die", idx)
    }
    challnge_dice_combination = {
        (row["miss (Split)"], row["strong_hit (Split)"], row["weak_hit (Split)"]): (
            "Challenge Dice",
            idx,
        )
    }

    all_combinations.append(action_die_combination)
    all_combinations.append(challnge_dice_combination)


# Initialize empty lists to store data
miss = []
strong_hit = []
weak_hit = []
modified_die = []
modificator = []

# Populate the lists with data
for entry in all_combinations:
    for outcome, mod_value in entry.items():
        miss_val, strong_hit_val, weak_hit_val = outcome
        miss.append(miss_val)
        strong_hit.append(strong_hit_val)
        weak_hit.append(weak_hit_val)
        modified_die.append(
            mod_value[0]
        )  # Extracting the die type ("Action" or "Chllenge")
        modificator.append(mod_value[1])

# Create the DataFrame
df = pd.DataFrame(
    {
        "miss": miss,
        "strong_hit": strong_hit,
        "weak_hit": weak_hit,
        "modified die": modified_die,
        "modificator": modificator,
    }
)

reverse_mapping = {v: k for k, v in label_mapping.items()}

df["miss_rank"] = df["miss"].map(reverse_mapping)
df["strong_hit_rank"] = df["strong_hit"].map(reverse_mapping)
df["weak_hit_rank"] = df["weak_hit"].map(reverse_mapping)

# Sort based on these ranks
sorted_df = df.sort_values(by=["miss_rank", "strong_hit_rank", "weak_hit_rank"]).drop(
    columns=["miss_rank", "strong_hit_rank", "weak_hit_rank"]
)

sorted_df["Action Die"] = np.nan
sorted_df["Lower Challenge Die"] = np.nan
sorted_df["Higher Challenge Die"] = np.nan

sorted_df.loc[sorted_df["modified die"] == "Action Die", "Action Die"] = sorted_df[
    "modificator"
]

vectorized_split = np.vectorize(split_modifiers)
sorted_df.loc[
    sorted_df["modified die"] == "Challenge Dice",
    ["Lower Challenge Die", "Higher Challenge Die"],
] = list(
    zip(
        *vectorized_split(
            sorted_df.loc[sorted_df["modified die"] == "Challenge Dice", "modificator"]
        )
    )
)
sorted_df.drop(["modified die", "modificator"], axis=1, inplace=True)
