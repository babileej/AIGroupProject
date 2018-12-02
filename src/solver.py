import numpy

# Returns the number of misplaced tiles in a given row
def misplaced_tiles_row(row):
    rowset = set(row)
    zeros = 1 if 0 in rowset else 0

    return len(row) - len(rowset) + zeros
    
# Returns total misplaced tiles in a gived grid
def misplaced_tiles(grid):
    total = 0

    npgrid = numpy.array(grid)

    for row in npgrid:
        total += misplaced_tiles_row(row)

    for i in range(9):
        # Get a column as a list
        column = npgrid[:, i]
        total += misplaced_tiles_row(column)

    for c in range(0, 9, 3):
        for r in range(0, 9, 3):
            # Get a box as a list
            box = npgrid[c:c+3, r:r+3]
            total += misplaced_tiles_row(box.ravel())
    
    return total
    
