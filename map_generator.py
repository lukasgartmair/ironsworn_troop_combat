#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 17:05:53 2025

@author: lukasgartmair
"""

import numpy as np
import random
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi
from noise import pnoise2
from scipy.ndimage import binary_dilation, gaussian_filter
import string
from faker import Faker
from scipy.stats import qmc

f = Faker()


def add_random_points(map_grid, x_range, y_range, n=2):

    n = random.randint(2, 10)

    num_points = 100
    sampler = qmc.Halton(d=2, scramble=False)
    points = sampler.random(num_points)

    points = np.floor(points * map_size).astype(int)

    num_points = 100
    sampler = qmc.Halton(d=2, scramble=False)
    points = sampler.random(num_points)
    points = np.floor(points * map_size).astype(int)
    mask2 = map_grid[points[:, 0], points[:, 1]] != terrain_mapping["Water"]
    valid_points = points[mask2]

    n = random.randint(2, 10)
    if valid_points.shape[0] < n:
        raise ValueError(
            f"Not enough valid points found. Only {valid_points.shape[0]} valid points."
        )

    random_rows = valid_points[
        np.random.choice(valid_points.shape[0], n, replace=False)
    ]

    for x, y in random_rows:
        name = f.city()
        plt.scatter(x, y, label=name)
        plt.text(x, y, name, fontsize=12, ha="right", va="bottom")


terrain_strategies = {
    # "Deep Water": {"water_threshold": 0.2, "mountain_threshold": None},
    # "Shallow Water": {"water_threshold": 0.4, "mountain_threshold": None},
    # "Flat Land": {"water_threshold": 0.5, "mountain_threshold": 0.3},
    # "Plains": {"water_threshold": None, "mountain_threshold": 0.4},
    # "Hills": {"water_threshold": None, "mountain_threshold": 0.6},
    # "Swamp": {"water_threshold": 0.45, "mountain_threshold": 0.35},
    # "Rocky Terrain": {"water_threshold": None, "mountain_threshold": 0.75},
    # "Mountains": {"water_threshold": None, "mountain_threshold": 0.9},
    "Lakes": {"water_threshold": 0.6, "mountain_threshold": 0.65},
    # "Snowy Peaks": {"water_threshold": None, "mountain_threshold": 0.95},
    # "Volcanic Rock": {"water_threshold": None, "mountain_threshold": 0.85},
}

terrain_strategy = random.choice(list(terrain_strategies))

terrain_colors = {
    1: (0.3, 0.8, 0.3),
    2: (0.1, 0.5, 0.1),
    3: (0.5, 0.5, 0.5),
    4: (0.1, 0.3, 0.8),
    5: (0.9, 0.9, 0.6),
    6: (0.6, 0.4, 0.2),
    7: (0.2, 0.6, 0.2),
    8: (0.8, 0.8, 0.5),
    9: (0.7, 0.7, 0.7),
    10: (0.3, 0.3, 0.3),
}

terrain_mapping = {
    "Grassland": 1,
    "Forest": 2,
    "Mountain": 3,
    "Water": 4,
    "Sand": 5,
    "Rocky Terrain": 6,
    "Swamp": 7,
    "Plains": 8,
    "Snowy Peaks": 9,
    "Volcanic Rock": 10,
}

sigma = 10
diltation_filter = 10
map_size = 300
width, height = map_size, map_size
num_points = random.randint(10, 70)

points = np.array(
    [[random.randint(0, width), random.randint(0, height)] for _ in range(num_points)]
)
terrain_types = [random.choice([1, 2]) for _ in range(num_points)]

vor = Voronoi(points)

map_grid = np.zeros((height, width), dtype=int)

for y in range(height):
    for x in range(width):
        distances = np.linalg.norm(points - np.array([x, y]), axis=1)
        nearest_seed = np.argmin(distances)
        map_grid[y, x] = terrain_types[nearest_seed]

elevation = np.array(
    [
        [pnoise2(x / 100, y / 100, octaves=8) for x in range(width)]
        for y in range(height)
    ]
)
elevation = (elevation - elevation.min()) / (elevation.max() - elevation.min())

elevation_mask = elevation > 0.1

dilated_elevation = binary_dilation(
    elevation_mask, structure=np.ones((diltation_filter, diltation_filter))
)
dilated_elevation = gaussian_filter(elevation, sigma=sigma)

if terrain_strategies[terrain_strategy]["mountain_threshold"]:
    map_grid = np.where(
        elevation > terrain_strategies[terrain_strategy]["mountain_threshold"],
        terrain_mapping["Mountain"],
        map_grid,
    )
if terrain_strategies[terrain_strategy]["water_threshold"]:
    map_grid = np.where(
        elevation > terrain_strategies[terrain_strategy]["water_threshold"],
        terrain_mapping["Water"],
        map_grid,
    )

color_map = np.array([[terrain_colors[cell] for cell in row] for row in map_grid])
color_map = np.array(
    [
        [
            np.array(terrain_colors[cell]) * (0.5 + 0.5 * elevation[y, x])
            for x, cell in enumerate(row)
        ]
        for y, row in enumerate(map_grid)
    ]
)
color_map = np.array(
    [
        [
            np.array(terrain_colors[cell]) * (0.5 + 0.5 * dilated_elevation[y, x])
            for x, cell in enumerate(row)
        ]
        for y, row in enumerate(map_grid)
    ]
)

plt.figure(figsize=(10, 10))
plt.imshow(color_map, interpolation="bicubic")
tick_divider = 50
plt.axis("on")
plt.grid(True, color="black", linewidth=0.2, linestyle="-", alpha=0.5)
plt.xticks(np.arange(0, map_size, tick_divider))
plt.gca().set_xticklabels(
    [letter for letter in string.ascii_uppercase[: map_size // tick_divider]]
)
plt.yticks(np.arange(0, map_size, tick_divider))
plt.gca().set_yticklabels(np.arange(1, map_size // tick_divider + 1))
plt.tick_params(
    axis="x", labelsize=10, labelrotation=0, direction="inout", length=6, width=1
)
plt.tick_params(
    axis="y", labelsize=10, labelrotation=0, direction="inout", length=6, width=1
)
add_random_points(map_grid, width, height)

plt.show()
