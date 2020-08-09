import pygame
import chess_engine

height =  width = 480
sq_size = int(height/8)
black, white = (100,100,100),(255,255,255)
pygame.init()
board = pygame.display.set_mode((height, width))
clock = pygame.time.Clock()

images = {}
def load_images():
	pieces = ["wP","wR","wN","wB","wK","wQ","bP","bR","bN","bB","bK","bQ"]
	for piece in pieces:
		images[piece] = pygame.image.load("images/"+piece+".png")

def drawboard(state,legal_moves, marked_piece):
	for row in range(8):
		for column in range(8):
			#draws chess board
			if (row+column)%2 != 0:
				colour = black
			else: colour = white
			x = int(column * sq_size)
			y = int(row * sq_size)
			pygame.draw.rect(board, colour, (x, y,sq_size, sq_size))

			#draws pieces
			piece = state[row][column]
			if piece != "--":
				x = column * sq_size
				y = row * sq_size	
				board.blit(images[piece], pygame.Rect(x,y,sq_size,sq_size))

			#draws legal moves
			try:
				if [row,column] in legal_moves[marked_piece]:
					x = int((column+0.5)*sq_size)
					y = int((row+0.5)*sq_size)
					pygame.draw.circle(board, (150,180,120),(x,y),5)
			except KeyError:
				pass

def get_sq(pos, state):
	c = int(pos[0]/sq_size)
	r = int(pos[1]/sq_size)
	return (r,c)

def main():
	load_images()
	state = chess_engine.gameState()
	update = True
	marked_piece = False
	state.get_legal_moves()	
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.MOUSEBUTTONUP:
				pos = get_sq(pygame.mouse.get_pos(),state)
				
				try:
					if state.turn in state.Board[pos[0]][pos[1]]:
						marked_piece = pos
						update = True

					elif list(pos) in state.legal_moves[marked_piece]:
						target = pos
						state.move(marked_piece,target)

						if state.turn == "w": state.turn = "b"
						elif state.turn == "b": state.turn = "w"
						marked_piece = False
						state.get_legal_moves()
						update = True
				except KeyError:
					pass	

		if update == True:
			drawboard(state.Board, state.legal_moves, marked_piece)
			pygame.display.update()
			update = False

if __name__ == "__main__":
	main()