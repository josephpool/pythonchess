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

def drawboard(state):
	for row in range(8):
		for column in range(8):
			if (row+column)%2 != 0:
				colour = black
			else: colour = white

			x = column * sq_size
			y = row * sq_size
			pygame.draw.rect(board, colour, (x, y,sq_size, sq_size))

			piece = state[row][column]
			if piece != "--":
				x = column * sq_size
				y = row * sq_size				
				board.blit(images[piece], pygame.Rect(x,y,sq_size,sq_size))

def get_sq(pos, state):
	c = int(pos[0]/sq_size)
	r = int(pos[1]/sq_size)
	return (r,c)

def main():
	load_images()
	state = chess_engine.gameState()
	update = True
	marked_piece = False
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.MOUSEBUTTONUP:
				pos = get_sq(pygame.mouse.get_pos(),state)
				if state.turn in state.Board[pos[0]][pos[1]]:
					#show legal moves

					marked_piece = pos
					update = True

				elif state.turn not in state.Board[pos[0]][pos[1]] and marked_piece:
					#elif pos in legal_moves: 
					target = pos
					state.move(marked_piece,target)

					if state.turn == "w": state.turn = "b"
					elif state.turn == "b": state.turn = "w"
					marked_piece = False
					update = True

		#board.fill(black)		

		if update == True:

			drawboard(state.Board)

			state.get_legal_moves()

			pygame.display.update()
			update = False

if __name__ == "__main__":
	main()

