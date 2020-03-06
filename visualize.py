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
f = open(path_name + ".path", "r")
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

p1 = paths[0]
p2 = paths[1]

c1 = estimate_path_time(p1, 2, 0, 0.01)
c2 = estimate_path_time(p2, 2, 0, 0.01)

# Calculate grid size and window size
grid_size = 800/max(height, width)

display_width = grid_size*width
display_height = grid_size*height

screen = pygame.display.set_mode((display_width, display_height))
background_image = pygame.image.load(map_name + ".jpeg")
animationTimer = pygame.time.Clock()

done = False

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
    x1 += grid_size/2
    y1 += grid_size/2

    x2 *= grid_size
    y2 *= grid_size
    x2 += grid_size/2
    y2 += grid_size/2

    # Draw object
    screen.blit(background_image, (0, 0))
    pygame.draw.ellipse(screen, (255, 0, 0), (x1, y1, 10, 10))
    pygame.draw.ellipse(screen, (0, 255, 0), (x2, y2, 10, 10))

    animationTimer.tick(40)
    pygame.display.update()
    i += 1