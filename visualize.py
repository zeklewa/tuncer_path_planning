### At the moment, the visualizer only works on two-robot path planning ###

import tuncer_globals
from tuncer_modules import * # Calculation module
import pygame

# Reading in map
map_name = raw_input("Enter map name: ").strip()
f = open(map_name + ".map", "r")
data = f.readlines()
wh_line = data[0].strip().split()
width = int(wh_line[0])
height = int(wh_line[1])
f.close()

print width, height

# Reading in path
path_name = raw_input("Enter path name: ").strip()
f = open(map_name + "_" + path_name + ".path", "r")
data = f.readlines()
f.close()

paths = []
for line in data:
    path = []
    line = line.replace('(', '').replace(')', '').replace(',', '').split()
    # Reconstructing path
    i = 0
    for x in line:
        if i % 2 == 1:
            path.append((int(prev), int(x)))
        prev = x
        i += 1
    
    paths.append(path)

print paths

# Calculate grid size and window size
grid_size = 800/max(height, width)

display_width = grid_size*width
display_height = grid_size*height

screen = pygame.display.set_mode((display_width, display_height))
background_image = pygame.image.load(map_name + ".jpeg")
animationTimer = pygame.time.Clock()

# Single path animation
if len(paths) == 1:
    p = paths[0]
    c = estimate_path_time(p, 2, 0, 0.01)

    for i in range(len(c)):
        x, y = c[i][1]

        x *= grid_size
        y *= grid_size

        x += grid_size/2
        y += grid_size/2

        x = int(x)
        y = int(y)

        # Draw object
        screen.blit(background_image, (0, 0))
        pygame.draw.circle(screen, (255, 0, 0), (x, y), int(grid_size/5))
        pygame.draw.circle(screen, (0, 255, 0), (x, y), int(grid_size/5))

        animationTimer.tick(40)
        pygame.display.update()
        i += 1

# Two-robot path animation
elif len(paths) == 2:
    p1 = paths[0]
    p2 = paths[1]

    c1 = estimate_path_time(p1, 2, 0, 0.01)
    c2 = estimate_path_time(p2, 2, 0, 0.01)

    max_i = max(len(c1), len(c2))

    for i in range(max_i):
        if i >= len(c1):
            x1, y1 = c1[-1][1]
            x2, y2 = c2[i][1]
        elif i >= len(c2):
            x1, y1 = c1[i][1]
            x2, y2 = c2[-1][1]
        else:
            x1, y1 = c1[i][1]
            x2, y2 = c2[i][1]

        x1 *= grid_size
        y1 *= grid_size

        x2 *= grid_size
        y2 *= grid_size

        x1 += grid_size/2
        y1 += grid_size/2

        x2 += grid_size/2
        y2 += grid_size/2

        x1 = int(x1)
        y1 = int(y1)

        x2 = int(x2)
        y2 = int(y2)

        # Draw object
        screen.blit(background_image, (0, 0))
        pygame.draw.circle(screen, (255, 0, 0), (x1, y1), int(grid_size/5))
        pygame.draw.circle(screen, (0, 255, 0), (x2, y2), int(grid_size/5))

        animationTimer.tick(40)
        pygame.display.update()
        i += 1