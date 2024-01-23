"""
for storing all information and determine the valid move
"""

class GameState():
	def __init__(self):
		#8x8
		self.board = [
			["bb","bb","bb","bb","bb","bb","bb","bb"],
			["bb","bb","bb","bb","bb","bb","bb","bb"],
			["--","--","--","--","--","--","--","--"],
			["--","--","--","--","--","--","--","--"],
			["--","--","--","--","--","--","--","--"],
			["--","--","--","--","--","--","--","--"],
			["ww","ww","ww","ww","ww","ww","ww","ww"],
			["ww","ww","ww","ww","ww","ww","ww","ww"]
			


		]
		self.whiteToMove = True
		self.moveLog = []
		self.check = False
		self.existWhite = 16
		self.existBlack = 16
		self.checkMate = False



	#take a move as a parameter and execute it
	def makeMove(self,move):
		self.board[move.startRow][move.startCol] = "--"
		
		self.board[move.endRow][move.endCol] = move.pieceMoved
		self.moveLog.append(move)
		self.whiteToMove = not self.whiteToMove  #swap players



	def undoMove(self):
		if len(self.moveLog) !=0:
			move = self.moveLog.pop()
			self.board[move.startRow][move.startCol] = move.pieceMoved
			self.board[move.endRow][move.endCol] = move.pieceCaptured
			self.whiteToMove = not self.whiteToMove


	def getValidMoves(self):

		moves = self.getPossibleMove() #generate all possible moves

		self.checkMate = False
		if self.inCheck(): 
			self.checkMate = True
			
		return moves

	def getValidMoves2(self):
		return self.getPossibleMove()
	#determine if the current player is in check
	def inCheck(self):
		if self.whiteToMove:
			return self.squareUnderAttack(7)
		else:
			return self.squareUnderAttack(0)



	def squareUnderAttack(self,r): #check if oppent is going to attack the last row

		self.whiteToMove = not self.whiteToMove
		oppMoves = self.getPossibleMove()
		self.whiteToMove = not self.whiteToMove
		for move in oppMoves:
			
			
			if move.endRow == r :
				return True

		return False


	def getPossibleMove(self):  #generate all possible move
		moves = []
		for r in range(len(self.board)):
			for c in range(len(self.board[r])):
				turn  = self.board[r][c][0]
				if (turn=="w" and self.whiteToMove) or (turn=="b" and not self.whiteToMove):

					self.pieceMove(r,c,moves)
		return moves
	def pieceMove(self,r,c,moves):

		if self.whiteToMove:
			if c!=0 and c!=7 and r-1>=0:
				if self.board[r-1][c] != "ww" :
					moves.append(Move((r,c),(r-1,c),self.board))					
				if self.board[r-1][c+1] != "ww" :
					moves.append(Move((r,c),(r-1,c+1),self.board))
				if self.board[r-1][c-1] != "ww" :
					moves.append(Move((r,c),(r-1,c-1),self.board))
			elif c==0:
				if self.board[r-1][c] != "ww":
					moves.append(Move((r,c),(r-1,c),self.board))					
				if self.board[r-1][c+1] != "ww" :
					moves.append(Move((r,c),(r-1,c+1),self.board))
			elif c==7:
				if self.board[r-1][c] != "ww":
					moves.append(Move((r,c),(r-1,c),self.board))					
				if self.board[r-1][c-1] != "ww" :
					moves.append(Move((r,c),(r-1,c-1),self.board))
		elif not self.whiteToMove:
			if c!=0 and c!=7 and r+1<=7:
				if self.board[r+1][c] != "bb" :
					moves.append(Move((r,c),(r+1,c),self.board))					
				if self.board[r+1][c+1] != "bb" :
					moves.append(Move((r,c),(r+1,c+1),self.board))
				if self.board[r+1][c-1] != "bb" :
					moves.append(Move((r,c),(r+1,c-1),self.board))
			elif c==0 and r+1<=7:
				if self.board[r+1][c] != "bb":
					moves.append(Move((r,c),(r+1,c),self.board))					
				if self.board[r+1][c+1] != "bb" :
					moves.append(Move((r,c),(r+1,c+1),self.board))
			elif c==7 and r+1<=7:
				if self.board[r+1][c] != "bb":
					moves.append(Move((r,c),(r+1,c),self.board))					
				if self.board[r+1][c-1] != "bb" :
					moves.append(Move((r,c),(r+1,c-1),self.board))

	def checkEndGame(self,move): #check if the piece move to th last row or the number of piece is zero
		if (move.pieceMoved=="ww" and move.endRow==0) or self.existBlack==0:
			return True
		elif (move.pieceMoved =='bb' and move.endRow==7) or self.existWhite==0:
			return True
		else:
			return False



						
class Move():
	#map keys to value
	ranksToRows = {"1":7, "2": 6, "3":5, "4":4, "5":3,"6":2 , "7":1 , "8":0}
	rowsToCols = {v:k for k,v in ranksToRows.items()}
	filesToCols = {"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7}
	colsToFiles = {v:k for k,v in filesToCols.items()}




	def __init__(self,startsq,endsq,board):
		self.startRow = startsq[0]
		self.startCol =  startsq[1]
		self.endRow = endsq[0]
		self.endCol = endsq[1]
		self.pieceMoved = board[self.startRow][self.startCol]
		self.pieceCaptured = board[self.endRow][self.endCol]
		self.moveID = self.startRow*1000 + self.startCol*100 + self.endRow*10 +self.endCol

	'''
	overriding the equals methods
	'''
	def __eq__(self,other):
		if isinstance(other,Move):
			return self.moveID == other.moveID
		return False
	def getChessNotation(self):
		return self.getRankFile(self.startRow,self.startCol) + self.getRankFile(self.endRow,self.endCol)
	def getRankFile(self,r,c):
		return self.colsToFiles[c]+self.rowsToCols[r]