import numpy as np
import pprint
from datasets import sudoku_easy as board

domain_sets = np.array([[[k+1 for k in xrange(9)] for j in xrange(9)] for i in xrange(9)])

#pprint.pprint(domain_sets)


def DomainSize(row, col):
    size = 9;
    for x in range(9):
        if domain_sets[row-1,col-1,x] == 0:
            size-= 1
    return size


def ReduceDomainValue(row, col, val):
    if domain_sets[row-1,col-1,val-1] != 0:
        domain_sets[row-1,col-1,val-1] = 0
        return True
    return False


def ReduceDomainByCol(col, val, skip):
    updated = False
    for row in range(1,10):
        if (row != skip) and (ReduceDomainValue(row,col,val)):
            updated = True
    return updated


def ReduceDomainByRow(row, val, skip):
    updated = False
    for col in range(1,10):
        if (col != skip) and (ReduceDomainValue(row,col,val)):
            updated = True
    return updated


def ReduceDomainBySector(row,col,val):
    updated = False
    st_row_pos = 3 * ((row - 1)/3) + 1
    st_col_pos = 3 * ((col - 1)/3) + 1

    for row_index in range(st_row_pos, st_row_pos + 3):
        for col_index in range(st_col_pos, st_col_pos + 3):
           
            if (row_index != row) or (col_index != col):
                if (ReduceDomainValue(row_index, col_index, val)):
                    updated = True
    return updated

def ReduceDomainSelf(row,col,val):
    updated = False

    for x in range(1,10):
        if x != val:
            if (ReduceDomainValue(row,col,x)):
                updated = True
    return updated

def PrintDomain(row, col):
    print(domain_sets[row-1,col-1,:])

def PrintDomainRow(row):
    for col in range(1,10):
        PrintDomain(row, col)

def PrintDomainCol(col):
    for row in range(1,10):
        PrintDomain(row, col)

def WritePenMark(row, col):
    for x in range(0,9):
        val = domain_sets[row-1,col-1,x]
        if val != 0:
            board[row-1][col-1] = val
            return


def RunArc3Iteration():
    change = False
    for row in range(1,10):
        for col in range(1,10):
            pen_mark = board[row-1][col-1]
            if pen_mark != 0:

                #We have a solution for this tile, so run all domain reductions
                if (ReduceDomainByCol(col, pen_mark, row)):
                    change = True
                if (ReduceDomainByRow(row, pen_mark, col)):
                    change = True
                if (ReduceDomainBySector(row, col, pen_mark)):
                    change = True
                if (ReduceDomainSelf(row, col, pen_mark)):
                    change = True
    return change

def WritePenMarks():
    for row in range(1,10):
        for col in range(1,10):
            domain_size = DomainSize(row,col)
            if (domain_size == 0):
                return False
            if (domain_size == 1):
                WritePenMark(row,col)
    return True


def RunArc3():
    cont = True
    while (cont):
        if RunArc3Iteration():
            WritePenMarks()
        else:
            cont = False


pprint.pprint(board)
RunArc3()
print('\n')
pprint.pprint(board)
RunArc3()
print('\n')
pprint.pprint(board)
