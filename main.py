import pygame
from pygame.locals import*

#Make some constant 
BOARD_WIDTH = 3   
BOARD_HEIGHT = 3
CELL_SIZE = 100
WINDOW_WIDTH = 480    
WINDOW_HEIGHT = 480
INF = int(1e9)

#Make some constant color
WHITE =         (255, 255, 255)
DARKTURQUOISE = (  3,  54,  73)
PINK = (252, 159, 252)
BG_COLOR = DARKTURQUOISE

CELL_COLOR = PINK
TEXT_COLOR = WHITE
BORDER_COLOR = WHITE

OG_FONT_SIZE = 20
MSG_COLOR = WHITE

BLANK = 10
PLAYER_O = 11 # bot
PLAYER_X = 21  #human

CONTINUE_GAME = 10
TIE = 20

X_MARGIN = int((WINDOW_WIDTH - CELL_SIZE*BOARD_WIDTH - (BOARD_WIDTH - 1))/2)
Y_MARGIN = int((WINDOW_HEIGHT - CELL_SIZE*BOARD_HEIGHT - (BOARD_HEIGHT - 1))/2)


# UI
# create surface and rect obj for text
def create_text(text,color,background_color,top,left):
    text_surf = OG_FONT.render(text,True,color,background_color)
    text_rect = text_surf.get_rect()
    # config text_rect to top,left
    text_rect.topleft = (top,left)
    return (text_surf,text_rect)

def get_left_top(row,col):
    left = X_MARGIN+row*CELL_SIZE + (row -1)
    top = Y_MARGIN+col*CELL_SIZE + (col -1)
    return (left,top)

def sym2str(symbol):
    if symbol == PLAYER_X:
        return 'X'
    elif symbol == PLAYER_O:
        return 'O'    

# draw cell and symbol (X/0) 
def draw_cell(row,col,symbol):

    left, top = get_left_top(row,col)
    pygame.draw.rect(WIN_SURF,CELL_COLOR,(left,top,CELL_SIZE,CELL_SIZE))
    text_surf = OG_FONT.render(sym2str(symbol),True,TEXT_COLOR)
    text_rect = text_surf.get_rect()
    text_rect.center = left+int(CELL_SIZE/2), top+int(CELL_SIZE/2)
    WIN_SURF.blit(text_surf,text_rect)

def draw_board(board,msg):
    WIN_SURF.fill(BG_COLOR)
    if msg:
        text_surf,text_rect = create_text(msg,MSG_COLOR,BG_COLOR,5,7)
        WIN_SURF.blit(text_surf,text_rect)
    for row in range(3):
        for col in range(3):
            if board[row*3+col] != BLANK:  # if cell is checked
                draw_cell(row,col,board[row*3+col])

    # get left, top of board
    left,top = get_left_top(0,0)
    width = CELL_SIZE*BOARD_WIDTH
    height = CELL_SIZE*BOARD_HEIGHT
    # draw border of board
    pygame.draw.rect(WIN_SURF,BORDER_COLOR,(left,top,width,height),4)

    WIN_SURF.blit(AI_SURF,AI_RECT)


def getSpotClicked(x,y):
    for row in range(3):
        for col in range(3):
            left,top = get_left_top(row,col)
            cell_rect = pygame.Rect(left,top,CELL_SIZE,CELL_SIZE)
            if cell_rect.collidepoint(x,y):
                return (row,col)
    return None            


def check_legal(coords,board):
    x,y = coords
    step = 3*x+y
    return board[step] == BLANK

def update_board(board,pos,player):
    board[pos] = player
def available_step(board):
    remain_cell = []
    for i in range(9):
        if board[i]== BLANK:
            remain_cell.append(i)
    return remain_cell        

def update_state(board,step,depth):
    new_board = list(board)
    new_board[step] = PLAYER_X if depth %2 else PLAYER_O
    return new_board
     

# minimax algorithm

def check_win(board):
    def check_tie():
        return sum(board)%10 == 9
    def check_horizontal(player):
        for i in [0,3,6]:
            if sum(board[i:i+3]) == 3* player:
                return player
    def check_vertical(player):
        for i in range(3):
            if sum(board[i: :3])== 3* player:
                return player            
    def check_diagonal(player):
        if (sum(board[0::4]) == 3* player) or (sum(board[2:7:2])== 3* player):
            return player

    for player in [PLAYER_X,PLAYER_O]:
        if any([check_horizontal(player), check_vertical(player), check_diagonal(player)]):
            return player

    if check_tie():
        return TIE
    else:
        return CONTINUE_GAME    
        
def minimax(board,depth,isMaximizing):
    if check_win(board) == PLAYER_O:
        return 1
    elif check_win(board) == PLAYER_X:
        return -1
    elif check_win(board) == TIE:
        return 0

    if isMaximizing:
        bestScore = -INF  
        for step in range(9):
            if board[step] == BLANK:
                board[step]=PLAYER_O
                score = minimax(board,depth+1,False)
                board[step] = BLANK
                if score>bestScore:
                    bestScore = score
        return bestScore
    else:
        bestScore = INF   
        for step in range(9):
            if board[step] == BLANK:
                board[step]=PLAYER_X
                score = minimax(board,depth+1,True)
                board[step] = BLANK
                if score<bestScore:
                    bestScore = score
        return bestScore



def AI_move(board):
    global choice
    bestScore = -INF
    bestMove = 0
    for step in range(9):
        if board[step] == BLANK:
            board[step]= PLAYER_O
            score = minimax(board,0,False)
            board[step] = BLANK
            if score>bestScore:
                bestScore = score
                bestMove = step
    choice = bestMove

def main():
    global WIN_SURF,OG_FONT, AI_SURF,AI_RECT
    pygame.init()
    WIN_SURF = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
    pygame.display.set_caption("TIC-TAC-TOE-AI-LAB-2")
    OG_FONT = pygame.font.Font("freesansbold.ttf", OG_FONT_SIZE)
    AI_SURF, AI_RECT = create_text('vs AI', TEXT_COLOR,CELL_COLOR, WINDOW_WIDTH-120,WINDOW_HEIGHT-60)

    #make board
    board = [BLANK]*9  # create 1D Array 9 element with value = 10 represent for empty cell
    game_over = False
    msg = "Welcome to Tic tac toe AI"

    draw_board(board,msg)
    pygame.display.update()
    run = True
    while run:
        coords = None
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                coords = getSpotClicked(event.pos[0],event.pos[1])
                # if click into button vs AI
                if not coords and AI_RECT.collidepoint(event.pos):
                    board = [BLANK]*9
                    game_over = False
                    msg = "Welcome to Tic Tac Toe AI"
                    draw_board(board,msg)
                    pygame.display.update()
            elif event.type == pygame.QUIT:
                run = False
        
        if coords and check_legal(coords,board) and not game_over:
            x,y = coords
            x_player_pos = x*3+y
            update_board(board,x_player_pos,PLAYER_X)
            draw_board(board,msg)
            pygame.display.update()
            if len(available_step(board))==0:
                game_over = True
                continue
            AI_move(board)
            update_board(board,choice,PLAYER_O)

        result = check_win(board)
        game_over = (result != CONTINUE_GAME) 
        if result == PLAYER_X:
            msg = "You win!. Congratulate <3"
        elif result == PLAYER_O:
            msg = "AI win!, you lose :(("  
        elif result == TIE:
            msg = "Tie!!"
        draw_board(board,msg)
        pygame.display.update()    

    pygame.quit()

if __name__ == "__main__":
    main()
