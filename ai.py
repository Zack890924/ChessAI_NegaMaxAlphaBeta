import random


DEPTH = 3 #depth to search
CHECKMATE = 10000
#determine piece score on different position
pieceBlackScore = [[0,0,0,0,0,0,0,0],
			  [5,5,5,5,5,5,5,5],
			  [10,10,10,10,10,10,10,10],
			  [13,13,13,13,13,13,13,13],
			  [15,15,15,15,15,15,15,15],
			  [25,25,25,25,25,25,25,25],
			  [50,50,50,50,50,50,50,50],
			  [300,300,300,300,300,300,300,300]
			 ]

pieceWhiteScore = [[300,300,300,300,300,300,300,300],
			  [50,50,50,50,50,50,50,50],
			  [25,25,25,25,25,25,25,25],
			  [15,15,15,15,15,15,15,15],
			  [13,13,13,13,13,13,13,13],
			  [10,10,10,10,10,10,10,10],
			  [5,5,5,5,5,5,5,5],
			  [0,0,0,0,0,0,0,0]
			 ]





def findRandomMove(validMoves):
	return validMoves[random.randint(0,len(validMoves)-1)]


def findBestMove(gs,validMoves):
	global nextMove
	nextMove = None
	random.shuffle(validMoves)
	findMoveNegaMaxAlphaBeta(gs,validMoves,DEPTH,-CHECKMATE,CHECKMATE,1 if gs.whiteToMove else -1)
	return nextMove




#NegaMax AlphaBeta puring

def findMoveNegaMaxAlphaBeta(gs,validMoves,depth,alpha,beta,turn):
	global nextMove
	if depth ==0:
		return turn * (pieceAndColumnScore(gs) +potentialDangerPiece(gs))

	maxScore = -CHECKMATE
	for move in validMoves:
		gs.makeMove(move)
		nextMoves = gs.getValidMoves()
		score = -findMoveNegaMaxAlphaBeta(gs,nextMoves,depth-1 ,-beta, -alpha,-turn)
		if score>maxScore:
			maxScore = score	
			if depth == DEPTH:
				nextMove = move
		gs.undoMove()
		if maxScore >alpha:   #puring happens
			alpha = maxScore
		if alpha >=beta:
			break
	return maxScore









#add more value to the piece which it will be the potential danger
def potentialDangerPiece(gs):
	score = 0
	if  gs.whiteToMove:
		for i in range(8):
			if gs.board[2][i] == 'ww':
				if i!=0 and i!=7:
					if gs.board[0][i+1]!='bb'or gs.board[0][i-1]!='bb' or gs.board[0][i]!='bb':
						score-=1000
				elif i==7:
					if gs.board[0][i-1]!='bb' or gs.board[0][i]!='bb':
						score-=1000
				elif i==0:
					if gs.board[0][i+1]!='bb' or gs.board[0][i]!='bb':
						
						score-=1000

	else:
		for i in range(8):
			if gs.board[5][i] == 'bb':
				if i!=0 and i!=7:
					if gs.board[7][i+1]!='ww'or gs.board[7][i-1]!='ww' or gs.board[7][i]!='ww':
						score+=1000
				elif i==7:
					if gs.board[7][i-1]!='ww' or gs.board[7][i]!='ww':
						score+=1000
				elif i==0:
					if gs.board[7][i+1]!='ww' or gs.board[7][i]!='ww':
						score+=1000
	

	return score




	
#calculate the score

def pieceAndColumnScore(gs):
	if gs.checkMate:
		if gs.whiteToMove:
			
			return CHECKMATE
		else:
			
			return -CHECKMATE
	score = 0
	for row in range(len(gs.board)):
		for col in range(len(gs.board[row])):
			sq = gs.board[row][col]
			if sq[0] == 'w':
				score = score+1+pieceWhiteScore[row][col] #number of white and the distance score to the end row
			elif sq[0] =='b':
				score  = score-1-pieceBlackScore[row][col]


	return score


