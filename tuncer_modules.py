import random
import tuncer_globals

# Ray-tracing to calculate grids through which the line p0-p1 passes
def raytrace(p0, p1):
	x0, y0 = p0
	x1, y1 = p1
	res = []
	dx = abs(x1 - x0)
	dy = abs(y1 - y0)
	x = x0
	y = y0
	n = 1 + dx + dy
	x_inc = -1
	y_inc = -1
	if x1 > x0:
		x_inc = 1
	if y1 > y0:
		y_inc = 1
	error = dx - dy
	dx *= 2
	dy *= 2

	while n > 0:
		res.append((x, y))
		if (error > 0):
			x += x_inc
			error -= dy
		else:
			y += y_inc
			error += dx
		n -= 1

	return res

# Generate random path
def gen_path(start, end):
    path = [start]
    i = 0
    while i != tuncer_globals.nodes:
        node = (random.randrange(tuncer_globals.map_width), random.randrange(tuncer_globals.map_height))
        if not node in tuncer_globals.obs_map:
            path.append(node)
            i += 1

    path.append(end)
    return path

def crossover(path1, path2):
    cross_point = random.randrange(tuncer_globals.gene_length)
    p1 = path1[:cross_point] + path2[cross_point:]
    p2 = path2[:cross_point] + path1[cross_point:]

    return (p1, p2)

def set_trace_path(path):
    set_traced = set([])

    for i in range(len(path) - 1):
		set_segment = raytrace(path[i], path[i + 1])
		set_traced |= set(set_segment)
    
    return set_traced

def set_collision_path(path):
    return set_trace_path(path) & set(tuncer_globals.obs_map)

def random_good_path(start, end):
    while True: # Only try a maximum of 50 times for possible candidate (adjustable)
        path = gen_path(start, end)
        if len(set_collision_path(path)) == 0: return path
    return []

def calculate_obstacle_cost(path):
    return tuncer_globals.obstacle_alpha*len(set_collision_path(path))

def calculate_length_cost(path):
    # Simply path length in Cartesian coordinates
    total = 0
    for i in range(len(path) - 1):
        x0, y0 = path[i]
        x1, y1 = path[i + 1]
        total += ((x1 - x0)**2 + (y1 - y0)**2)**0.5
    return total*tuncer_globals.length_alpha

def calculate_friend_cost(path):
    # TODO
    return 0

def calculate_total_cost(path):
    return calculate_obstacle_cost(path) + calculate_length_cost(path) + calculate_friend_cost(path)