### FOR SINGLE ROBOT PATH PLANNING

import tuncer_globals
from tuncer_modules import * # Calculation module
import sys # For get_args
import time # For time calculations

# start = time.process_time()
# # your code here    
# print(time.process_time() - start)

# Initialize globals
tuncer_globals.init()

### Default parameters (adjustable)
num_nodes = 3 # Number of discreet nodes in a generated path, endpoints not included

### Reading map to tuncer_globals
map_name = raw_input("Enter map name: ").strip()

f = open(map_name + ".map", "r")

data = f.readlines()

wh_line = data[0].strip().split()

# Number of nodes
tuncer_globals.nodes = num_nodes
tuncer_globals.gene_length = num_nodes + 2

# Reading in map width and height
tuncer_globals.map_width = int(wh_line[0])
tuncer_globals.map_height = int(wh_line[1])

# Obstacle map
tuncer_globals.obs_map = [tuple([int(y) for y in x.split()]) for x in data[1:]]

### User input start and end coordinates
while 1:
	start = raw_input("Enter starting grid (x, y): ").strip().split()
	end = raw_input("Enter ending grid (x, y): ").strip().split()
	start = (int(start[0]), int(start[1]))
	end = (int(end[0]), int(end[1]))

	if start in tuncer_globals.obs_map or end in tuncer_globals.obs_map:
		print "Invalid start/end! Please try again."
		print
	else:
		break

### Path processing
population = [] # Population of current generation

# Generate initial population
for i in range(tuncer_globals.num_population):
	current_path = random_good_path(start, end)
	population.append((current_path, calculate_total_cost(current_path)))
	# Sort current population by total cost
	population.sort(key = lambda x: x[1])

print "***"

# Generate future generations:
for gen in range(tuncer_globals.num_gens):
	time_start = time.clock()
	# Crossing the best half of the population
	new_population = population[:tuncer_globals.num_population/2]

	len_new_pop = len(new_population)

	# Implementation Note: Crossing every pair of path, can choose a different policy
	for i in range(len_new_pop - 1):
		for j in range(i + 1, len_new_pop):
			child1, child2 = crossover(new_population[i][0], new_population[j][0])
			new_population.append([child1, calculate_total_cost(child1)])
			new_population.append([child2, calculate_total_cost(child2)])

	# Adding newly generated paths for the new population
	for i in range(tuncer_globals.num_population):
		current_path = random_good_path(start, end)
		new_population.append((current_path, calculate_total_cost(current_path)))

	# Sort current population by total cost
	new_population.sort(key = lambda x: x[1])
	population = new_population[:tuncer_globals.num_population]

	print("Generation " + str(gen) + " created after " + str(time.clock() - time_start) + "s")

# Print best candidate for generation
print "***"
print "Best candidate found after " + str(tuncer_globals.num_gens) + " generations", population[0][0]