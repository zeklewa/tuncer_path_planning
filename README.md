**Overview**
This repository contains the implementation of Tuncer's single-robot path planning algorithm, as well as that of an adapted multi-robot path planning algorithm.

The original paper can be found here: [https://dl.acm.org/doi/10.1016/j.compeleceng.2012.06.016](https://dl.acm.org/doi/10.1016/j.compeleceng.2012.06.016)

**Program usage:**
To create an obstacle map, launch:

    >>> python map_creator.py

Rectangular obstacles can be directly created on the generated map by clicking and dragging the mouse.
After creating the obstacle map, either run `python single.py` for single-robot path planning, or `python double.py` for 2-robot path planning on the map.

**Example:**
Running `single.py` and providing the corresponding inputs:

    >>> python single.py
    Enter map name: spec
    Enter starting grid (x, y): 0 0
    Enter ending grid (x, y): 9 9

Produces the following output:

    ***
    Generation 0 created after 0.069748s
    Generation 1 created after 0.118467s
    Generation 2 created after 0.064918s
    ***
    Best candidate found after 3 generations [(0, 0), (2, 6), (7, 7), (9, 8), (9, 9)]

**Notes:**
Sample maps (small, large_sparse and spec) are included in this repository, on which I primarily tested these algorithms. Results from sample experiments will be posted to this README once more data is obtained.

Also, in the future, this repository will be updated with finer visual displays (possibly a Gazebo simulation) and further tweaks for the multi-robot path planning algorithm.
