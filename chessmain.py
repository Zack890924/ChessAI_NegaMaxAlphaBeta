"""
for user input and display the current gamestate
"""


import pygame as  p
from chessengine import *
from ai import *
from multiprocessing import Process, Queue

Width = Height = 512
MOVE_LOG_PANEL_WIDTH = 250
MOVE_LOG_PANEL_HEIGHT = Height
dim = 8
sq_size = Height//dim
max_fps = 15
IMAGES = {}

"""



"""
#load black and white piece
def loadImages():
	IMAGES['bb'] = p.transform.scale(p.image.load('images/b.png'),(sq_size,sq_size))
	IMAGES['ww'] = p.transform.scale(p.image.load('images/w.png'),(sq_size,sq_size))



def main():
	p.init()
	screen = p.display.set_mode((Width+MOVE_LOG_PANEL_WIDTH,Height))
	clock = p.time.Clock()
	screen.fill(p.Color("white"))
	gs = GameState() #initial gamestate
	validMoves = gs.getValidMoves()

	moveLogFont = p.font.SysFont("Arial",12,False,False)
	gameOver = False
	loadImages()
	moveMade = False
	playerClicks = [] #keep track of player clicks
	sqSelected = ()  # no square is selected initally
	running = True
	playerOne = True #human playing white
	playerTwo = False #human playing black



	while running:
		humanTurn = (gs.whiteToMove and playerOne) 

		for e in p.event.get():
			if e.type == p.QUIT:
				running = False

			elif e.type==p.MOUSEBUTTONDOWN: 
				if not gameOver and humanTurn:
					
					location = p.mouse.get_pos()
					col = location[0]//sq_size
					row = location[1]//sq_size
					
					if sqSelected ==(row,col) or col>=8: ##user clicked the same square twice
						sqSelected = ()
						playerClicks = []
						
					else:
						sqSelected = (row,col) 
						playerClicks.append(sqSelected)
						 # print(playerClicks)
						
					
					if len(playerClicks) ==2: 
						
						
							
						move = Move(playerClicks[0],playerClicks[1],gs.board) 
				
						
						for i in range(len(validMoves)): #make the move and check the black piece number
							if move == validMoves[i]:		
								gs.makeMove(validMoves[i])
								if move.pieceCaptured=='bb':
									gs.existBlack = gs.existBlack-1
								
								moveMade = True
								sqSelected = () #reset
								playerClicks = [] #reset
						
						if not moveMade:
						
							playerClicks = [sqSelected]
						if gs.checkEndGame(move):    #if end game set gameOver to True

							gameOver = True

							
								
								
			

			#AI move
			if not gameOver and not humanTurn and not gs.whiteToMove:

				AIMove = findBestMove(gs,validMoves) #call the apha beta function 

				if AIMove is None:   #if no move can make, make random move
					validMoves2 = gs.getValidMoves2()
					AIMove = findRandomMove(validMoves2)
					print('Random Move')
					
					
				gs.makeMove(AIMove)
				if move.pieceCaptured=='ww': #check the white piece number
					gs.existWhite = gs.existWhite-1
				if gs.checkEndGame(AIMove):
					gameOver = True
					
				moveMade = True
				AIThinking = False
			

			if moveMade:
				
				validMoves = gs.getValidMoves()			
				moveMade = False


		drawGameState(screen,gs,validMoves,sqSelected,moveLogFont)   #draw the gamestate

		
		if e.type == p.KEYDOWN:
			if e.key ==p.K_z: #undo move when  z is pressed
				gs.undoMove()
				moveMade = True
			if e.key ==p.K_r: #reset the game if r is pressed
				gs = GameState()
				validMoves = gs.getValidMoves()
				sqSelected = ()
				playerClicks = []
				moveMade = False
		if gameOver:
			if  gs.whiteToMove:
				text = 'Black Wins'
				drawEndGameText(screen,text)
				if e.type == p.KEYDOWN:
					if e.key ==p.K_r:
						gs = GameState()
						validMoves = gs.getValidMoves()
						sqSelected = ()
						playerClicks = []
						moveMade = False
						gameOver = False
				
			else:
				text = 'White Wins'
				drawEndGameText(screen,text)
				if e.type == p.KEYDOWN:
					if e.key ==p.K_r:
						gs = GameState()
						validMoves = gs.getValidMoves()
						sqSelected = ()
						playerClicks = []
						moveMade = False
						gameOver = False
				
		clock.tick(max_fps)
		p.display.flip()
def highlightSquares(screen,gs,validMoves,sqSelected): #function to color the select square and its valid moves
	if sqSelected !=():
		r,c = sqSelected
		if gs.board[r][c][0]== ('w' if gs.whiteToMove else 'b'):
			s = p.Surface((sq_size,sq_size))
			s.set_alpha(100) #transperancy value
			s.fill(p.Color('blue'))
			screen.blit(s,(c*sq_size , r*sq_size))
			s.fill(p.Color('yellow'))
			for move in validMoves:
				if move.startRow ==r and move.startCol ==c:
					screen.blit(s,(sq_size *move.endCol ,sq_size* move.endRow))

def drawGameState(screen,gs,validMoves,sqSelected,moveLogFont):
	drawBoard(screen)
	highlightSquares(screen,gs,validMoves,sqSelected)
	drawPieces(screen,gs.board)
	drawMoveLog(screen,gs,moveLogFont)




def drawMoveLog(screen,gs,font):  #function to print moveLog on the right of the board
	
	moveLogRect = p.Rect(Width,0,MOVE_LOG_PANEL_WIDTH,MOVE_LOG_PANEL_HEIGHT)
	p.draw.rect(screen,p.Color('black'),moveLogRect)
	moveLog = gs.moveLog
	moveTexts = []
	for i in range(0,len(moveLog),2):
		moveString = str(i//2 + 1) + ", " +moveLog[i].getChessNotation() +" "
		if i+1 < len(moveLog): #make sure black made a move
			moveString += moveLog[i+1].getChessNotation()
		moveTexts.append(moveString)
	padding =  5
	textY = padding
	for i in range(len(moveTexts)):
		text =moveTexts[i]
		textObject = font.render(text,True,p.Color('white'))
		textLocation = moveLogRect.move(padding,textY)
		screen.blit(textObject,textLocation)
		textY += textObject.get_height() + 2



def drawBoard(screen):

	colors = [p.Color("white"),p.Color("gray")]
	for i in range(dim):
		for j in range(dim):
			color = colors[((i+j) %2)]
			p.draw.rect(screen,color,p.Rect(j*sq_size,i*sq_size,sq_size,sq_size))





def drawPieces(screen,board):
	for r in range(dim):
		for c in range(dim):
			piece = board[r][c]
			if piece != "--":
				screen.blit(IMAGES[piece],p.Rect(c*sq_size,r*sq_size,sq_size,sq_size))
def drawEndGameText(screen , text):
	font = p.font.SysFont("Helvitca",32,True,False) #setting font
	textObject = font.render(text,0,p.Color('Black'))
	textLocation = p.Rect(0,0,Width,Height).move(Width/2 - textObject.get_width()/2,Height/2 - textObject.get_height()/2)
	screen.blit(textObject,textLocation)



if __name__=="__main__":
	main()


