#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 20:21:28 2025

@author: lukasgartmair
"""

import numpy as np
import random


def get_rnd_stat():
    return random.randint(1, 3)


def clip(x):
    return np.clip(x, 0, 10)


def split_modifiers(v):

    v1 = v // 2 + v % 2
    v2 = v // 2
    return v1, v2


def determine_outcome(a, b, res):

    a = clip(a)
    b = clip(b)
    res = clip(res)

    if res > a and res > b:
        return 2
    elif res > a and res <= b:
        return 1
    elif res > b and res <= a:
        return 1
    else:
        return 0


def n_chance(p=0.85):
    if np.random.rand() < p:
        # print("chance True")
        return True
    else:
        # print("chance False")
        return False


def d10():
    return random.randint(1, 10)


def d100():
    return random.randint(1, 100)


def d6():
    return random.randint(1, 6)


def d4():
    return random.randint(0, 3)
