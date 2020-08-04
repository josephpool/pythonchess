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

	def legal_moves(self):
		self.legal_moves = []
		for r in self.Board:
			for piece in r:
				if self.turn_white in piece:
					print(piece)
					if "R" in piece:
						pass
					if "N" in piece:
						pass
					if "B" in piece:
						pass
					if "Q" in piece:
						pass
					if "K" in piece:
						pass
					if "P" in piece:
						pass


		return self.legal_moves
		

	def absolute_pin(self):
		pass