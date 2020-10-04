# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 16:54:50 2020

@author: Gabriel Boscoli

Interface gráfica do trabalho 1 de Inteligência Artificial
"""

import pygame

# Define some colors
COLORS = {'M': (128, 128, 128), 'P': (191, 191, 191), 'R': (217, 217, 217)}
BLACK = (0, 0, 0)

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 20
HEIGHT = 20

# This sets the margin between each cell
MARGIN = 1

# grid deve ser quadrada
def setGrid(grid):
    global GRID
    GRID = grid
            
def desenhaGrid():
    linhas = len(GRID)
    colunas = len(GRID[0])
    # Draw the grid
    for row in range(linhas):
        for column in range(colunas):
            color = COLORS.get(GRID[row][column])
            pygame.draw.rect(SCREEN,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
            
def inicializaInterface(linhas, colunas, title):
    # Initialize pygame
    pygame.init()
    # Set the HEIGHT and WIDTH of the screen
    window_size = [linhas * WIDTH + (linhas + 1) * MARGIN, colunas * HEIGHT + (colunas + 1) * MARGIN]
    global SCREEN
    SCREEN = pygame.display.set_mode(window_size)
    # Set the screen background
    SCREEN.fill(BLACK)
    # Set title of screen
    pygame.display.set_caption(title)

def fechaInterface():
    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()