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

# Same function, variable num_nodes
# Generate random path
def gen_path_var(start, end, num_nodes):
    path = [start]
    i = 0
    while i != num_nodes:
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

# Generate random good path without collisions
def random_good_path(start, end):
    while True: # Only try a maximum of 50 times for possible candidate (adjustable)
        path = gen_path(start, end)
        if len(set_collision_path(path)) == 0: return path
    return []

# Same function, variable num_nodes
def random_good_path_var(start, end, num_nodes):
    while True: # Only try a maximum of 50 times for possible candidate (adjustable)
        path = gen_path_var(start, end, num_nodes)
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

# Multi-robot path planning - 2 robot's coordinates estimation
def estimate_path_time(path, speed, turn_speed, delta_t):
    # Description: function takes in the arguments:
    # path: list of turning coordinates, same as previous "path" variable
    # speed: constant speed at which the robot moves on a straight line
    # turn_speed: constant turning speed of the robot when transitioning between straight trajectories
    # delta_t: minimal time step at which coordinates calculations are performed
    
    est_coords = []

    # Calculations:
    # Total time taken for each straight-line trajectory:
    line_ts = []
    for i in range(len(path) - 1):
        x0, y0 = path[i]
        x1, y1 = path[i + 1]
        line_ts.append((((x1 - x0)**2 + (y1 - y0)**2)**0.5)/speed)
    
    # Total time taken for each turn:
    turn_ts = []
    for i in range(len(path) - 1):
        # TODO
        turn_ts.append(0)

    # Estimate robots' coordinates
    coords = []
    cum_line_ts = []
    cum_line_pre_ts = []
    for i in range(len(line_ts)):
        cum_line_ts.append(sum(line_ts[:i+1]))
        cum_line_pre_ts.append(sum(line_ts[:i]))

    t = 0
    current_trajectory = 0 

    while t < cum_line_ts[-1]:
        start_x, start_y = path[current_trajectory]
        end_x, end_y = path[current_trajectory + 1]

        if (line_ts[current_trajectory] == 0): p_f = 0
        else: p_f = (t - cum_line_pre_ts[current_trajectory])/line_ts[current_trajectory]
        r_x = (end_x - start_x)*p_f + start_x
        r_y = (end_y - start_y)*p_f + start_y

        est_coords.append((t, (r_x, r_y), current_trajectory))
        if t >= cum_line_ts[current_trajectory]:
            current_trajectory += 1
        t += delta_t

    return est_coords

# Detect collision between two robots
def detect_collision(path1, path2):
    # Naive implementation, will change
    # Collision returns true if the difference between x and y coordinates are too small

    # =================== THIS PART NEEDS TO BE MODIFIED TO ACCOUNT FOR VARIABLE ACCELERATION =====================
    coords1 = estimate_path_time(path1, 2, 0, 0.01)
    coords2 = estimate_path_time(path2, 2, 0, 0.01)
    # =============================================================================================================

    min_length_c = min(len(coords1), len(coords2))
    max_length_c = max(len(coords1), len(coords2))

    for i in range(max_length_c):
        # Stop conditions
        if i >= min_length_c:
            if len(coords1) > len(coords2):
                x1, y1 = coords1[i][1]
                x2, y2 = coords2[-1][1]
                tr1 = coords1[i][2]
                tr2 = coords2[-1][2]
            else:
                x1, y1 = coords1[-1][1]
                x2, y2 = coords2[i][1]
                tr1 = coords1[-1][2]
                tr2 = coords2[i][2]
        else:  
            x1, y1 = coords1[i][1]
            x2, y2 = coords2[i][1]
            tr1 = coords1[i][2]
            tr2 = coords2[i][2]

        if abs(x2 - x1) < 0.05 and abs(y2 - y1) < 0.05:
            if i >= len(coords1):
                collision_t = coords2[i][0]
            else:
                collision_t = coords1[i][0]
            # print "Collision predicted at t = %f and (x, y) = (%f, %f)" % (collision_t, x1, y1)
            return (tr1, tr2)

    # print "No collisions predicted"
    return (-1, -1)

# num_nodes variable denotes number of extra nodes inserted to resolve collision
def resolve_collision(path1, path2, tr1, tr2, num_nodes):
    fpath1 = []
    fpath2 = []
    i = 0

    # Generate random good inserted nodes for both paths:
    # Maximum of 1000 iterations
    for i in range(1000):
        print "Iteration %d of generating solution (%d inserted nodes)..." % (i, num_nodes)
        extra_path1 = random_good_path_var(path1[tr1], path1[tr1 + 1], num_nodes)
        extra_path2 = random_good_path_var(path2[tr2], path2[tr2 + 1], num_nodes)
        fpath1 = path1[:tr1] + extra_path1[:] + path1[tr1 + 1:]
        fpath2 = path2[:tr2] + extra_path2[:] + path2[tr2 + 1:]
        if detect_collision(fpath1, fpath2) == (-1, -1):
            print "*******************"
            print "One solution found:"
            print fpath1
            print fpath2
            print "*******************"
            return (fpath1, fpath2)
        i += 1
    
    return ([], [])