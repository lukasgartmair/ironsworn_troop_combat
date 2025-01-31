import numpy as np
import pygame
from perlin_noise import PerlinNoise

def generate_terrain(width=100, height=100, scale=100, octaves=4):
    noise = PerlinNoise(octaves=octaves, seed=np.random.randint(0, 1000))
    terrain = np.zeros((height, width))
    
    for y in range(height):
        for x in range(width):
            terrain[y][x] = noise([x / (scale * 0.5), y / (scale * 0.5)])    
    return terrain

def render_terrain(terrain, screen, width, height):
    max_val = np.max(terrain)
    min_val = np.min(terrain)
    
    for y in range(height):
        for x in range(width):
            value = (terrain[y][x] - min_val) / (max_val - min_val)  # Normalize to 0-1
            color = (value * 255, value * 255, value * 255)  # Grayscale
            scale_factor = screen.get_width() / width  # Adjusts based on screen size
            pygame.draw.rect(screen, color, (x * scale_factor, y * scale_factor, scale_factor, scale_factor))


def main():
    width, height = 400, 400
    scale, octaves = 30, 6
    terrain = generate_terrain(width, height, scale, octaves)
    
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("2D Perlin Noise Terrain")
    render_terrain(terrain, screen, width, height)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()
