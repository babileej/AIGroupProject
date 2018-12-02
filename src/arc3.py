import time
import sys
import numpy as np
import pprint
import solver
from datasets import sudoku_easy, sudoku_medium, sudoku_hard


# I use a 1 based reference for all columns/rows (so 1-9 values vs 0-8). I can change that if needed.
# I use some terminology here. In Sudoku, traditionally, a player might write the answers in pen as they go and write 'possible answers' in pencil really tiny off to the side or on some scratch paper.
# The domain sets used by the ARC-3 algorithm is basically representation of these 'pencil marks'. So when an answer is known, it is written to the board as a 'pen mark'. The domain_sets variable is then
# basically the scratch paper where all the pencil marks are made.

# TO IMPLEMENT:
    ## Refactor Existing code
        ## Move basic domain reduction methods to a single group  method
        ## Add flags in loop for each method return
        ## Change main loop to:
            ## Do basic dmoain reduce loop (w/ a write call whenver domain reduced to 1)
            ## Check for 'Singletons' (And write when found)

    ## Add some changes to increase efficiency
        ## Each successful write called from the 'Singletons' check will trigger domain reduction for that tile
        ## Writes called from the Domain Reduction in this way will not cascade further (to prevent stack issues)

    ## Add a domain_size array, to track size better. Would require a write everytime we reduce domain, BUT would increase read efficiency a ton. Besides, each domain reduction does a read so...





# Should change to pass in a board, right? Until we hook everything up... I'll just leave this for testing
if (len(sys.argv) < 2):
    board = sudoku_easy
else:
    arg = sys.argv[1]
    if (arg == "medium"):
        board = sudoku_medium
    elif (arg == "hard"):
        board = sudoku_hard
    else:
        board = sudoku_easy


# This is the domain sets.
domain_sets = np.array([[[k+1 for k in range(9)] for j in range(9)] for i in range(9)])

# This tracks the domain_size... makes it easier/faster and we have the memory to spare
domain_size = np.array([[9 for j in xrange(9)] for i in xrange(9)])


def IsARC3Error():
    for row in range(9):
        for col in range(9):
            if (domain_size[row,col] <= 0):
                return True
    return False

# Gets domain size of a particular tile. Could be used by MRV
def DomainSize(row, col):
    size = 9
    for x in range(9):
        if domain_sets[row-1,col-1,x] == 0:
            size-= 1
    return size

# Reduces the domain of a tile by the value equal to the one passed in. (Used by all domain reductions)
def ReduceDomainValue(row, col, val):
    if domain_sets[row-1,col-1,val-1] != 0:
        domain_sets[row-1,col-1,val-1] = 0
        domain_size[row-1,col-1] -= 1
        if (domain_size[row-1,col-1] == 1):
            WritePenMark(row,col)
        return True
    return False

# Reduces the domain of an entire column by the value passed in, except for the skipped row
def ReduceDomainByCol(col, val, skip):
    updated = False
    for row in range(1,10):
        if (row != skip) and (ReduceDomainValue(row,col,val)):
            updated = True
    return updated

# Reduces the domain of an entire row by the value passed in, except for the skipped column
def ReduceDomainByRow(row, val, skip):
    updated = False
    for col in range(1,10):
        if (col != skip) and (ReduceDomainValue(row,col,val)):
            updated = True
    return updated

# Reduces the domain of an entire sector by the value passed in, except for the specified tile
def ReduceDomainBySector(row,col,val):
    updated = False
    st_row_pos = 3 * ((row - 1)//3) + 1
    st_col_pos = 3 * ((col - 1)//3) + 1

    for row_index in range(st_row_pos, st_row_pos + 3):
        for col_index in range(st_col_pos, st_col_pos + 3):
           
            if (row_index != row) or (col_index != col):
                if (ReduceDomainValue(row_index, col_index, val)):
                    updated = True
    return updated

# Reduces the domain of a tile by all the values NOT EQUAL to the one passed in
def ReduceDomainSelf(row,col,val):
    updated = False

    for x in range(1,10):
        if x != val:
            if (ReduceDomainValue(row,col,x)):
                updated = True
    return updated

def BasicDomainReductions(row, col, val):
    updatedRow = ReduceDomainByRow(row, val, col)
    updatedCol = ReduceDomainByCol(col, val, row)
    updatedSector = ReduceDomainBySector(row,col,val)
    updatedSelf = ReduceDomainSelf(row,col,val)
    return (updatedRow or updatedCol or updatedSector or updatedSelf)


def SingletonRowCheck(row):
    singletonRow = np.array([0 for k in xrange(9)])
    for col in range(1,10):
       singletonRow += domain_sets[row-1,col-1]

    for index in range(1, 10):
        if (singletonRow[index-1] == index):
            for col in range(1,10):
                if (board[row-1][col-1] == 0) and (domain_sets[row-1,col-1,index-1] != 0):
                    WritePenMarkWithCascade(row,col,index)

def SingletonColCheck(col):
    singletonCol = np.array([0 for k in xrange(9)])
    for row in range(1,10):
       singletonCol += domain_sets[row-1,col-1]

    for index in range(1, 10):
        if (singletonCol[index-1] == index):
            for row in range(1,10):
                if (board[row-1][col-1] == 0) and (domain_sets[row-1,col-1,index-1] != 0):
                    WritePenMarkWithCascade(row,col,index)

# The following methods are just print methods for debug/ metrics
def PrintDomain(row, col):
    print(domain_sets[row-1,col-1,:])

def PrintDomainRow(row):
    for col in range(1,10):
        PrintDomain(row, col)

def PrintDomainCol(col):
    for row in range(1,10):
        PrintDomain(row, col)

def PrintDomainSector(start_row, start_col):
    for row in range(start_row, start_row+3):
        for col in range(start_col, start_col+3):
            pprint.pprint(domain_sets[row-1,col-1,:])

# Used to make a mark on our board once we've reduced the domain of the tile to 1 (aka, found the solution to the tile)
def WritePenMark(row, col):
    for x in range(0,9):
        val = domain_sets[row-1,col-1,x]
        if val != 0:
            board[row-1][col-1] = val
            return

def WritePenMarkWithCascade(row, col, val):
    board[row-1][col-1] = val
    BasicDomainReductions(row,col,val)

# This is the main ARC-3 Function. Continues to run until it can no longer reduce the domains with the implmented constraints
def RunArc3Iteration():
    change = False
    for row in range(1,10):
        for col in range(1,10):
            pen_mark = board[row-1][col-1]
            if pen_mark != 0:
                #We have a solution for this tile, so run all domain reductions
                change = (BasicDomainReductions(row, col, pen_mark) or RunSingletonChecks() or RunTupleChecks() or RunPairwiseChecks())

    return change

def RunSingletonChecks():
    updated = False
    for row in range(1,10):
        if (SingletonRowCheck(row)):
            updated = True
    
    for col in range(1,10):
        if (SingletonColCheck(col)):
            updated = True

    return updated


def RunTupleChecks():
    updated = False

    for row in range(1,10,3):
        for col in range(1,10,3):
            updated = TupleCheckOnSector(row,col)
    return updated

def RunPairwiseChecks():
    updated = False

    for row in range(1,10,3):
        for col in range(1,10,3):
            updated = PairwiseCheckOnSector(row,col)
    return updated   


def TupleCheckOnSector(start_row,start_col):
    tuple_check = np.array([0 for k in xrange(9)])
    updated = False

    for row in range(start_row, start_row+3):
        for col in range(start_col, start_col+3):
            tuple_check += domain_sets[row-1,col-1]

    for index in range(1,10):
        if (tuple_check[index-1] == index*2):
            for row in range(start_row, start_row+3):
                count = 0
                for col in range(start_col, start_col+3):           
                    if (domain_sets[row-1,col-1,index-1] != 0):
                        count += 1
                if (count == 2):
                    updated = ReduceDomainByRowTuple(row, index, start_col)

            
            for col in range(start_col, start_col+3):
                count = 0
                for row in range(start_row, start_row+3):           
                    if (domain_sets[row-1,col-1,index-1] != 0):
                        count += 1
                if (count == 2):
                    updated = ReduceDomainByColTuple(col, index, start_row)

    return updated


def PairwiseCheckOnSector(start_row, start_col):
    tuple_check = np.array([0 for k in xrange(9)])
    updated = False

    for row in range(start_row, start_row+3):
        for col in range(start_col, start_col+3):
            tuple_check += domain_sets[row-1,col-1]

    for index_1 in range(1,9):
        if (tuple_check[index_1-1] == index_1*2):
            for index_2 in range(index_1+1,10):
                if (index_1 != index_2 and tuple_check[index_2-1] == index_2*2):
                    count = 0
                    for row in range(start_row, start_row+3):
                        for col in range(start_col, start_col+3):           
                            if (domain_sets[row-1,col-1,index_1-1] != 0 and domain_sets[row-1,col-1,index_2-1] != 0):
                                count += 1
                    if (count == 2):
                        updated = ReduceDomainByPairwise(start_row, start_col, index_1, index_2)
    return updated



def ReduceDomainByPairwise(start_row, start_col, index_1, index_2):
    updated = False
    for row in range(start_row, start_row+3):
        for col in range(start_col, start_col+3):
            if (domain_sets[row-1,col-1,index_1-1] != 0):
                updated = ReduceDomainByPairwiseSelf(row,col, index_1, index_2)
    return updated


def ReduceDomainByPairwiseSelf(row, col, index_1, index_2):
    updated = False
    for x in range(1,10):
        if (x != index_1 and x != index_2):
            if (ReduceDomainValue(row,col,x)):
                updated = True
    return updated


def ReduceDomainByRowTuple(row, val, skip_three):
    updated = False
    for col in range(1,10):
        if (col == skip_three or col == (skip_three + 1) or col == (skip_three + 2)):
            col += 3
        elif (ReduceDomainValue(row,col,val)):
            updated = True
    return updated


def ReduceDomainByColTuple(col, val, skip_three):
    updated = False
    for row in range(1,10):
        if (row == skip_three or row == (skip_three + 1) or row == (skip_three + 2)):
            row += 3
        elif (ReduceDomainValue(row,col,val)):
            updated = True
    return updated


# This loops through the domain_sets, finding all tiles that have been reduced to domain size 1, and mark them on the board if they aren't already
def WritePenMarks():
    for row in range(1,10):
        for col in range(1,10):
            domain_size = DomainSize(row,col)
            if (domain_size == 0):
                return False
            if (domain_size == 1):
                WritePenMark(row,col)
    return True

# This method is runs the ARC-3 function until a solution is found or no updates were made over an entire pass
def RunArc3():
    cont = True
    while (cont):
        arc = RunArc3Iteration()
        write = WritePenMarks()
        cont =  (arc and write)

# Execution Code. Should probably put in a main method...
RunArc3()


