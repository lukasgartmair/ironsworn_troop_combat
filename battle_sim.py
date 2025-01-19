#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 17:33:38 2025

@author: lukasgartmair
"""

from utils import d10, d6, determine_outcome, apply_ability_mod

import random
import numpy as np


def apply_ability_mod(x):
    return abs(x // 2)


attacker_stats = {"heart": 1, "iron": 2, "edge": 2, "wits": 3, "shadow": 1}

defender_stats = {"heart": 2, "iron": 1, "edge": 2, "wits": 1, "shadow": 3}

ws = [50, 50]
combat_style = ["close_combat", "ranged_combat"]

roles = ["attacker", "defender"]

balancing_weights = [5, 10, 60, 10, 15]
advantage_dict = {
    "outnumbered": -2,
    "lower numbers": -1,
    "equal numbers": 0,
    "slight numbers advantage": 1,
    "great numbers advantage": 2,
}

units = {
    "skirmishers": 5,
    "warriors": 30,
    "archers": 10,
    "cavalry": 10,
    # "elite forces": 5,
    # "mages": 0
}

relevant_attributes = {
    "skirmishers": "heart",
    "warriors": "iron",
    "archers": "edge",
    "cavalry": "wits",
    # "elite forces": "shadow",
    # "mages": "essence"  # or "chaos" if preferred
}

# convention: xy = close_combat, yx = ranged_combat
# 0,1 is skirm in close combat against a warrior
# 1,2 is a warrior in ranged combat against an archer

close_combat_dict = {
    "skirmishers": {"skirmishers": 0, "warriors": -1, "archers": 2, "cavalry": -2},
    "warriors": {"skirmishers": 2, "warriors": 0, "archers": 3, "cavalry": -1},
    "cavalry": {"skirmishers": 2, "warriors": 1, "archers": 3, "cavalry": 0},
}

ranged_combat_dict = {
    "skirmishers": {"skirmishers": 0, "warriors": 1, "archers": -2, "cavalry": 1},
    "archers": {"skirmishers": 2, "warriors": 3, "archers": 0, "cavalry": 1},
}


def rnd_move():
    return (
        random.choice(list(units)),
        random.choice(list(units)),
        random.choices(combat_style, weights=ws)[0],
        random.choices(list(advantage_dict), weights=balancing_weights, k=1)[0],
    )


iterations = 3

for i in range(iterations):

    print("")

    combat_mod = None

    while combat_mod is None:

        results = rnd_move()
        if results[2] == "close_combat":
            if results[0] in close_combat_dict:
                combat_mod = close_combat_dict[results[0]][results[1]]
        elif results[2] == "ranged_combat":
            if results[0] in ranged_combat_dict:
                combat_mod = ranged_combat_dict[results[0]][results[1]]

        if combat_mod is not None:
            print("Combat Situation {}".format(i))

            print("{} vs. {} in {} with {}".format(*results))
            print()
            advantage = advantage_dict[results[3]]
            attribute_mod = 0

            attacker_attribute = relevant_attributes[results[0]]
            attacker_ability = attacker_stats[attacker_attribute]
            my_units = results[0]
            defender_attribute = relevant_attributes[results[1]]
            defender_ability = defender_stats[defender_attribute]
            defender_units = results[1]
            print(
                "relevant_attacker_ability: {} : {}".format(
                    attacker_attribute, attacker_ability
                )
            )
            print(
                "relevant_defender_ability: {} : {}".format(
                    defender_attribute, defender_ability
                )
            )
            attribute_mod = apply_ability_mod(attacker_ability - defender_ability)
            print(
                "Ability mod calculation: {} : {} - {} : {} = {}".format(
                    attacker_attribute,
                    attacker_ability,
                    defender_attribute,
                    defender_ability,
                    attacker_ability - defender_ability,
                )
            )
            print()
            print(
                "Initial: {}, Applied: {}".format(
                    attacker_ability - defender_ability, attribute_mod
                )
            )
            print()
            print(
                "class difference {} vs. {} in {} is {}".format(
                    my_units, defender_units, results[2], combat_mod
                )
            )
            print()
            print(
                "Modifiers: class vs class: {}, numbers difference: {}, ability difference {}".format(
                    combat_mod, advantage, attribute_mod
                )
            )
            print()
            print("Dice Roll")
            my_action_die = d6()
            enemy_dice = d10(), d10()
            print("[{}, {}] vs. {}".format(*enemy_dice, my_action_die))
            print()
            modifiers_sum = combat_mod + advantage + attribute_mod
            print("Modifiers final sum")
            print(modifiers_sum)

            my_role = random.choices(roles, weights=ws)[0]
            print()
            print("My role is to be the {}".format(my_role))
            print()
            mods = combat_mod + advantage + attribute_mod
            if my_role == "attacker":
                modified_action_die = min(my_action_die + mods, 10)
            else:

                modified_action_die = max(my_action_die - mods, 1)

            print("Modifiers applied")
            print(modified_action_die)

            outcome = determine_outcome(*enemy_dice, modified_action_die)
            print()
            print("Outcome: {}".format(outcome))
