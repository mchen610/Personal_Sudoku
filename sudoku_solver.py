from sudoku_generator import *
from board import Board
import pygame as pg

def print_board(board):
    for row in board:
        print(row)

class SudokuSolver(Board):
    def __init__(self,  screen: pg.Surface, box_len: int, difficulty: int):
        super.__init__(screen, box_len, difficulty)
        rows = generate_sudoku(9, 30)
        print_board(rows)
        cols = [[row[col] for row in row_board] for col in range(len(row_board))]
        boxes = []
        for box_row in range(0,9,3):
            for box_col in range(0,9,3):
                box = []
                for row in range(box_row,box_row+3):
                    for col in range(box_col,box_col+3):
                        box.append(row_board[row][col])
                boxes.append(box)


if __name__ == '__main__':
    pg.init()
    screen = pg.display.set_mode((440,440))


    digits = [x for x in range(1,10)]
    row_board = generate_sudoku(9, 30)
    print_board(row_board)
    col_board = [[row[col] for row in row_board] for col in range(len(row_board))]
    box_board = []
    for box_row in range(0,9,3):
        for box_col in range(0,9,3):
            box = []
            for row in range(box_row,box_row+3):
                for col in range(box_col,box_col+3):
                    box.append(row_board[row][col])
            box_board.append(box)

    print(box_board)

    empty_cells = []
    for row in range(len(row_board)):
        for col in range(len(row_board[0])):
            if row_board[row][col] == 0:
                empty_cells.append([row, col, row//3*3+col//3, row_board[row][col]])

    #print(empty_cells)

    new_board = Board(screen, 9, 30, row_board)
    new_board.draw()
    pg.display.update()

    staying = True
    while staying:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                staying = False
    
    one_popped = True
    while one_popped:
        one_popped = False
        print(empty_cells)
        index = 0
        while index < len(empty_cells):
            cell = empty_cells[index]
            print(cell, row_board[cell[0]], col_board[cell[1]], box_board[cell[2]])
            popped = False
            possibilities = (set(digits) - set(row_board[cell[0]])) & (set(digits) - set(col_board[cell[1]])) & (set(digits) - set(box_board[cell[2]]))
            for x in possibilities:
                if x not in row_board[cell[0]]:
                    if len(set(row_board[cell[0]])) == len(row_board[cell[0]]): #1 empty cell in row
                        print('row')
                        row_board[cell[0]][cell[1]] = x
                        col_board[cell[1]][cell[0]] = x
                        box_board[cell[2]][cell[0]%3+cell[1]%3]
                        empty_cells.pop(index)
                        popped = True
                        break

                    elif x not in col_board[cell[1]]:
                        if len(set(col_board[cell[1]])) == len(col_board[cell[1]]): #1 empty cell in col
                            print('col')
                            row_board[cell[0]][cell[1]] = x
                            col_board[cell[1]][cell[0]] = x
                            box_board[cell[2]][cell[0]%3+cell[1]%3]
                            empty_cells.pop(index)
                            popped = True
                            break

                        elif x not in box_board[cell[2]]:
                            if len(set(box_board[cell[2]])) == len(row_board[cell[2]]): #1 empty cell in box
                                print('box')
                                row_board[cell[0]][cell[1]] = x
                                col_board[cell[1]][cell[0]] = x
                                box_board[cell[2]][cell[0]%3+cell[1]%3]
                                empty_cells.pop(index)
                                popped = True
                                break

                if row_board[cell[0]]
            if not popped:
                index+=1
            elif one_popped == False:
                one_popped = True

                
            


    
    newer_board = Board(screen, 9, 30, row_board)
    newer_board.draw()
    pg.display.update()

    staying = True
    while staying:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                staying = False


    

