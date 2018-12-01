import datasets
from solver import misplaced_tiles
import math
import numpy as np
from timeit import Timer
from mrv import select_unassigned_variable

def getRemainingValues(row, col, box):
    # check row, col and box of the cell
    options = [i for i in range(1,10)]
    for x, y, z in zip(row, col, box):
        if x in options:
            options.remove(x)
        if y in options:
            options.remove(y)
        if z in options:
            options.remove(z)
    return options

def fillSquare(grid, x, y):
    row = grid[x][:]
    col = [(row[y]) for row in grid]
    boxX = math.floor(x / 3) * 3
    boxY = math.floor(y / 3) * 3
    box = []
    for x in grid[boxX:boxX+3]:
        for y in x[boxY:boxY+3]:
            box.append(y)
    options = getRemainingValues(row, col, box)
    return options

def generateSuccessors(grid):
    gridList = []
    for x in range(0, len(grid)):
        for y in range(len(grid[x])):
            if grid[x][y] == 0:
                gridList.append([(x, y), fillSquare(grid, x, y)])
                return gridList
    return gridList

def backtrackingSearch(grid, i):
    res = backtrack(grid, i)
    for row in res:
        print(row)
    print()
    print("Misplaced: ", misplaced_tiles(res))
    # for row in gridSol:
    #     print(row)
    return res

def backtrack(grid, depth):
    # print(depth)
    if depth == 81:
        return grid
    # successors = generateSuccessors(grid)
    successors = select_unassigned_variable(grid)
    successor = []
    if len(successors):
        successor = successors[0]
    else:
        return []
    for i in successor[1]:
        tempGrid = [row[:] for row in grid]
        tempGrid[successor[0][0]][successor[0][1]] = i
        ret = backtrack(tempGrid, depth+1)
        if len(ret):
            return ret
    return []

if __name__ == "__main__":
    i = 0
    grid = datasets.sudoku_hard
    gridSol = datasets.sudoku_easy_solution
    for row in grid:
        for cell in row:
            if cell:
                i += 1
    for row in grid:
        print(row)
    print()
    toTime = Timer(lambda: backtrackingSearch(grid, i))
    time = toTime.timeit(number=1)
    print("Time: ", round(time, 3), "s")