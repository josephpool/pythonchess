class gameState():
	def __init__(self):
		self.Board = [["bR","bN","bB","bQ","bK","bB","bN","bR"],
					["bP","bP","bP","bP","bP","bP","bP","bP"],
					["--","--","--","--","--","--","--","--"],
					["--","--","--","--","--","--","--","--"],
					["--","--","--","--","--","--","--","--"],
					["--","--","--","--","--","--","--","--"],
					["wP","wP","wP","wP","wP","wP","wP","wP"],
					["wR","wN","wB","wQ","wK","wB","wN","wR"]]
		self.turn = "w" 
		self.movelog = []
		self.legal_moves = {}
		self.check = False

	def get_legal_moves(self):
		self.legal_moves = {}
		row_n = 0
		for row in self.Board:
			column_n = 0
			for piece in row:
				if self.turn in piece:
					if "R" in piece:
						moves = []
						for i in [-1,1]:
							moves = self.rbqInner(moves, row_n, column_n, i,0)
							moves = self.rbqInner(moves, row_n, column_n, 0,i)

						self.legal_moves[(row_n,column_n)] = moves
					if "N" in piece:
						moves = []

						for i in [-2,2]:
							for j in [-1,1]:
								next_sq = [row_n+i,column_n+j]
								if self.on_board(next_sq):
									isBlocked = self.occupied(next_sq)
									if not isBlocked:
										moves.append(next_sq)
									elif isBlocked == self.turn or isBlocked=="K":
										break
									else:	
										moves.append(next_sq)
										break
						for i in [-1,1]:
							for j in [-2,2]:
								next_sq = [row_n+i,column_n+j]
								if self.on_board(next_sq):
									isBlocked = self.occupied(next_sq)
									if not isBlocked:
										moves.append(next_sq)
									elif isBlocked == self.turn or isBlocked=="K":
										break
									else:	
										moves.append(next_sq)
										break

						self.legal_moves[(row_n,column_n)] = moves		
					if "B" in piece:
						moves = []
						for i in [-1,1]:
							for j in [-1,1]:
								moves = self.rbqInner(moves, row_n, column_n, i,j)

						self.legal_moves[(row_n,column_n)] = moves
					if "Q" in piece:
						moves = []
						for i in [-1,1]:
							moves = self.rbqInner(moves, row_n, column_n, i,0)
							moves = self.rbqInner(moves, row_n, column_n, 0,i)
							for j in [-1,1]:
								moves = self.rbqInner(moves, row_n, column_n, i,j)

						self.legal_moves[(row_n,column_n)] = moves
					if "K" in piece:
						moves = []
						for r in range(-1,2,1):
							for c in range(-1,2,1):
								if r!=0 or c!=0:
									pos_r = row_n+r
									pos_c = column_n+c
									if self.on_board([pos_r,pos_c]):
										if self.turn not in self.Board[pos_r][pos_c] and not "K" in self.Board[pos_r][pos_c]:
											#cant capture own pieces						or opponents king
											moves.append([pos_r,pos_c])
						self.legal_moves[(row_n,column_n)] = moves

					if "P" in piece:
						moves = []
						if "w" in piece:
							moves.append([row_n-1,column_n])
							if row_n==6:
								moves.append([row_n-2,column_n])
						if "b" in piece:
							moves.append([row_n+1,column_n])
							if row_n==1:
								moves.append([row_n+2,column_n])

						self.legal_moves[(row_n,column_n)] = moves

				column_n += 1
			row_n += 1



		return self.legal_moves
	def rbqInner(self,moves, row, col, i,j):
		dis = 1
		blocked = False
		while True:
			next_sq = [row+i*dis,col+j*dis]
			if not self.on_board(next_sq):	break

			isBlocked = self.occupied(next_sq)
			if isBlocked == self.turn or isBlocked=="K":#blocked by own piece or by king
				break
			elif not isBlocked:#free square
				moves.append(next_sq)
			else:#blocked by opponents piece (not the king)	
				moves.append(next_sq)
				break
			dis += 1
		return moves

	def on_board(self, sq):
		if 0<=sq[0]<8 and 0<=sq[1]<8:	return True
		else:	return False

	def occupied(self,sq):
		if self.Board[sq[0]][sq[1]] == "--":
			return False
		if "K" in self.Board[sq[0]][sq[1]]:
			return "K"	
		if "w" in self.Board[sq[0]][sq[1]]:
			return "w"
		if "b" in self.Board[sq[0]][sq[1]]:
			return "b"	


	def absolute_pin(self):
		pass

	def move(self,current_sq,target):
		r, c = target
		self.Board[r][c] = self.Board[current_sq[0]][current_sq[1]]
		self.Board[current_sq[0]][current_sq[1]] = "--"