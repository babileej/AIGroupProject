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
    
    
# Picks a random row and swaps 2 random tiles within that row
def generate_successor(puzzle, indexPool):
    state = np.copy(puzzle)

    rowNumber           = random.randint(0, 8)
    mutableRowIndeces   = [index for index in indexPool if index[0] == rowNumber]
    index1, index2      = random.sample(mutableRowIndeces, 2)
    
    r1, c1 = index1
    r2, c2 = index2

    state[r1][c1], state[r2][c2] = state[r2][c2], state[r1][c1]

    return state


# Replaces 0's in each row keeping the row numbers non repeating
def fill_zeros(puzzle):
    for row in range(9):
        numberPool = [i for i in range(1, 10) if i not in puzzle[row]]
        random.shuffle(numberPool)

        for column in range(9):
            if(puzzle[row][column] == 0):
                puzzle[row][column] = numberPool.pop()



def sim_annealing(puzzle):
    T                = 0.5
    coolingRate      = 0.99999

    currentState     = np.array(puzzle)
    mutableIndexPool = mutable_indeces(puzzle)

    fill_zeros(currentState)

    it = 0

    while(T > 0):
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

        it += 1
        
        print("IT: %d, T:%.20f, CS: %d" % (it, T, currentScore))
    
    print(currentState)

    return currentState