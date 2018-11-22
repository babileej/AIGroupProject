import numpy

def valid_sequence(row):
    return sum(row) == sum(set(row))

# Checks all rows, columns and separate boxes
def solved(grid):
    npgrid = numpy.array(grid)

    for row in npgrid:
        if(not valid_sequence(row)): return False
    
    for i in range(9):
        # Get a column as a list
        column = npgrid[:, i]
        
        if(not valid_sequence(column)): return False

    for c in range(0, 9, 3):
        for r in range(0, 9, 3):
            # Get a box as a list
            box = npgrid[c:c+3, r:r+3]
            if(not valid_sequence(box.ravel())): return False

    return True