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
		castling = ["K","Q","k","q"]
		castling_fen = "KQkq"
		enpassant = []

	def fen(self):
		position = ""
		print(self.Board)
		#board white in uppercase; block lowercase
		for row in self.Board:
			empty = 0
			counter = 0
			for piece in row:
				counter += 1
				if piece == "--":
					empty += 1
				if "w" in piece:
					if empty != 0:
						position += str(empty)
						position += piece[1].upper()
						empty = 0
					else:
						position += piece[1].upper()
				if "b" in piece:
					if empty != 0:
						position += str(empty)
						position += piece[1].lower()
						empty = 0
					else:
						position += piece[1].lower()
				if counter == 8 and empty != 0:
					position += str(empty)
			position += "/"
		#turn
		position += " "+self.turn
		#castling rights
		position += " "+self.castling_fen
		#en passant

		#half moves since last capture or pawn advance

		#number of full moves starts at 1 incremented after black's move

		return position

	def load_position(self, fen):
		self.Board = []
		rows = fen.split("/")
		for fen_row in rows:
			row = []
			for piece in fen_row:
				try:
					empty = int(piece)
					for i in range(empty):
						row.append("--")
				except:
					if piece.isupper():
						row.append("w"+piece)
					elif piece.islower():
						row.append("b"+piece.upper())

			self.Board.append(row)
		return self.Board

	def get_legal_moves(self,check_check=False):
		self.legal_moves = {}
		self.check_moves = {}
		row_n = 0
		for row in self.Board:
			column_n = 0
			for piece in row:
				if self.turn in piece:
					if "R" in piece:
						moves = []
						for i in [-1,1]:
							moves = self.rbqInner("R", moves, row_n, column_n, i,0)
							moves = self.rbqInner("R", moves, row_n, column_n, 0,i)
						self.legal_moves[(row_n,column_n)] = moves

					if "N" in piece:
						moves = []
						for i in [-2,2]:
							for j in [-1,1]:
								moves.append(self.rbqInner("N", moves, row_n, column_n, i, j))
								moves.append(self.rbqInner("N", moves, row_n, column_n, j, i))
						self.legal_moves[(row_n,column_n)] = moves

					if "B" in piece:
						moves = []
						for i in [-1,1]:
							for j in [-1,1]:
								moves = self.rbqInner("B", moves, row_n, column_n, i,j)
						self.legal_moves[(row_n,column_n)] = moves

					if "Q" in piece:
						moves = []
						for i in [-1,1]:
							moves = self.rbqInner("Q", moves, row_n, column_n, i,0)
							moves = self.rbqInner("Q", moves, row_n, column_n, 0,i)
							for j in [-1,1]:
								moves = self.rbqInner("Q", moves, row_n, column_n, i,j)
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
							Dir = -1
							start_row = 6
							not_turn = "b"
						elif "b" in piece:
							Dir = 1
							start_row = 1
							not_turn = "w"

						#move pawn foreward by one
						if not self.occupied([row_n+Dir, column_n]):
							moves.append([row_n+Dir, column_n])
							#move by two on first move
							if row_n==start_row and not self.occupied([row_n+Dir*2,column_n]):
								moves.append([row_n+Dir*2,column_n])
						#capture
						for column in [-1,1]:
							try:
								capture_sq = self.occupied([row_n+Dir,column_n+column])
								if not_turn == capture_sq:
									moves.append([row_n+Dir,column_n+column])
							except:
								pass

						#en passant

						#pawn promotion?

						self.legal_moves[(row_n,column_n)] = moves
				column_n += 1
			row_n += 1
		return self.legal_moves

	def rbqInner(self,p, moves, row, col, i,j):
		dis = 1
		blocked = False
		while True:
			next_sq = [row+i*dis,col+j*dis]

			if self.on_board(next_sq):
				if p == "N":
					print(next_sq)
				isBlocked = self.occupied(next_sq)
				if isBlocked == self.turn or isBlocked=="K":#blocked by own piece or by king
					#check_moves.append(next_sq)
					break
				elif not isBlocked:#free square
					moves.append(next_sq)
				else:#blocked by opponents piece (not the king)
					moves.append(next_sq)
					break
			else: break
			if p == "N":
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