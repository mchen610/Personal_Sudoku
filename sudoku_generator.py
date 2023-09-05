import math,random

"""
This was adapted from a GeeksforGeeks article "Program for Sudoku Generator" by Aarti_Rathi and Ankur Trisal
https://www.geeksforgeeks.org/program-sudoku-generator/

"""

class SudokuGenerator:
  
    def __init__(self, row_length, removed_cells):
        self.row_length = row_length
        self.removed_cells = removed_cells
        self.board = [[0 for cell in range(self.row_length)] for row in range(self.row_length)]
        self.box_length = int(math.sqrt(row_length))

 
    def get_board(self):
        return self.board


    def print_board(self):
        for row in self.board:
            print(row)


    def valid_in_row(self, row, num):
        return num not in self.board[row]

    def valid_in_col(self, col, num):
        return num not in [self.board[i][col] for i in range(len(self.board))]

    def valid_in_box(self, row_start, col_start, num):
        #self.board[row_start][col_start] is the top-left of the box
        for i in range(row_start, row_start+3):
            for j in range(col_start, col_start+3):
                if num == self.board[i][j]:
                    return False
        return True

    def is_valid(self, row, col, num):
        row_start = row//3*3 #leftmost index of the box we're in
        col_start = col//3*3 #topmost index of the box we're in 

        valid = self.valid_in_row(row, num) and self.valid_in_col(col, num) and self.valid_in_box(row_start, col_start, num) and self.board[row][col] == 0
        return valid
        

    def fill_box(self, row_start, col_start):
        digits = [i for i in range(1,self.row_length+1)] 
        for i in range(row_start, row_start + self.box_length):
            for j in range(col_start, col_start + self.box_length):
                self.board[i][j] = random.choice(digits)
                digits.remove(self.board[i][j])

    '''
    Fills the three boxes along the main diagonal of the board
    These are the boxes which start at (0,0), (3,3), and (6,6)

	Parameters: None
	Return: None
    '''
    def fill_diagonal(self):
        for i in range(0,self.row_length-self.box_length+1,self.box_length): 
            self.fill_box(i,i)

    '''
    DO NOT CHANGE
    Provided for students
    Fills the remaining cells of the board
    Should be called after the diagonal boxes have been filled
	
	Parameters:
	row, col specify the coordinates of the first empty (0) cell

	Return:
	boolean (whether or not we could solve the board)
    '''
    def fill_remaining(self, row, col):
        if (col >= self.row_length and row < self.row_length - 1): #if the column were on is too big and the row is in range, add 1 to row and set column to 0
            row += 1
            col = 0
        if row >= self.row_length and col >= self.row_length: #if the row is too big and column is too big, return true
            return True
        if row < self.box_length:
            if col < self.box_length: #if row and col are in range then set column to box_length
                col = self.box_length
        elif row < self.row_length - self.box_length: #if row is to the left of the rightmost box
            if col == int(row // self.box_length * self.box_length): #if column is at the left of the box, change one box to the right
                col += self.box_length
        else:
            if col == self.row_length - self.box_length:
                row += 1
                col = 0
                if row >= self.row_length:
                    return True
        
        for num in range(1, self.row_length + 1):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.fill_remaining(row, col + 1):
                    return True
                self.board[row][col] = 0
        return False

    '''
    DO NOT CHANGE
    Provided for students
    Constructs a solution by calling fill_diagonal and fill_remaining

	Parameters: None
	Return: None
    '''
    def fill_values(self):
        self.fill_diagonal()
        self.fill_remaining(0, self.box_length)

    '''
    Removes the appropriate number of cells from the board
    This is done by setting some values to 0
    Should be called after the entire solution has been constructed
    i.e. after fill_values has been called
    
    NOTE: Be careful not to 'remove' the same cell multiple times
    i.e. if a cell is already 0, it cannot be removed again

	Parameters: None
	Return: None
    '''


    '''
    def remove_cells(self):
        count = 0
        while(count < self.removed_cells):
            row = random.randint(0,self.row_length-1)
            col = random.randint(0,self.row_length-1)
            
            if(self.board[row][col] != 0):
                count+=1
                self.board[row][col] = 0
            
            if(count%10 == 0):
                self.print_board()
                print()
    '''

    
    def remove_cells(self):
        count = 0
        removed_cell_list = [] #[(row,col)]
        while(count < self.removed_cells):
            row = random.randint(0,self.row_length-1)
            col = random.randint(0,self.row_length-1)

            if((row,col) not in removed_cell_list):
                count+=1
                self.board[row][col] = 0
                removed_cell_list.append((row,col))
    

'''
DO NOT CHANGE
Provided for students
Given a number of rows and number of cells to remove, this function:
1. creates a SudokuGenerator
2. fills its values and saves this as the solved state
3. removes the appropriate number of cells
4. returns the representative 2D Python Lists of the board and solution

Parameters:
size is the number of rows/columns of the board (9 for this project)
removed is the number of cells to clear (set to 0)

Return: list[list] (a 2D Python list to represent the board)
'''

def generate_sudoku(size, removed):
    sudoku = SudokuGenerator(size, removed)
    sudoku.fill_values()
    board = sudoku.get_board()
    sudoku.remove_cells()
    board = sudoku.get_board()
    return board




