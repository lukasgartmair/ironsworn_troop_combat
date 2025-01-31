#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 08:02:32 2025

@author: lukasgartmair
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from utils import d10, d6, determine_outcome


def simulate():
    n = 100000
    data = []
    results = []
    hists = []
    values = list(range(-4, 6))

    outcomes = {0: "miss", 1: "weak_hit", 2: "strong_hit"}
    outcome_order = {"miss": 0, "weak_hit": 1, "strong_hit": 2}

    cases = {0: "Act_Die", 1: "Ch_Die_1", 2: "Ch_Die_2", 3: "Split"}

    # for j in range(4):
    for j in [0, 3]:
        for v in values:
            for i in range(n):

                x = d6()
                a = d10()
                b = d10()

                if j == 0:
                    x = x + v
                elif j == 1:
                    a = a + v
                elif j == 2:
                    b = b + v
                elif j == 3:
                    v1 = v // 2 + v % 2
                    v2 = v // 2

                    a = a + v1
                    b = b + v2

                result = determine_outcome(a, b, x)

                data.append((cases[j], i, v, a, b, x, result))
                results.append(result)
            percentages, bin_edges = np.histogram(
                results, bins=3, weights=[1 / len(results)] * len(results)
            )
            percentages = percentages * 100
            results = []

            hists.append((cases[j], v, [np.round(q, 1) for q in list(percentages)]))

    # df = pd.DataFrame(hists)
    # expanded_cols = pd.DataFrame(
    #     df[2].tolist(), columns=["miss", "weak_hit", "strong_hit"]
    # )

    # for xy in range(3):
    #     fig, ax = plt.subplots()
    #     df_tmp = pd.concat([df.drop(columns=[2]), expanded_cols], axis=1).iloc[::-1]
    #     heatmap_data = df_tmp.pivot(index=1, columns=0, values=outcomes[xy])
    #     sns.heatmap(heatmap_data, annot=True, fmt=".2f", cmap="coolwarm_r")
    #     plt.title("Heatmap of {} Probabilities".format(outcomes[xy]))
    #     plt.xlabel("Case")
    #     plt.ylabel("Modification Value")
    #     ax.invert_yaxis()
    #     plt.show()

    import pandas as pd
    import seaborn as sns
    import matplotlib.pyplot as plt

    outcomes = {0: "miss", 1: "weak_hit", 2: "strong_hit"}

    # Create DataFrame
    df = pd.DataFrame(hists)
    expanded_cols = pd.DataFrame(
        df[2].tolist(), columns=["miss", "weak_hit", "strong_hit"]
    )

    # Combine Data
    df_tmp = pd.concat([df.drop(columns=[2]), expanded_cols], axis=1).iloc[::-1]
    # melted_df = df_tmp.melt(
    #     id_vars=[0, 1],
    #     value_vars=["miss", "weak_hit", "strong_hit"],
    #     var_name="Outcome",
    #     value_name="prob"
    # )

    # # Create Pivot Table for Heatmap
    # heatmap_data = melted_df.pivot_table(
    #     index=1, columns=["Outcome", 0], values="prob"
    # )

    # # Plot Heatmap
    # fig,ax = plt.subplots(figsize=(12, 12))
    # sns.heatmap(
    #     heatmap_data, annot=True, fmt=".2f", cmap="coolwarm_r", cbar_kws={"label": "prob"}
    # )
    # plt.title("Heatmap of Outcome Probabilities")
    # plt.xlabel("Case and Outcome")
    # plt.ylabel("Modification Value")
    # ax.tick_params(axis='x', rotation=45)
    # plt.show()

    melted_df = df_tmp.melt(
        id_vars=[0, 1],
        value_vars=["miss", "weak_hit", "strong_hit"],
        var_name="Outcome",
        value_name="prob",
    )

    melted_df["Case_Outcome"] = (
        melted_df["Outcome"] + " (" + melted_df[0].astype(str) + ")"
    )

    outcome_order = {"miss": 0, "weak_hit": 1, "strong_hit": 2}
    melted_df["Outcome_Num"] = melted_df["Outcome"].map(outcome_order)

    melted_df["Case_Outcome"] = (
        melted_df["Outcome"] + " (" + melted_df[0].astype(str) + ")"
    )

    heatmap_data = melted_df.pivot(index=1, columns="Case_Outcome", values="prob")
    heatmap_data = heatmap_data.round()
    plt.figure(figsize=(12, 8))
    ax = sns.heatmap(
        heatmap_data, annot=True, fmt=".1f", cmap="Oranges", cbar_kws={"label": "prob"}
    )
    plt.title("Heatmap of Outcome Probabilities")
    plt.xlabel("Case and Outcome")
    plt.ylabel("Modification Value")
    ax.invert_yaxis()
    plt.xticks(rotation=25, ha="right")
    plt.show()


if __name__ == "__main__":
    simulate()
