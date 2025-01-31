#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 13:31:04 2025

@author: lukasgartmair
"""
import pygame
import sys

def quit_everything():
    pygame.display.quit()
    pygame.quit()
    sys.exit()

background_color = (0,0,0)

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((800, 600))

# Create a black layer
black_layer = pygame.Surface((800, 600))
black_layer.fill((0, 0, 0))  # Completely black layer

# Main game loop
running = True
revealing = False  # Variable to track whether the mouse is clicked
brush_radius = 30  # Size of the reveal area

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_everything()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            revealing = True
        elif event.type == pygame.MOUSEBUTTONUP:
            revealing = False

    # If the mouse is pressed, reveal the black layer
    if revealing:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        pygame.draw.circle(black_layer, background_color, (mouse_x, mouse_y), brush_radius)
    
    # Fill the screen with the background color (or a background image)
    screen.fill((255, 255, 255))  # White background (can be changed to any color/image)

    # Draw the black layer (over the background)
    screen.blit(black_layer, (0, 0))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
