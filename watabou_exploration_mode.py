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
from PIL import Image
import urllib
import random

def set_up_chrome():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def get_city_map():
    driver = set_up_chrome()
    params = {
    "size": 35,
    # "seed": 1512426027,
    # "citadel": 1,
    # "urban_castle": 1,
    # "plaza": 1,
    # "temple": 1,
    # "walls": 1,
    # "shantytown": 1,
    # "coast": 1,
    "river": random.randint(1,3),
    # "greens": 1,
    # "gates": -1,
    # "sea": 0.8
}
    
    base_url = "https://watabou.github.io/city-generator/"
    query_string = urllib.parse.urlencode(params)
    full_url = f"{base_url}?{query_string}"

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


def quit_everything():
    pygame.display.quit()
    pygame.quit()
    sys.exit()


pygame.init()

need_new_map = False
if need_new_map == True:
    get_city_map()

scale_factor = 2
pil_image = Image.open("city_map.png")
width, height = pil_image.size
width, height = width * scale_factor, height * scale_factor
upscaled_image = pil_image.resize((width, height), Image.Resampling.LANCZOS)
data = np.flipud(np.rot90(np.array(upscaled_image)))
background = pygame.surfarray.make_surface(data)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("City Map Viewer")

black_layer = pygame.Surface((width, height), pygame.SRCALPHA)
black_layer.fill((0, 0, 0, 255))
black_layer.set_alpha(255)

brush_size = 25
cursor_radius = brush_size
cursor_color = (0, 0, 255, 70)


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
