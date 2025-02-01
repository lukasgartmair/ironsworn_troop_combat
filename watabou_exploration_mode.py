#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  1 09:21:45 2025

@author: lukasgartmair
"""

import pygame
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import numpy as np
from PIL import Image, ImageFilter
import urllib
import random

# TODO change here to load / generate new map

need_new_map = False

map_types = ["city", "realm"]
map_type = map_types[0]

scale_factor = 2


block_size = 300

covering_alpha = 253
cover_color = (
    random.randint(0, 200),
    random.randint(0, 200),
    random.randint(0, 200),
    covering_alpha,
)
full_cover = False

if full_cover == True:
    covering_alpha = 255

brush_size = 30
cursor_radius = brush_size
cursor_color = (255, 0, 0, 70)


def set_up_chrome():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def get_realm_url():
    params = {
        "tags": "large",
    }

    base_url = "https://watabou.github.io/perilous-shores/"
    query_string = urllib.parse.urlencode(params)
    full_url = f"{base_url}?{query_string}"
    return full_url


def get_city_url():

    params = {
        # "size": 35,
        # "seed": 1512426027,
        # "citadel": 1,
        # "urban_castle": 1,
        # "plaza": 1,
        # "temple": 1,
        # "walls": 1,
        # "shantytown": 1,
        # "coast": 1,
        # "river": random.randint(1, 3),
        # "greens": 1,
        # "gates": -1,
        # "sea": 0.8
    }

    base_url = "https://watabou.github.io/city-generator/"
    query_string = urllib.parse.urlencode(params)
    full_url = f"{base_url}?{query_string}"

    return full_url


def get_map(map_type="city"):
    driver = set_up_chrome()
    if map_type == "city":
        full_url = get_city_url()
    elif map_type == "realm":
        full_url = get_realm_url()

    try:
        driver.get(full_url)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "canvas"))
        )

        time.sleep(3)
        driver.save_screenshot("city_map.png")

        print("City map saved as city_map.png")

    finally:
        driver.quit()


def voronoi_lines(points, width, height):
    lines = []
    for x in range(0, width, 10):
        for y in range(0, height, 10):
            distances = np.linalg.norm(points - np.array([x, y]), axis=1)
            closest_point_idx = np.argmin(distances)
            lines.append(
                (x, y, points[closest_point_idx][0], points[closest_point_idx][1])
            )
    return lines


def quit_everything():
    pygame.display.quit()
    pygame.quit()
    sys.exit()


pygame.init()

if need_new_map == True:
    get_map(map_type)


pil_image = Image.open("city_map.png")
width, height = pil_image.size
width, height = np.round(width * scale_factor).astype(int), np.round(
    height * scale_factor
).astype(int)
upscaled_image = pil_image.resize((width, height), Image.Resampling.LANCZOS)
data = np.flipud(np.rot90(np.array(upscaled_image)))

background = pygame.surfarray.make_surface(data)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Map Exploration Mode")

noise = np.random.randint(
    150, 200, (height // block_size, width // block_size), dtype=np.uint8
)

fog_image = Image.fromarray(noise, mode="L").convert("RGBA")
fog_image = fog_image.filter(ImageFilter.GaussianBlur(10))

fog_texture = pygame.image.fromstring(fog_image.tobytes(), fog_image.size, "RGBA")


black_layer = pygame.Surface((width, height), pygame.SRCALPHA)
black_layer.fill((50, 50, 50, covering_alpha))


num_cells = 20
points = np.array(
    [[random.randint(0, width), random.randint(0, height)] for _ in range(num_cells)]
)

lines = voronoi_lines(points, width, height)

for line in lines:
    pygame.draw.line(
        black_layer, cover_color, (line[0], line[1]), (line[2], line[3]), 1
    )
black_layer.blit(fog_texture, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)


revealed_area = pygame.Surface((width, height), pygame.SRCALPHA)
revealed_area.set_colorkey((0, 0, 0))

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_everything()
            running = False
        elif event.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_pressed()[0]:
                pygame.draw.circle(black_layer, (100, 0, 0, 0), event.pos, brush_size)

    screen.blit(background, (0, 0))

    screen.blit(black_layer, (0, 0))
    mouse_x, mouse_y = pygame.mouse.get_pos()
    cursor_surface = pygame.Surface(
        (cursor_radius * 2, cursor_radius * 2), pygame.SRCALPHA
    )
    pygame.draw.circle(
        cursor_surface, cursor_color, (cursor_radius, cursor_radius), cursor_radius
    )
    screen.blit(cursor_surface, (mouse_x - cursor_radius, mouse_y - cursor_radius))

    pygame.display.flip()

pygame.quit()
