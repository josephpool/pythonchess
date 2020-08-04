import pygame
import chess_engine


height =  width = 480
sq_size = height/8
black, white = (50,50,50),(255,255,255)
pygame.init()
board = pygame.display.set_mode((height, width))
clock = pygame.time.Clock()

images = {}

def load_images():
	pieces = ["wP","wR","wN","wB","wK","wQ","bP","bR","bN","bB","bK","bQ"]
	for piece in pieces:
		images[piece] = pygame.image.load("images/"+piece+".png")

def drawboard():
	for row in range(8):
		for column in range(8):
			if (row+column)%2 != 0:
				colour = black
			else: colour = white

			x = column * sq_size
			y = row * sq_size
			pygame.draw.rect(board, colour, (x, y,sq_size, sq_size))

def drawpieces(state):
	for r in range(8):
		for c in range(8):
			piece = state[r][c]
			if piece != "--":
				x = c * sq_size
				y = r * sq_size				
				board.blit(images[piece], pygame.Rect(x,y,sq_size,sq_size))

def get_sq(pos, state):
	c = int(pos[0]/sq_size)
	r = int(pos[1]/sq_size)
	if state[r][c] != "--":
		return (r,c)
	else: return False

def main():
	load_images()
	state = chess_engine.gameState()
	update = True

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.MOUSEBUTTONUP:
				pos = pygame.mouse.get_pos()
				#get_sq(pos, state.Board)

		#board.fill(black)		

		if update == True:
			drawboard()
			drawpieces(state.Board)
			update = False
			state.legal_moves()
			pygame.display.update()

if __name__ == "__main__":
	main()

