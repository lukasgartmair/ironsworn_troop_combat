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

from scipy.ndimage import binary_dilation, binary_erosion, gaussian_filter

# Terrain classification based on elevation thresholds
# Terrain classification based on elevation thresholds
terrain_strategies = {
    "Deep Water": {"water_threshold": 0.2, "mountain_threshold": None},
    "Shallow Water": {"water_threshold": 0.4, "mountain_threshold": None},
    "Flat Land": {"water_threshold": 0.5, "mountain_threshold": 0.3},
    "Plains": {"water_threshold": None, "mountain_threshold": 0.4},
    "Hills": {"water_threshold": None, "mountain_threshold": 0.6},
    "Swamp": {"water_threshold": 0.45, "mountain_threshold": 0.35},
    "Rocky Terrain": {"water_threshold": None, "mountain_threshold": 0.75},
    "Mountains": {"water_threshold": None, "mountain_threshold": 0.9},
    "Snowy Peaks": {"water_threshold": None, "mountain_threshold": 0.95},
    "Volcanic Rock": {"water_threshold": None, "mountain_threshold": 0.85}
}

terrain_strategy = random.choice(list(terrain_strategies))

# Extended terrain colors (RGB values)
terrain_colors = {
    1: (0.3, 0.8, 0.3),  # Grassland (Green)
    2: (0.1, 0.5, 0.1),  # Forest (Dark Green)
    3: (0.5, 0.5, 0.5),  # Mountain (Gray)
    4: (0.1, 0.3, 0.8),  # Water (Blue)
    5: (0.9, 0.9, 0.6),  # Sand (Beige)
    6: (0.6, 0.4, 0.2),  # Rocky Terrain (Brown)
    7: (0.2, 0.6, 0.2),  # Swamp (Dark Olive)
    8: (0.8, 0.8, 0.5),  # Plains (Light Yellow-Green)
    9: (0.7, 0.7, 0.7),  # Snowy Peaks (Light Gray)
    10: (0.3, 0.3, 0.3)  # Volcanic Rock (Dark Gray)
}

# Map terrain names to keys
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
    "Volcanic Rock": 10
}

map_size = 300
# Map size
width, height = map_size, map_size  
num_points = random.randint(10,70)  # Number of Voronoi seed points

# Generate random Voronoi seed points
points = np.array([[random.randint(0, width), random.randint(0, height)] for _ in range(num_points)])
terrain_types = [random.choice([1, 2]) for _ in range(num_points)]  # Assign Grassland or Forest

# Compute Voronoi diagram
vor = Voronoi(points)

# Create a grid to store terrain types
map_grid = np.zeros((height, width), dtype=int)

# Assign each grid cell to the nearest Voronoi seed
for y in range(height):
    for x in range(width):
        distances = np.linalg.norm(points - np.array([x, y]), axis=1)
        nearest_seed = np.argmin(distances)  # Find closest Voronoi center
        map_grid[y, x] = terrain_types[nearest_seed]  # Assign terrain

# Generate Perlin noise for elevation
elevation = np.array([[pnoise2(x / 100, y / 100, octaves=8) for x in range(width)] for y in range(height)])
elevation = (elevation - elevation.min()) / (elevation.max() - elevation.min())  # Normalize to [0,1]

# Create a binary mask based on elevation thresholds
elevation_mask = elevation > 0.5  # Adjust threshold for desired effect

# Apply dilation to the elevation mask
dilated_elevation = binary_dilation(elevation_mask, structure=np.ones((5, 5)))  # Use a 3x3 square kernel
dilated_elevation = gaussian_filter(elevation, sigma=2)

if terrain_strategies[terrain_strategy]["mountain_threshold"]:
    map_grid = np.where(elevation > terrain_strategies[terrain_strategy]["mountain_threshold"], terrain_mapping["Mountain"], map_grid)
if terrain_strategies[terrain_strategy]["water_threshold"]:
    map_grid = np.where(elevation > terrain_strategies[terrain_strategy]["water_threshold"], terrain_mapping["Water"], map_grid)

# Convert terrain types to color values
color_map = np.array([[terrain_colors[cell] for cell in row] for row in map_grid])
color_map = np.array([[np.array(terrain_colors[cell]) * (0.5 + 0.5 * elevation[y, x]) for x, cell in enumerate(row)] for y, row in enumerate(map_grid)])

# Recalculate color map based on dilated elevation mask
color_map = np.array([[np.array(terrain_colors[cell]) * (0.5 + 0.5 * dilated_elevation[y, x]) for x, cell in enumerate(row)] for y, row in enumerate(map_grid)])

# Plot the terrain map
plt.figure(figsize=(10, 10))
plt.imshow(color_map, interpolation="nearest")
# plt.scatter(points[:, 0], points[:, 1], c="black", marker="x")  # Show Voronoi seed points
plt.axis("off")  # Hide axes
plt.show()
