from board import Board, Cell
import pygame   
from pygamecentering import Button, Text
from colors import *

#DIFFICULTIES
EASY = 30
MEDIUM = 40
HARD = 55

#BOARD DIMENSIONS
NORMAL = 9  

screen_length = 440

#use in get_hoveredCell, changes mouse pos in terms of board indices, no cell if past row_length (9) or below 0
def board_pos(sudoku: Board):
    mouse_pos = list(pygame.mouse.get_pos())
    #mouse_pos = [x,y] -> mouse_pos = [col,row]
    for i in range(2):
        mouse_pos[i]-=sudoku.cell_len #get position of mouse relative to board
        mouse_pos[i]//=sudoku.cell_len #get indices of mouse relative to board
        mouse_pos[i] = int(mouse_pos[i])
    #mouse_pos = [col,row]
    return mouse_pos

def get_hoveredCell(sudoku: Board): #get hovered cell
    mouse_pos = board_pos(sudoku)
    if not (8 >= mouse_pos[0] >= 0 and 8 >= mouse_pos[1] >= 0): #if not in board
        return None
    else: #draw outline if in board
        currentCell = sudoku.board[mouse_pos[1]][mouse_pos[0]]
        return currentCell

def is_digit(event: pygame.event.Event): #0 = False
    try:
        return int(event.unicode)
    except:
        return 0

def is_arrow(event: pygame.event.Event):
    return event.type == pygame.KEYDOWN and (event.key == pygame.K_LEFT or event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_RIGHT)

def arrow_move(sudoku: Board, prevCell: Cell, event: pygame.event.Event) -> Cell:
    if prevCell == None:
        return sudoku.board[sudoku.row_len//2][sudoku.row_len//2]
    else:
        row, col = prevCell.row, prevCell.col

    #teleports to opposite end if out of bounds
    if event.key == pygame.K_UP:
        return sudoku.board[row-1][col]
    elif event.key == pygame.K_DOWN:
        return sudoku.board[(row+1)%sudoku.row_len][col]
    elif event.key == pygame.K_LEFT:
        return sudoku.board[row][col-1]
    elif event.key == pygame.K_RIGHT:
        return sudoku.board[row][(col+1)%sudoku.row_len]
    return prevCell



def left_click(event: pygame.event.Event):
    return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1

def valid_Cell(cell: Cell, sudoku: Board):
    return sudoku.sudoku_gen.is_valid(cell.row, cell.col, cell.value)

def main():
    screen_center = screen_length//2
    screen_color = BLACK

    pygame.init()
    screen = pygame.display.set_mode(((screen_length,screen_length)))
    screen.fill(screen_color)
    pygame.display.set_caption("Sudoku")
    clock = pygame.time.Clock()

    

    #difficulty buttons settings
    diff_dim = (screen_length*0.6, screen_length*0.15) #(w,h)
    
    welcome_center = (screen_center,screen_length//10)
    welcome_text = Text(screen, 'PLAY SUDOKU', WHITE, welcome_center, 70)
    welcome_y = screen_length//10+int(screen_length*0.075)
    welcome_text.draw()

    easy_button = Button(screen, 'EASY', GREEN, center = (screen_center, screen_center//2+welcome_y//2), dim = diff_dim)
    easy_button.draw()
    
    medium_button = Button(screen, 'MEDIUM', YELLOW, center = (screen_center, screen_center+welcome_y//2), dim = diff_dim)
    medium_button.draw()

    hard_button = Button(screen, 'HARD', RED, center = (screen_center, screen_center+screen_center//2+welcome_y//2), dim = diff_dim)
    hard_button.draw()

   
    

    #get difficulty
    DIFFICULTY = 0
    while DIFFICULTY == 0:
        if easy_button.is_clicked():
                DIFFICULTY = EASY
        elif medium_button.is_clicked():
            DIFFICULTY = MEDIUM
        elif hard_button.is_clicked(): 
            DIFFICULTY = HARD

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        clock.tick(60)
        pygame.display.update()

    screen.fill(BLACK)
    screen = pygame.display.set_mode((screen_length, screen_length*1.2))
    pygame.display.update()
    
    #generate sudoku and display it
    SIZE = NORMAL
    sudoku = Board(screen, SIZE, DIFFICULTY)

    

    button_dim = (screen_length*0.28, screen_length*0.08)
    button_y = screen_length
    left_button_x = int((screen_length-button_dim[0])/3.5)
    right_button_x = screen_length - left_button_x

    #left
    retry_button = Button(screen, 'RETRY', GREEN, (left_button_x, button_y), button_dim)
    retry_button.draw()

    #middle
    menu_button = Button(screen, 'MENU', BLUE, (screen_length//2, button_y), button_dim)
    menu_button.draw()

    #right
    exit_button = Button(screen, 'EXIT', RED, (right_button_x, button_y), button_dim)
    exit_button.draw()

    #bottom
    submit_button = Button(screen, 'SUBMIT', WHITE, (screen_length//2, int(button_y+button_dim[1]*1.5)), (button_dim[0]*1.3,button_dim[1]*1.1), thickness = 2) 
    submit_button.draw()

    prevCell = None
    currentCell = None
    locked = False #leaving the current cell
    valid_entries = set()
    bad_entries = set()
    sketched_entries = set()
    #while empty cells exist (sketched counts as empty)
    
    
    while submit_button.clicked == False:
        if retry_button.is_clicked():
                if locked:
                    sudoku.remove_border(prevCell)
                for cell in valid_entries:
                    cell.erase_value()
                    cell.set_value(0)
                for cell in bad_entries:
                    cell.erase_value()
                    cell.set_value(0)
                for cell in sketched_entries:
                    cell.erase_value(sketched = True)
                    cell.set_sketched_value(0)
                valid_entries.clear()
                bad_entries.clear()
                sketched_entries.clear()

        if menu_button.is_clicked():
            main()

        if exit_button.is_clicked():
            pygame.quit()
            exit()

        if submit_button.is_clicked() and (len(valid_entries) > 0 or len(bad_entries) > 0):
            break  

        for event in pygame.event.get():    

            if is_arrow(event):
                currentCell = arrow_move(sudoku, prevCell, event)  

            elif event.type == pygame.KEYDOWN and event.key != pygame.K_RETURN:
                pygame.event.post(event)

            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION and not locked:
                currentCell = get_hoveredCell(sudoku)


            if currentCell != prevCell or not locked: #switched cells or unlocked from same cell
                
                if prevCell != None: #draw over outline -> redraw cell border -> redraw box
                    sudoku.remove_border(prevCell)

                if currentCell != None: #draw current cell if in board
                    currentCell.draw_outline()
                    locked = False

                pygame.display.update()
            
            #user has left is_clicked an editable cell
            if currentCell != None and not currentCell.generated: 
                if left_click(event):
                    currentCell.draw_outline(RED)
                    locked = True
                    pygame.display.update()
                typing = event.type != pygame.MOUSEMOTION #can input if mouse not moving
                while typing:
                    
                    for new_event in pygame.event.get():
                        if retry_button.is_clicked() or menu_button.is_clicked() or exit_button.is_clicked() or submit_button.is_clicked():
                            typing = False
                            break                           
                            
                        #print(pygame.event.event_name(new_event.type))
                        #move cell if any of these happen no matter what, even if locked
                        elif new_event.type == pygame.MOUSEBUTTONDOWN or (new_event.type == pygame.KEYDOWN and new_event.key == pygame.K_ESCAPE or is_arrow(new_event)) or (not locked and new_event.type == pygame.MOUSEMOTION): #exit typing
                            typing = False
                            locked = False
                            if not (new_event.type == pygame.KEYDOWN and new_event.key == pygame.K_ESCAPE):
                                pygame.event.post(new_event)
                                break
                                
                        elif new_event.type == pygame.KEYDOWN:   
                            #print(pygame.event.event_name(new_event.type), digit_input, new_event.unicode)
                            
                            if currentCell.value == 0: 
                                digit_input = is_digit(new_event)       

                                #add or replace sketched value
                                if digit_input > 0 and digit_input != currentCell.sketched_value: #has input a number and cell has no value
                                    #replace and sketch if sketch is different or doesnt exist
                                    currentCell.rewrite_sketch(digit_input)
                                    sketched_entries.add(currentCell)

                                #promote sketch to real value
                                elif currentCell.sketched_value > 0 and (new_event.key == pygame.K_RETURN or digit_input == currentCell.sketched_value): 
                                    sketched_entries.remove(currentCell)
                                    currentCell.promote_sketch() #sets cell value and draws 
                                
                                    valid = valid_Cell(currentCell, sudoku) 
                                    if valid:    
                                        valid_entries.add(currentCell)
                                    else:
                                        bad_entries.add(currentCell)

                                    sudoku.transfer_value(currentCell) #sets cell value into original 2d value board

                                                 
                            if new_event.key == pygame.K_BACKSPACE: #erase value

                                #erase real value
                                if currentCell.value > 0:
                                    valid = currentCell in valid_entries
                                    if valid:
                                        valid_entries.remove(currentCell)
                                    else:
                                        bad_entries.remove(currentCell)
                                    
                                    currentCell.erase_value(sketched = False)
                                    currentCell.set_value(0)
                                    sudoku.transfer_value(currentCell)
                                
                                #erase sketched
                                elif currentCell.sketched_value > 0:
                                    currentCell.erase_value(sketched = True)
                                    currentCell.set_sketched_value(0)
                                    sketched_entries.remove(currentCell)
                           
                        if new_event.type == pygame.QUIT:
                            pygame.quit()
                            exit()
                        pygame.display.update()


            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            prevCell = currentCell
        pygame.display.update()
    
    '''GAME OVER''' 

    if locked:
        sudoku.remove_border(prevCell)

    win = len(valid_entries) == DIFFICULTY
    
    font = pygame.font.Font(None, screen_length//12)

    for cell in bad_entries:
        cell.draw_outline(RED)

    sudoku.draw_boxes(GRAY)

    if win:
        text = font.render('GAME WIN', True, GREEN)
        
        
    else:
        text = font.render('GAME OVER', True, RED)
        

    pygame.display.update()

    end_board = True
    while end_board:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and (event.key != pygame.K_LCTRL and event.key != pygame.K_z and event.key != pygame.K_LSHIFT) or event.type == pygame.MOUSEBUTTONDOWN:
                end_board = False
            
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    #draw 'game win' or 'game lose'
    screen.fill(screen_color)
    screen.blit(text, text.get_rect(center = (screen_center,screen_center)))

    menu_button.move((2*screen_center/3, screen_center*1.5))
    menu_button.draw()

    exit_button.move((4*screen_center/3, screen_center*1.5))
    exit_button.draw()

    pygame.display.update()

    while True:
        if menu_button.is_clicked():
            main()
        
        if exit_button.is_clicked():
            pygame.quit()
            exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()        


if __name__ == '__main__':
    main()
