import sys
import numpy as np
import pprint
from datasets import sudoku_easy, sudoku_medium, sudoku_hard


# I use a 1 based reference for all columns/rows (so 1-9 values vs 0-8). I can change that if needed.
# I use some terminology here. In Sudoku, traditionally, a player might write the answers in pen as they go and write 'possible answers' in pencil really tiny off to the side or on some scratch paper.
# The domain sets used by the ARC-3 algorithm is basically representation of these 'pencil marks'. So when an answer is known, it is written to the board as a 'pen mark'. The domain_sets variable is then
# basically the scratch paper where all the pencil marks are made.

class ARC3:
    board = sudoku_easy

    # This is the domain sets.
    domain_sets = np.array([[[k+1 for k in range(9)] for j in range(9)] for i in range(9)])

    # This tracks the domain_size... makes it easier/faster and we have the memory to spare
    domain_size = np.array([[9 for j in range(9)] for i in range(9)])


    def IsARC3Error(self):
        for row in range(9):
            for col in range(9):
                if (self.domain_size[row,col] <= 0):
                    return True
        return False

    # Gets domain size of a particular tile. Could be used by MRV
    def DomainSize(self, row, col):
        size = 9
        for x in range(9):
            if self.domain_sets[row-1,col-1,x] == 0:
                size-= 1
        return size

    # Reduces the domain of a tile by the value equal to the one passed in. (Used by all domain reductions)
    def ReduceDomainValue(self, row, col, val):
        if self.domain_sets[row-1,col-1,val-1] != 0:
            self.domain_sets[row-1,col-1,val-1] = 0
            self.domain_size[row-1,col-1] -= 1
            if (self.domain_size[row-1,col-1] == 1):
                self.WritePenMark(row,col)
            return True
        return False

    # Reduces the domain of an entire column by the value passed in, except for the skipped row
    def ReduceDomainByCol(self, col, val, skip):
        updated = False
        for row in range(1,10):
            if (row != skip) and (self.ReduceDomainValue(row,col,val)):
                updated = True
        return updated

    # Reduces the domain of an entire row by the value passed in, except for the skipped column
    def ReduceDomainByRow(self, row, val, skip):
        updated = False
        for col in range(1,10):
            if (col != skip) and (self.ReduceDomainValue(row,col,val)):
                updated = True
        return updated

    # Reduces the domain of an entire sector by the value passed in, except for the specified tile
    def ReduceDomainBySector(self,row,col,val):
        updated = False
        st_row_pos = 3 * ((row - 1)//3) + 1
        st_col_pos = 3 * ((col - 1)//3) + 1

        for row_index in range(st_row_pos, st_row_pos + 3):
            for col_index in range(st_col_pos, st_col_pos + 3):
           
                if (row_index != row) or (col_index != col):
                    if (self.ReduceDomainValue(row_index, col_index, val)):
                        updated = True
        return updated

    # Reduces the domain of a tile by all the values NOT EQUAL to the one passed in
    def ReduceDomainSelf(self,row,col,val):
        updated = False

        for x in range(1,10):
            if x != val:
                if (self.ReduceDomainValue(row,col,x)):
                    updated = True
        return updated

    def BasicDomainReductions(self,row, col, val):
        updatedRow = self.ReduceDomainByRow(row, val, col)
        updatedCol = self.ReduceDomainByCol(col, val, row)
        updatedSector = self.ReduceDomainBySector(row,col,val)
        updatedSelf = self.ReduceDomainSelf(row,col,val)
        return (updatedRow or updatedCol or updatedSector or updatedSelf)


    def SingletonRowCheck(self,row):
        singletonRow = np.array([0 for k in range(9)])
        for col in range(1,10):
           singletonRow += self.domain_sets[row-1,col-1]

        for index in range(1, 10):
            if (singletonRow[index-1] == index):
                for col in range(1,10):
                    if (self.board[row-1][col-1] == 0) and (self.domain_sets[row-1,col-1,index-1] != 0):
                        self.WritePenMarkWithCascade(row,col,index)

    def SingletonColCheck(self,col):
        singletonCol = np.array([0 for k in range(9)])
        for row in range(1,10):
           singletonCol += self.domain_sets[row-1,col-1]

        for index in range(1, 10):
            if (singletonCol[index-1] == index):
                for row in range(1,10):
                    if (self.board[row-1][col-1] == 0) and (self.domain_sets[row-1,col-1,index-1] != 0):
                        self.WritePenMarkWithCascade(row,col,index)

    # The following methods are just print methods for debug/ metrics
    def PrintDomain(self, row, col):
        print(self.domain_sets[row-1,col-1,:])

    def PrintDomainRow(self,row):
        for col in range(1,10):
            self.PrintDomain(row, col)

    def PrintDomainCol(self,col):
        for row in range(1,10):
            self.PrintDomain(row, col)

    def PrintDomainSector(self,start_row, start_col):
        for row in range(start_row, start_row+3):
            for col in range(start_col, start_col+3):
                pprint.pprint(self.domain_sets[row-1,col-1,:])

    # Used to make a mark on our board once we've reduced the domain of the tile to 1 (aka, found the solution to the tile)
    def WritePenMark(self, row, col):
        for x in range(0,9):
            val = self.domain_sets[row-1,col-1,x]
            if val != 0:
                self.board[row-1][col-1] = val
                return

    def WritePenMarkWithCascade(self, row, col, val):
        self.board[row-1][col-1] = val
        self.BasicDomainReductions(row,col,val)

    # This is the main ARC-3 Function. Continues to run until it can no longer reduce the domains with the implmented constraints
    def RunArc3Iteration(self):
        change = False
        for row in range(1,10):
            for col in range(1,10):
                pen_mark = self.board[row-1][col-1]
                if pen_mark != 0:
                    #We have a solution for this tile, so run all domain reductions
                    change = (self.BasicDomainReductions(row, col, pen_mark) or self.RunSingletonChecks() or self.RunTupleChecks() or self.RunPairwiseChecks())

        return change

    def RunSingletonChecks(self):
        updated = False
        for row in range(1,10):
            if (self.SingletonRowCheck(row)):
                updated = True
    
        for col in range(1,10):
            if (self.SingletonColCheck(col)):
                updated = True

        return updated


    def RunTupleChecks(self):
        updated = False

        for row in range(1,10,3):
            for col in range(1,10,3):
                updated = self.TupleCheckOnSector(row,col)
        return updated

    def RunPairwiseChecks(self):
        updated = False

        for row in range(1,10,3):
            for col in range(1,10,3):
                updated = self.PairwiseCheckOnSector(row,col)
        return updated   


    def TupleCheckOnSector(self, start_row,start_col):
        tuple_check = np.array([0 for k in range(9)])
        updated = False

        for row in range(start_row, start_row+3):
            for col in range(start_col, start_col+3):
                tuple_check += self.domain_sets[row-1,col-1]

        for index in range(1,10):
            if (tuple_check[index-1] == index*2):
                for row in range(start_row, start_row+3):
                    count = 0
                    for col in range(start_col, start_col+3):           
                        if (self.domain_sets[row-1,col-1,index-1] != 0):
                            count += 1
                    if (count == 2):
                        updated = self.ReduceDomainByRowTuple(row, index, start_col)

            
                for col in range(start_col, start_col+3):
                    count = 0
                    for row in range(start_row, start_row+3):           
                        if (self.domain_sets[row-1,col-1,index-1] != 0):
                            count += 1
                    if (count == 2):
                        updated = self.ReduceDomainByColTuple(col, index, start_row)

        return updated


    def PairwiseCheckOnSector(self, start_row, start_col):
        tuple_check = np.array([0 for k in range(9)])
        updated = False

        for row in range(start_row, start_row+3):
            for col in range(start_col, start_col+3):
                tuple_check += self.domain_sets[row-1,col-1]

        for index_1 in range(1,9):
            if (tuple_check[index_1-1] == index_1*2):
                for index_2 in range(index_1+1,10):
                    if (index_1 != index_2 and tuple_check[index_2-1] == index_2*2):
                        count = 0
                        for row in range(start_row, start_row+3):
                            for col in range(start_col, start_col+3):           
                                if (self.domain_sets[row-1,col-1,index_1-1] != 0 and self.domain_sets[row-1,col-1,index_2-1] != 0):
                                    count += 1
                        if (count == 2):
                            updated = self.ReduceDomainByPairwise(start_row, start_col, index_1, index_2)
        return updated



    def ReduceDomainByPairwise(self, start_row, start_col, index_1, index_2):
        updated = False
        for row in range(start_row, start_row+3):
            for col in range(start_col, start_col+3):
                if (self.domain_sets[row-1,col-1,index_1-1] != 0):
                    updated = self.ReduceDomainByPairwiseSelf(row, col, index_1, index_2)
        return updated


    def ReduceDomainByPairwiseSelf(self, row, col, index_1, index_2):
        updated = False
        for x in range(1,10):
            if (x != index_1 and x != index_2):
                if (self.ReduceDomainValue(row,col,x)):
                    updated = True
        return updated


    def ReduceDomainByRowTuple(self, row, val, skip_three):
        updated = False
        for col in range(1,10):
            if (col == skip_three or col == (skip_three + 1) or col == (skip_three + 2)):
                col += 3
            elif (self.ReduceDomainValue(row,col,val)):
                updated = True
        return updated


    def ReduceDomainByColTuple(self, col, val, skip_three):
        updated = False
        for row in range(1,10):
            if (row == skip_three or row == (skip_three + 1) or row == (skip_three + 2)):
                row += 3
            elif (self.ReduceDomainValue(row,col,val)):
                updated = True
        return updated


    # This loops through the domain_sets, finding all tiles that have been reduced to domain size 1, and mark them on the board if they aren't already
    def WritePenMarks(self):
        for row in range(1,10):
            for col in range(1,10):
                domain_size = self.DomainSize(row,col)
                if (domain_size == 0):
                    return False
                if (domain_size == 1):
                    self.WritePenMark(row,col)
        return True

    # This method is runs the ARC-3 function until a solution is found or no updates were made over an entire pass
    def RunArc3(self, _board):
        self.board = _board
        cont = True
        while (cont):
            arc = self.RunArc3Iteration()
            write = self.WritePenMarks()
            cont =  (arc and write)

# Should change to pass in a board, right? Until we hook everything up... I'll just leave this for testing
if (len(sys.argv) > 1):
    arc3 = ARC3()
    arg = sys.argv[1]
    if (arg == "medium"):
        arc3.RunArc3(sudoku_medium)
    elif (arg == "hard"):
        arc3.RunArc3(sudoku_hard)
    else:
        arc3.RunArc3(sudoku_easy)


