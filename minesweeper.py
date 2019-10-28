# TO DO
#area none bomb
#if board[tilex][tiley] == 0:
#    get random 3 locations
#repeat
import sys, pygame, random
from pygame.locals import *

WINDOWWIDTH = 640
WINDOWHEIGHT = 480
FPS = 30
BLANK = None

BOARDWIDTH = 10
BOARDHEIGHT = 10
MARGIN = 1
TILESIZE = 20
NUMBOMB = 20
NUMFLAG = NUMBOMB
BOMB = 'bomb'
#color
#                 R    G    B

TURQUOISE  = (   3,  178,  227) #cannot be 003
DARKBLUE   = (   6,   77,  135)
PINK       = ( 250,  117,  118)
JAUNE      = ( 255,  228,  197)
BLACK      = (   0,    0,    0)
WHITE      = ( 255,  255,  255)
DARKTURQUOISE = (  24,  41, 88)
RED1       = ( 255,  192,  203)
RED2       = ( 247,  143,  167)
RED3       = ( 217,   72,   97)
RED4       = ( 179,   33,   52)
RED5       = ( 212,  138,  146)
RED6       = ( 183,  110,  117)


FLAG = pygame.image.load('flag.png')
MINE = pygame.image.load('bomb.png')
EXPLODE = pygame.image.load('shockwave.png')

BGCOLOR = JAUNE
BORDERCOLOR = DARKTURQUOISE
TILECOLOR = JAUNE
TEXTCOLOR = PINK
BASICFONTSIZE = 24

BUTTONCOLOR = DARKBLUE
BUTTONTEXTCOLOR = WHITE
MESSAGECOLOR = TURQUOISE

XMARGIN = int((WINDOWWIDTH - (TILESIZE * BOARDWIDTH + (BOARDWIDTH - 1))) / 2)
YMARGIN = int((WINDOWHEIGHT - (TILESIZE * BOARDHEIGHT + (BOARDHEIGHT - 1))) / 2)

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, NEW_SURF, NEW_RECT, SOLVE_SURF, SOLVE_RECT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Minesweeper')
    BASICFONT = pygame.font.Font('iCielSoupofJustice.ttf', BASICFONTSIZE)


    # Store the option buttons and their rectangles in OPTIONS.
    NEW_SURF,   NEW_RECT   = makeText('New Game', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 60)
    SOLVE_SURF, SOLVE_RECT = makeText('Solve',    TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 30)

    board, bombLocation = newGame(BOARDWIDTH, BOARDHEIGHT, NUMBOMB)
    Mboard = getStartingBoard(BOARDWIDTH, BOARDHEIGHT)
    msg = 'Try to find ' + str(NUMBOMB) + ' bombs.'
    drawBoard(Mboard, msg)
    pygame.display.update()
    pygame.time.wait(500) # pause 500 milliseconds for effect

    flagLocation = []
    bombLeft = NUMBOMB
    NUMFLAG = NUMBOMB
    gameover = False
    mainBoard = getStartingBoard(BOARDWIDTH, BOARDHEIGHT)
    while True:
        checkForQuit()
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEBUTTONUP:
                spotx, spoty = getSpotClicked(mainBoard, event.pos[0], event.pos[1])
                if (spotx, spoty) == (None, None):
                    # check if the user clicked on an option button
                    if NEW_RECT.collidepoint(event.pos):  # clicked on New Game button
                        board, bombLocation = newGame(BOARDWIDTH, BOARDHEIGHT, NUMBOMB)
                        NUMFLAG = NUMBOMB
                        Mboard = getStartingBoard(BOARDWIDTH, BOARDHEIGHT)
                        msg = 'Try to find ' + str(NUMBOMB) + ' bombs.'
                        drawBoard(Mboard, msg)
                        flagLocation = []
                    elif SOLVE_RECT.collidepoint(event.pos):    # clicked on Solve button
                        solve(bombLocation)
                else:
                    if (event.button == 3):
                        # print((spotx, spoty))
                        if NUMFLAG > 0:
                            NUMFLAG = putFlag(NUMFLAG, flagLocation, spotx, spoty)
                        else:
                            textSurf, textRect = makeText("You don't have any flag left!", MESSAGECOLOR, BGCOLOR, 5, 5)
                            DISPLAYSURF.blit(textSurf, textRect)
                            checkWin(flagLocation, bombLocation)
                    elif checkBombLocation((spotx, spoty), bombLocation) == True:
                        gameover = gameOver()
                    else:
                        underneath(spotx, spoty, board, bombLocation)
            checkWin(flagLocation, bombLocation)

        # for event in pygame.event.get(): # event handling loop
        #     if event.type == MOUSEBUTTONUP:
        #         spotx, spoty = getSpotClicked(mainBoard, event.pos[0], event.pos[1])
        #         if (spotx, spoty) == (None, None):
        #             # check if the user clicked on an option button
        #             if NEW_RECT.collidepoint(event.pos):  # clicked on New Game button
        #                 gameOver = False
        #                 mainBoard = getStartingBoard(BOARDWIDTH, BOARDHEIGHT)
        #                 board, bombLocation = newGame(BOARDWIDTH, BOARDHEIGHT, NUMBOMB)


        pygame.display.update()
        FPSCLOCK.tick(FPS)

def terminate():
    pygame.quit()
    sys.exit()

def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate() # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event) # put the other KEYUP event objects back

def makeText(text, color, bgcolor, top, left):
    # create the Surface and Rect objects for some text.
    textSurf = BASICFONT.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)

def getStartingBoard(BOARDWIDTH, BOARDHEIGHT):
    board = []
    column = []
    tile = 0
    for i in range(BOARDWIDTH):
        column = []
        for i in range(BOARDHEIGHT):
            column.append(tile)
        board.append(column)
    return board

def drawBoard(board, message):
    DISPLAYSURF.fill(BGCOLOR)
    if message:
        textSurf, textRect = makeText(message, MESSAGECOLOR, BGCOLOR, 5, WINDOWHEIGHT - 30)
        DISPLAYSURF.blit(textSurf, textRect)
    left, top = getLeftTopOfTile(0, 0)
    width = (BOARDWIDTH) * (TILESIZE + MARGIN)
    height = (BOARDHEIGHT) * (TILESIZE + MARGIN)
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (left - 5, top - 5, width + 10, height + 10), 4)
    DISPLAYSURF.blit(NEW_SURF, NEW_RECT)
    DISPLAYSURF.blit(SOLVE_SURF, SOLVE_RECT)
    for row in range(BOARDWIDTH):
        for column in range(BOARDHEIGHT):

            pygame.draw.rect(DISPLAYSURF,
                             TURQUOISE,
                             [(MARGIN + TILESIZE) * column + XMARGIN,
                              (MARGIN + TILESIZE) * row + YMARGIN,
                              TILESIZE,
                              TILESIZE])

    pygame.display.update()
    FPSCLOCK.tick(FPS)

def getBoardCoordinate(board):  #get the list of all coordinates of tiles
    boardCoord = []
    for i in range(BOARDWIDTH):
        for j in range(BOARDHEIGHT):
            boardCoord.append((i, j))
    return boardCoord

def getLeftTopOfTile(tileX, tileY): #get x & y pixel coordinates of the tile
    left = XMARGIN + (tileX * TILESIZE) + (tileX - 1)
    top = YMARGIN + (tileY * TILESIZE) + (tileY - 1)
    return (left, top)

def getSpotClicked(board, x, y):
    # from the x & y pixel coordinates, get the x & y board coordinates
    for tileX in range(len(board)):
        for tileY in range(len(board[0])):
            left, top = getLeftTopOfTile(tileX, tileY)
            tileRect = pygame.Rect(left, top, TILESIZE, TILESIZE)
            if tileRect.collidepoint(x, y):
                return (tileX, tileY)
    return (None, None)

def getSurounding(board):
    for i in range(BOARDWIDTH):
        for j in range(BOARDHEIGHT):
            if not (board[i][j] == BOMB):
                if (j != BOARDHEIGHT - 1) and (board[i][j + 1] == BOMB):
                    board[i][j] += 1
                if (j != 0) and (board[i][j - 1] == BOMB):
                    board[i][j] += 1
                if (i != BOARDWIDTH - 1) and (j != BOARDHEIGHT - 1) and (board[i + 1][j + 1] == BOMB):
                    board[i][j] += 1
                if (i != BOARDWIDTH - 1) and (board[i + 1][j] == BOMB):
                    board[i][j] += 1
                if(i != BOARDWIDTH - 1) and (j != 0) and (board[i + 1][j - 1] == BOMB):
                    board[i][j] += 1
                if (i != 0) and (board[i - 1][j] == BOMB):
                    board[i][j] += 1
                if (i != 0) and (j != BOARDHEIGHT - 1) and (board[i - 1][j + 1] == BOMB):
                    board[i][j] += 1
                if (i != 0) and (j != 0) and (board[i - 1][j - 1] == BOMB):
                    board[i][j] += 1
    return board

def getRandomBomb(numBomb, board):
    boardCoord = getBoardCoordinate(board)
    bombLocation = []
    while (numBomb > 0):
        bombLocate = random.choice(boardCoord)
        numBomb -= 1;
        row = bombLocate[0]
        column = bombLocate[1]
        board[row][column] = BOMB
        bombLocation.append((row, column))
        boardCoord.remove(bombLocate)
    return board, bombLocation

def checkBombLocation(spot, bombLocation):
    if spot in bombLocation:
        return True
    else:
        return False

def newGame(BOARDWIDTH, BOARDHEIGHT, NUMBOMB):
    board = getStartingBoard(BOARDWIDTH, BOARDHEIGHT)
    board, bombLocation = getRandomBomb(NUMBOMB, board)
    board = getSurounding(board)
    return board, bombLocation

def solve(bombLocation):
    for spot in bombLocation:
        left, top = getLeftTopOfTile(spot[0], spot[1])
        pygame.draw.rect(DISPLAYSURF, TILECOLOR, (left + MARGIN, top + MARGIN, TILESIZE, TILESIZE))
        DISPLAYSURF.blit(MINE, (left + MARGIN, top + MARGIN) )

def drawTile(tilex, tiley, number, adjx=0, adjy=0):
    # draw a tile at board coordinates tilex and tiley, optionally a few
    # pixels over (determined by adjx and adjy)
    left, top = getLeftTopOfTile(tilex, tiley)
    pygame.draw.rect(DISPLAYSURF, TILECOLOR, (left + adjx, top + adjy, TILESIZE, TILESIZE))
    # textSurf = BASICFONT.render(str(number), True, TEXTCOLOR)

def underneath(tilex, tiley, board, bombLocation, adjx=1, adjy=1):
    x, y = getLeftTopOfTile(tilex, tiley)
    pygame.draw.rect(DISPLAYSURF, TILECOLOR, (x + adjx, y + adjy, TILESIZE, TILESIZE))
    if board[tilex][tiley] == 0:
        COLOR = RED1
    elif board[tilex][tiley] == 1:
        COLOR = RED2
    elif board[tilex][tiley] == 2:
        COLOR = RED3
    elif board[tilex][tiley] == 3:
        COLOR = RED4
    elif board[tilex][tiley] == 4:
        COLOR = RED5
    elif board[tilex][tiley] > 4:
        COLOR = RED6
    textSurf = BASICFONT.render(str(board[tilex][tiley]), True, COLOR)
    textRect = textSurf.get_rect()
    textRect.center = x + int(TILESIZE / 2) + adjx, y + int(TILESIZE / 2) + adjy
    DISPLAYSURF.blit(textSurf, textRect)
    pygame.display.update()
    FPSCLOCK.tick(FPS)

def gameOver():
    GameOverText = pygame.font.Font('iCielSoupofJustice.ttf', BASICFONTSIZE*3)
    text = GameOverText.render("Game Over", True, WHITE)
    text_rect = text.get_rect()
    text_x = DISPLAYSURF.get_width() / 2 - text_rect.width / 2
    text_y = DISPLAYSURF.get_height() / 2 - text_rect.height / 2
    XMarginGameOver = int((WINDOWWIDTH - 500) / 2)
    YMarrginGameOver = int((WINDOWHEIGHT - 500) / 2)
    DISPLAYSURF.blit(EXPLODE, (XMarginGameOver, YMarrginGameOver))
    DISPLAYSURF.blit(text, [text_x, text_y])
    return True

def putFlag(numFlag, flagLocation, spotx, spoty):
    left, top = getLeftTopOfTile(spotx, spoty)
    if (spotx, spoty) in flagLocation:
        pygame.draw.rect(DISPLAYSURF,
                         TURQUOISE,
                         [left + MARGIN, top + MARGIN,
                          TILESIZE,
                          TILESIZE])
        numFlag += 1
        flagLocation.remove((spotx, spoty))
    else:
        DISPLAYSURF.blit(FLAG, (left + MARGIN, top + MARGIN))
        numFlag -= 1
        flagLocation.append((spotx, spoty))
    msg = 'Flags: ' + str(numFlag) + '  '
    # print(flagLocation)

    textSurf, textRect = makeText(msg, MESSAGECOLOR, BGCOLOR, WINDOWWIDTH - 120, 5)
    DISPLAYSURF.blit(textSurf, textRect)
    pygame.display.update()
    FPSCLOCK.tick(FPS)
    return numFlag

def checkWin(FlagLocation, bombLocation):
    win = True
    if len(FlagLocation) != len(bombLocation):
        win = False
    else:
        for location in FlagLocation:
            if location not in bombLocation:
                win = False
    if win == True:
        textSurf, textRect = makeText("You won!", MESSAGECOLOR, BGCOLOR, 5, 5)
        DISPLAYSURF.blit(textSurf, textRect)
if __name__ == '__main__':
    main()
