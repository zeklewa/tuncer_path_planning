import pygame

map_name = raw_input("Enter map name: ").strip()

f = open(map_name + ".map", "w+")

width = int(input("Enter width of map: "))
height = int(input("Enter height of map: "))

f.write("%d %d\n" % (width, height))

print "Currently making map of dimensions: %dx%d" % (width, height)

# Max dim (width/height): 800 pixels
grid_size = 800/max(height, width)

display_width = grid_size*width
display_height = grid_size*height

pygame.init()
screen = pygame.display.set_mode((display_width, display_height))
screen.fill((255, 255, 255))

font = pygame.font.Font('freesansbold.ttf', 20*5/width)

done = False

def convert_grid(mouse_coords):
	return (mouse_coords[0]/grid_size, mouse_coords[1]/grid_size)

while not done:
	# Draw grid
	for i in range(width):
		pygame.draw.line(screen, (0, 0, 0), [i*grid_size, 0], [i*grid_size, display_height])
	for j in range(height):
		pygame.draw.line(screen, (0, 0, 0), [0, j*grid_size], [display_width, j*grid_size])

	# Rendering text over grids
	for i in range(width):
		for j in range(height):
			text = font.render("(" + str(i) + ", " + str(j) + ")", True, (0, 0, 0))
			screen.blit(text, (i*grid_size, j*grid_size))

	# Event handling
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN and pygame.K_SPACE:
			pygame.image.save(screen, map_name + ".jpeg")
			done = True
		if event.type == pygame.MOUSEBUTTONDOWN:
			prev_coords = pygame.mouse.get_pos()
		if event.type == pygame.MOUSEBUTTONUP:
			new_coords = pygame.mouse.get_pos()
			prev_grid = convert_grid(prev_coords)
			new_grid = convert_grid(new_coords)
			width_grid = (new_grid[0] - prev_grid[0] + 1)
			height_grid = (new_grid[1] - prev_grid[1] + 1)

			for j in range(height_grid):
				for i in range(width_grid):
					f.write(str(prev_grid[0] + i) + " " + str(prev_grid[1] + j) + "\n")

			pygame.draw.rect(screen, (0, 0, 0), [prev_grid[0]*grid_size, prev_grid[1]*grid_size, width_grid*grid_size, height_grid*grid_size])
	pygame.display.flip()

print "Map successfully created!"