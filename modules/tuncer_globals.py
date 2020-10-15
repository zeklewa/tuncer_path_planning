# Globals initialized to be 0s

def init():
    # Default parameters for algorithm, adjust here
    global length_alpha, obstacle_alpha, friend_alpha
    global num_gens, num_population

    length_alpha = 1 # Path length cost multiplier
    obstacle_alpha = 10 # Single-robot collision (with obstacle map) cost multiplier
    friend_alpha = 0 # Multi-robot collision cost multiplier

    num_gens = 3 # Number of child generations
    num_population = 10 # Population of a single generation

    # Parameters to be read in from file
    global map_width, map_height
    global obs_map
    global nodes
    global gene_length

    map_width = 0
    map_height = 0
    obs_map = []
    start = (0, 0)
    end = (0, 0)
    nodes = 0