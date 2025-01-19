#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 17:33:38 2025

@author: lukasgartmair
"""

from utils import d10, d6, determine_outcome, split_modifiers, clip, get_rnd_stat
import matplotlib.pyplot as plt
import random
import numpy as np    
import pandas as pd

def apply_ability_mod(x):
#TODO diff 4 not possible  
    x=abs(x)
    if 0 <= x < 2:
        return 0
    elif 2 <= x < 4:
        return 1

    
outcomes = {0:'miss', 1:'weak_hit', 2:'strong_hit'}

attacker_stats = {
    "heart": 1,
    "iron": 2,
    "edge": 2,
    "wits": 3,
    "shadow":1
}

defender_stats = {
    "heart": 2,
    "iron": 1,
    "edge": 2,
    "wits": 1,
    "shadow": 3
}

#balancing_weights = [5,10,60,10,15]
balancing_weights = [20,20,20,20,20]
advantage_dict = {
    'attacker outnumbered': -2,
    'attacker lower numbers': -1,
    'equal numbers': 0,
    'attacker slight numbers advantage': 1,
    'attacker great numbers advantage': 2
}

relevant_attributes = {
"skirmishers": "heart",
"warriors": "iron",
"archers": "edge",
"cavalry": "wits"}


close_combat_dict = {
    'skirmishers': {'skirmishers':0,'warriors': -1, 'archers':2, 'cavalry': -2},
    'warriors': {'skirmishers': 2, 'warriors':0,'archers': 3, 'cavalry': -1},
    'cavalry': {'skirmishers': 2, 'warriors': 1, 'archers': 3,'cavalry':0}
}

ranged_combat_dict = {
    'skirmishers': {'skirmishers':0,'warriors': 1 , 'archers': -2, 'cavalry': 1},
    'archers': {'skirmishers': 2, 'warriors': 3, 'archers':0, 'cavalry': 2},
}

ws = [50,50]
combat_style = ["close_combat","ranged_combat"]

roles = ["attacker", "defender"]

unit_types = {0:'skirmishers', 1:'warriors', 2:'archers', 3:'cavalry'}
        
def rnd_move():
    return (random.choice(list(unit_types.values())), random.choice(list(unit_types.values())), random.choices(combat_style, weights=ws)[0],random.choices(list(advantage_dict), weights=balancing_weights, k=1)[0])

def calculate_output(move_tuple=(None, None,None,None)):
    #attacking_unit, defending_unit, combat_style, numbers_advantage = move_tuple

    verbose = False
    
    combat_mod = None
    
    #this loop accounts for the fact that warriors can not attack archers in ranged combat. 
    #it will loop until anything valid is found
    while combat_mod is None:
    
        results = rnd_move()    
        if results[2] == "close_combat":
            if results[0] in close_combat_dict:
                combat_mod = close_combat_dict[results[0]][results[1]]
        elif results[2] == "ranged_combat":
            if results[0] in ranged_combat_dict:
                combat_mod = ranged_combat_dict[results[0]][results[1]]
        
        if combat_mod is not None:
            advantage = advantage_dict[results[3]]
            attribute_mod = 0
            
            attacker_attribute = relevant_attributes[results[0]]
            #attacker_ability = attacker_stats[attacker_attribute]
            attacker_ability = get_rnd_stat()
            attacker_units = results[0]
            defender_attribute = relevant_attributes[results[1]]
            #defender_ability = defender_stats[defender_attribute]
            defender_ability = get_rnd_stat()
            defender_units = results[1]
            attribute_mod = apply_ability_mod(attacker_ability - defender_ability)
            
            action_die = d6()
            challenge_dice = d10(), d10()
            
            original_action_die = action_die
            original_challenge_dice = challenge_dice
            
            if verbose:
                print(challenge_dice, action_die)
            player_role = random.choices(roles,weights=ws)[0]
            mods_total = combat_mod+advantage+attribute_mod

            if player_role == "attacker":
                if mods_total > 0:
                    action_die = np.clip(action_die+mods_total,0,10)
                else:
                    splits = split_modifiers(mods_total)
                    challenge_dice = clip(challenge_dice[0]+abs(splits[0])), clip(challenge_dice[1]+abs(splits[1]))
            elif player_role == "defender":
                if mods_total < 0:
                    action_die = clip(action_die+abs(mods_total))
                else:
                    splits = split_modifiers(mods_total)
                    challenge_dice = clip(challenge_dice[0]+splits[0]), clip(challenge_dice[1]+splits[1] )
                    
            outcome_numeric = determine_outcome(*challenge_dice,  action_die)
            if verbose:
                print(player_role, attacker_units, defender_units, results[2],results[3], attribute_mod, mods_total)
                print(challenge_dice, action_die, outcomes[outcome_numeric])
                print("--------------")
            
            data = player_role, attacker_units, defender_units, results[2],results[3], attribute_mod, mods_total, original_challenge_dice, original_action_die, challenge_dice, action_die, outcomes[outcome_numeric], outcome_numeric
            return data, outcome_numeric

iterations = 100000

results = []
hists = []
for i in range(iterations):
    
    data,outcome = calculate_output()
    
    results.append(data)
            
columns = ['role', 'attacker', 'defender', 'combat_style','numbers_attacker','ability_modifier','total_modifier','original_challende_challenge_dice','original_action_die', 'modifie_challenge_dice','modified_action_dice','outcome_str','outcome_numeric']
df = pd.DataFrame(results,columns=columns)

grouped = df.groupby(['role','attacker', 'defender', 'combat_style','numbers_attacker','ability_modifier'])['outcome_numeric']

hist_data = []

for name, group in grouped:
    hist, _ = np.histogram(group, bins=np.arange(0, 4), density=False)  
    sum_occurences = np.sum(hist)
    hist, _ = np.histogram(group, bins=np.arange(0, 4), density=True)  
    hist_data.append((name, hist * 100,sum_occurences))

hist_df = pd.DataFrame(hist_data, columns=["Group", "Percentages",'n_Occurences'])

group_columns = ['role','attacker', 'defender', 'combat_style','numbers_attacker','ability_modifier']
hist_df[group_columns] = pd.DataFrame(hist_df['Group'].tolist(), index=hist_df.index)
percentage_columns = ['Miss_Percentage', 'Weak_Hit_Percentage', 'Strong_Hit_Percentage']
hist_df[percentage_columns] = pd.DataFrame(hist_df['Percentages'].tolist(), index=hist_df.index)
hist_df = hist_df.drop(columns=['Group', 'Percentages'])
hist_df['numbers_attacker_numeric'] = hist_df["numbers_attacker"].map(advantage_dict)
hist_df = hist_df.sort_values(by=['attacker', 'defender','combat_style','role','numbers_attacker_numeric'])
hist_df.drop(['numbers_attacker_numeric'], axis=1, inplace=True)
hist_df = hist_df[[col for col in hist_df if col != 'n_Occurences'] + ['n_Occurences']]
hist_df = hist_df.reset_index()
hist_df.drop(['index'], axis=1, inplace=True)

subset_df = hist_df.loc[380:399]