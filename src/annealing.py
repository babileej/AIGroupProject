import random
import math
import numpy as np

from solver import misplaced_tiles


# Returns a list of sets representing modifiable indeces in a given starting puzzle
def mutable_indeces(grid):
    indeces = []

    for(r, c), tile in np.ndenumerate(grid):
        if(tile == 0): indeces.append((r,c))

    return indeces

# Given the box number (0-8) returns its offsets in the grid
def boxOffsets(boxNumber):
    xoffset = (3 * boxNumber) % 9
    yoffset = 3 * int(boxNumber / 3)

    return xoffset, yoffset
    
# Picks a random box and swaps 2 random tiles within that box
def generate_successor(puzzle, indexPool):
    state = np.copy(puzzle)

    boxNumber         = random.randint(0, 8)
    xoffset, yoffset  = boxOffsets(boxNumber)
    mutableBoxIndeces = []

    # Get the list of mutable indeces within the box
    for row in range(yoffset, yoffset+3):
        for column in range(xoffset, xoffset+3):
            if((row, column) in indexPool): mutableBoxIndeces.append((row, column))

    
    # Randomly pick 2 tiles to swap
    index1, index2  = random.sample(mutableBoxIndeces, 2)
    
    r1, c1 = index1
    r2, c2 = index2

    # Swap
    state[r1][c1], state[r2][c2] = state[r2][c2], state[r1][c1]

    return state


# Replaces 0's in each box keeping the box numbers non repeating
def fill_zeros(puzzle):

    for box in range(9):
        xoffset, yoffset = boxOffsets(box)

        # Represent the box as a list in order to generate possible unique numbers to fill
        listBox = (puzzle[yoffset: yoffset + 3, xoffset:xoffset + 3]).ravel()
        numberPool = [i for i in range(1, 10) if i not in listBox]
        random.shuffle(numberPool)

        # Fill the tiles
        for row in range(yoffset, yoffset+3):
            for column in range(xoffset, xoffset+3):
                if(puzzle[row][column] == 0): puzzle[row][column] = numberPool.pop()

 

def sim_annealing(puzzle, T=0.5, Tmin=0.1, coolingRate=0.999999, verbose=False):
    currentState     = np.array(puzzle)
    mutableIndexPool = mutable_indeces(puzzle)

    fill_zeros(currentState)

    it = 0

    while(T > Tmin):
        nextState       = generate_successor(currentState, mutableIndexPool)

        currentScore    = misplaced_tiles(currentState)
        nextScore       = misplaced_tiles(nextState)
        
        # Stop if solved
        if(currentScore == 0): break

        dE = nextScore - currentScore

        if(dE < 0):
            currentState = nextState
        else:
            exp = math.e ** (-dE / T)
            if(random.uniform(0, 1) < exp):
                currentState = nextState
            
        T *= coolingRate

        if(verbose):
            it += 1
            if(it % 20000 == 0): print("IT: %d, T:%.20f, CS: %d\n" % (it, T, currentScore))
                

    return currentState
