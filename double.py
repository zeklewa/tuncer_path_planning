### FOR 2-ROBOT PATH PLANNING

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
    start1 = raw_input("Enter starting grid of robot1 (x, y): ").strip().split()
    end1 = raw_input("Enter ending grid of robot1 (x, y): ").strip().split()
    start2 = raw_input("Enter starting grid of robot2 (x, y): ").strip().split()
    end2 = raw_input("Enter ending grid of robot2 (x, y): ").strip().split()

    start1 = (int(start1[0]), int(start1[1]))
    end1 = (int(end1[0]), int(end1[1]))
    start2 = (int(start2[0]), int(start2[1]))
    end2 = (int(end2[0]), int(end2[1]))

    if start1 in tuncer_globals.obs_map or end1 in tuncer_globals.obs_map:
        print "Invalid start/end for robot1! Please try again."
        print
    else:
        if start2 in tuncer_globals.obs_map or end2 in tuncer_globals.obs_map:
            print "Invalid start/end for robot2! Please try again."
            print
        else:
            break

print 

### Path processing for robot1 (master)
population = [] # Population of current generation

# Generate initial population
for i in range(tuncer_globals.num_population):
	current_path = random_good_path(start1, end1)
	population.append((current_path, calculate_total_cost(current_path)))
	# Sort current population by total cost
	population.sort(key = lambda x: x[1])

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
		current_path = random_good_path(start1, end1)
		new_population.append((current_path, calculate_total_cost(current_path)))

	# Sort current population by total cost
	new_population.sort(key = lambda x: x[1])
	population = new_population[:tuncer_globals.num_population]

# Finished path planning for robot1
path1 = population[0]

###############################

### Path processing for robot2
population = [] # Population of current generation
new_population = []

# Generate initial population
for i in range(tuncer_globals.num_population):
    current_path = random_good_path(start2, end2)
    population.append((current_path, calculate_total_cost(current_path)))
    # Sort current population by total cost
    population.sort(key = lambda x: x[1])

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
        current_path = random_good_path(start2, end2)
        new_population.append((current_path, calculate_total_cost(current_path)))

    # Sort current population by total cost
    new_population.sort(key = lambda x: x[1])
    population = new_population[:tuncer_globals.num_population]

path2 = population[0]

# Multi robot coordination part
# Prediction: Estimate robot1's location in time and anticipate collision by altering robot2's path

print "***"
print "Initial paths generated:"
print "Robot1's path: ", path1[0]
print "Robot2's path: ", path2[0]
print "***"

col_tr1, col_tr2 = detect_collision(path1[0], path2[0])

print col_tr1, col_tr2

if (col_tr1 != -1):
    print "Collision detected!"
    print "Resolving collision, generating possible solutions:"
    for num_nodes in range(1, 10):
        print "### Attempting to insert %d nodes" % num_nodes
        fpath1, fpath2 = resolve_collision(path1[0], path2[0], col_tr1, col_tr2, num_nodes)
        if (fpath1, fpath2) != ([], []): break
print "***"
print "Final generated paths: "
print "Robot1: ", fpath1
print "Robot2: ", fpath2
print "***"

# Exporting path to .path file
path_name = raw_input("Save subpath name: ")

f.close()
f = open(map_name + "_" + path_name + ".path", "w")
for x in fpath1:
    f.write("(%d %d) " % (x[0], x[1])),
f.write("\n")
for x in fpath2:
    f.write("(%d %d) " % (x[0], x[1])),
f.write("\n")
f.close()