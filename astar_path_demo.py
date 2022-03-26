from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement

xs = 1
ys = 1
xe = 3
ye = 4

# 0 : obstacle  
# 1 : free passage
map_matrix = [
    [0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0],
    ]

#create a grid from map_matrix
grid = Grid(matrix = map_matrix)

#starting & ending position
start = grid.node(xs, ys)
end = grid.node(xe,ye)

#create A* path finder
finder = AStarFinder(diagonal_movement = DiagonalMovement.always)

#use finder to find path
path, runs = finder.find_path(start, end, grid)
 
print(path)
