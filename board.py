import pygame
import math
import sudoku_generator
from colors import *

class Cell:
    def __init__(self, value: int, row: int, col: int, screen: pygame.Surface, width = 40, screen_color = BLACK):
        self.value = value
        self.generated = value > 0 #computer generated or not
        self.sketched_value = 0

        self.row = row
        self.col = col
        self.screen = screen
        self.width = width
        self.screen_color = screen_color

        self.left = (col+1)*width #actual visual location in the display
        self.right = self.left + self.width
        self.top = (row+1)*width #actual visual location in the display
        self.bot = self.top + self.width
        self.rect = pygame.Rect(self.left, self.top, width, width) #(x,y, width, height) #ACTUAL VISUAL SUDOKU CELL
        
    def set_value(self, value):
        self.value = value

    def set_sketched_value(self, value):
        self.sketched_value = value
    
    def draw_border(self, COLOR = GRAY): #original border
       pygame.draw.rect(self.screen, COLOR, self.rect, 1) 
    
    def draw_outline(self, COLOR = LIGHT_BLUE): #thicker outline border
        pygame.draw.rect(self.screen, COLOR, self.rect.inflate(-2+self.screen.get_width()%2,-2+self.screen.get_height()%2), 2) #screen_length%2 makes it stay even with the cell sizes
        
    def draw_value(self, sketched = False, erasing = False):
        if sketched:
            font_size = int(self.width*3/5)
            value = self.sketched_value
            COLOR = GRAY

        else:
            font_size = int(self.width*9/10)
            value = self.value
            
            if self.generated:
                COLOR = WHITE
            else:
                COLOR = LIGHT_BLUE

        font = pygame.font.Font(None, font_size)

        if value > 0: #draw digit if not 0 or draw to erase
            cell_digit = font.render(str(value), True, COLOR) #actual Surface object containing the digit (1,2,3,4.. etc)
            if value == 5: #5 is too high for some reason
                cell_digit_square = cell_digit.get_rect(center=(self.rect.centerx,self.rect.centery+1))
            else:
                cell_digit_square = cell_digit.get_rect(center=self.rect.center) #new square the size of the text, NOT THE ACTUAL SUDOKU CELL, JUST EXISTS TO CENTER THE DIGIT INSIDE THE CELL OR ERASE
            
            if erasing:
                return cell_digit_square
            else:
                self.screen.blit(cell_digit, cell_digit_square) #places text starting from topleft of square, ends up in center
        
    def erase_value(self, sketched = False): 
        cell_digit_square = self.draw_value(sketched, erasing = True)
        pygame.draw.rect(self.screen, self.screen_color, cell_digit_square)

    #erase sketched value -> set value -> draw value -> set sketched value to 0 
    def promote_sketch(self):
        self.erase_value(sketched = True)
        self.set_value(self.sketched_value)
        self.draw_value()
        self.set_sketched_value(0)

    def rewrite_sketch(self, digit_input):
        if self.sketched_value != digit_input:
            if self.sketched_value != 0:
                self.erase_value(sketched = True)
            self.set_sketched_value(digit_input)
            self.draw_value(sketched = True)

        
    def draw(self):
        self.draw_value()
        self.draw_border()

#THE INITIAL DRAWING OF THE BOARD IS INSIDE THE CONSTRUCTOR, CHANGE IF NEEDED
class Board:
    def __init__(self, screen: pygame.Surface, row_len: int, difficulty: int, board = None):
        self.sudoku_gen = sudoku_generator.SudokuGenerator(row_len, difficulty)

        if board != None:
            self.sudoku_gen.board = board
        else:
            self.sudoku_gen.fill_values()
            self.sudoku_gen.remove_cells()
            
        self.board = [row.copy() for row in self.sudoku_gen.get_board()] #will turn into 2d list of Cell objects
        
        self.screen = screen

        self.row_len = row_len #cells in row
        self.box_len = int(math.sqrt(self.row_len)) #cells in box
        self.cell_len = self.screen.get_width()/(self.row_len+2) #drawing length

        #create and draw Cell objects
        self.boxes = [] #[pygame.Rect] list of boxes
        for row in range(self.row_len):
            for col in range(self.row_len):
                self.board[row][col] = Cell(self.board[row][col], row, col, self.screen, width = self.cell_len)
                self.board[row][col].draw()

                #outlines of boxes
                if(row%self.box_len == 0 and col%self.box_len == 0):
                    self.boxes.append(pygame.Rect(self.board[row][col].left,self.board[row][col].top, self.cell_len*self.box_len, self.cell_len*self.box_len))

        #self.original_board = [row.copy() for row in self.board]

        #self.boxes is a 1d list of boxes, ordered row by row, 1st box is topleft box, last box is bottomright
        #draw box outlines over cell drawings
        for box in self.boxes:
            pygame.draw.rect(self.screen, WHITE, box, 1)

    #draw the 3x3 box borders
    def draw_boxes(self, COLOR = WHITE, width = 1):
        for box in self.boxes:
            pygame.draw.rect(self.screen, COLOR, box, width)

    def draw(self):
      for row in range(self.row_len):
            for col in range(self.row_len):
                self.board[row][col].draw()
      self.draw_boxes()

    #boxes[] IS A 1D ARRAY, THIS IS HOW TO GET THE BOX USING ITS 2D INDEX
    def get_box(self, cell: Cell): 
        #get 2d box index
        row = cell.row
        col = cell.col
        row//=self.box_len
        col//=self.box_len

        return self.boxes[row*self.box_len+col] #self.boxes[] index from theoretical 2d box index topleft box, if box_len = 3, self.boxes[4] would have row=1, col=1, 1*3+1 = 4
      
    def transfer_value(self, cell: Cell):
        self.sudoku_gen.board[cell.row][cell.col] = cell.value

    def remove_border(self, cell: Cell):
        cell.draw_outline(cell.screen_color)
        cell.draw_border()
        pygame.draw.rect(self.screen, WHITE, self.get_box(cell), 1)

       
  





        
        