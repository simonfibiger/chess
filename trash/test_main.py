import pygame
import random

pygame.init()

# Load background image
background_image = pygame.image.load("pictures/empty-chess-board-template-classic-ancient-game-on-wooden-floor-vector.jpg")
image_width, image_height = background_image.get_size()
screen = pygame.display.set_mode((image_width, image_height))
pygame.display.set_caption("CHESS")

# Constants for the board layout
EDGE = 100  # Distance from the edge of the screen to the first square
REAL_EDGE = 45
BOTTOM = 100  # Distance from the bottom of the screen to the first square
STRAIGHT_DISTANCE = 110  # Distance between the centers of squares
LIFT_SCALE = STRAIGHT_DISTANCE * 1.3
SHOW_MOVE = "pictures/actual/options.png"
round_num = 1

# Load piece images
pieces = {
    "black_bishop": "pictures/actual/Chess_bdt60.png",
    "black_king": "pictures/actual/Chess_kdt60.png",
    "black_knight": "pictures/actual/Chess_ndt60.png",
    "black_pawn": "pictures/actual/Chess_pdt60.png",
    "black_queen": "pictures/actual/Chess_qdt60.png",
    "black_rook": "pictures/actual/Chess_rdt60.png",
    "white_bishop": "pictures/actual/Chess_blt60.png",
    "white_king": "pictures/actual/Chess_klt60.png",
    "white_knight": "pictures/actual/Chess_nlt60.png",
    "white_pawn": "pictures/actual/Chess_plt60.png",
    "white_queen": "pictures/actual/Chess_qlt60.png",
    "white_rook": "pictures/actual/Chess_rlt60.png"
}

class Square:
    def __init__(self, name, x_range, y_range, occupied, show_move_position_x, show_move_position_y):
        self.name = name
        self.x_range = x_range
        self.y_range = y_range
        self.occupied = occupied
        self.xmove_pos = show_move_position_x
        self.ymove_pos = show_move_position_y
        self.circle_pos = (self.xmove_pos, self.ymove_pos)
        
        # Create a hitbox (rectangle) based on the x and y ranges
        self.hitbox = pygame.Rect(self.x_range[0], self.y_range[0], self.x_range[1] - self.x_range[0], self.y_range[1] - self.y_range[0])

    def show(self):
        self.image = pygame.image.load(SHOW_MOVE)
        self.option_rect = self.image.get_rect(center=self.circle_pos)
        screen.blit(self.image, self.option_rect.center)


squares = []
for row in range(8):
    for col in range(8):
        square_name = f"{chr(97 + col)}{8 - row}"  # Naming like 'a8', 'b8', ..., 'h1'
        x_start = REAL_EDGE + col * STRAIGHT_DISTANCE
        x_end = x_start + STRAIGHT_DISTANCE 

        y_start = REAL_EDGE + row * STRAIGHT_DISTANCE
        y_end = y_start + STRAIGHT_DISTANCE  
        occupied = False

        Show_move_position_x = x_start + ((x_end - x_start) / 2)  # Corrected X calculation
        Show_move_position_y = y_start + ((y_end - y_start) / 2)  # Corrected Y calculation

        square = Square(square_name, [x_start, x_end], [y_start, y_end], occupied, Show_move_position_x, Show_move_position_y)

        squares.append(square)

class Piece:
    def __init__(self, image_path, start_pos, scale_size, type, number, letter):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, scale_size)
        self.rect = self.image.get_rect(center=start_pos)
        self.hitbox = self.rect.inflate(self.rect.width * 0.1, self.rect.height * 0.1)
        self.lifted = False
        self.type = type
        self.number = number
        self.letter = letter
        square_name = f'{self.letter}{self.number}'
        self.square_index = next((i for i, sq in enumerate(squares) if sq.name == square_name), None)
        self.square = squares[self.square_index]

    def move(self, direction):
        global round_num
        self.rect.move_ip(direction)
        round_num += 1

    def spawn(self):
        screen.blit(self.image, self.rect.topleft)

    def lift(self):
        if not self.lifted:
            self.image = pygame.transform.scale(self.image, (int(LIFT_SCALE), int(LIFT_SCALE)))
            self.rect = self.image.get_rect(center=self.rect.center)  # Corrected
            self.lifted = True

    def show_options(self):
        squares_to_return = []
        if self.type == "pawn":
            # Check multiple rounds for testing
            if round_num <= 2:  
                for square in range(int(self.number) + 1, int(self.number) + 2):
                    square_name = str(self.letter + str(square))
                    for sq in squares:
                        if sq.name == square_name:
                            pass
                           # sq.show()
                           # squares_to_return.append(sq)
       # return squares_to_return


    def drop(self):
        if self.lifted:
            self.image = pygame.transform.scale(self.image, (STRAIGHT_DISTANCE, STRAIGHT_DISTANCE))
            self.rect = self.image.get_rect(center=self.rect.center)
            self.lifted = False

def create_board():
    piece_order = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
    pieces_on_board = {}

    for i, piece in enumerate(piece_order):
        # White pieces (bottom side)
        pieces_on_board[f"{chr(97 + i)}_wp"] = Piece(
            image_path=pieces[f"white_pawn"],
            start_pos=(EDGE + STRAIGHT_DISTANCE * i, image_height - (STRAIGHT_DISTANCE + BOTTOM)),
            scale_size=(STRAIGHT_DISTANCE, STRAIGHT_DISTANCE),
            type="pawn",
            letter=f"{chr(97 + i)}",
            number="2"
        )
        pieces_on_board[f"{chr(97 + i)}_w{piece[0]}"] = Piece(
            image_path=pieces[f"white_{piece}"],
            start_pos=(EDGE + STRAIGHT_DISTANCE * i, image_height - BOTTOM),
            scale_size=(STRAIGHT_DISTANCE, STRAIGHT_DISTANCE),
            type=piece,
            letter=f"{chr(97 + i)}",
            number="1"
        )

        # Black pieces (top side)
        pieces_on_board[f"{chr(97 + i)}_bp"] = Piece(
            image_path=pieces[f"black_pawn"],
            start_pos=(EDGE + STRAIGHT_DISTANCE * i, STRAIGHT_DISTANCE + BOTTOM),
            scale_size=(STRAIGHT_DISTANCE, STRAIGHT_DISTANCE),
            type="pawn",
            letter=f"{chr(97 + i)}",
            number="7"
        )
        pieces_on_board[f"{chr(97 + i)}_b{piece[0]}"] = Piece(
            image_path=pieces[f"black_{piece}"],
            start_pos=(EDGE + STRAIGHT_DISTANCE * i, BOTTOM),
            scale_size=(STRAIGHT_DISTANCE, STRAIGHT_DISTANCE),
            type=piece,
            letter=f"{chr(97 + i)}",
            number="8"
        )

    return pieces_on_board

pieces_on_board = create_board()
squares_to_blit = []
# Main loop
running = True
lifted_piece = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            for piece in pieces_on_board.values():
                if piece.lifted == True:
                    piece.drop()
                    lifted_piece = False
                elif piece.square.hitbox.collidepoint(mouse) and lifted_piece == False:
                    piece.lift()
                    lifted_piece = True

                    #squares_to_blit =  piece.show_options()
                    #print([sq_name.name for sq_name in squares_to_blit])
  
    
    # Draw the background image
    screen.blit(background_image, (0, 0))

    # Draw legal move squares
    if len(squares_to_blit) > 0:
        for square in squares_to_blit:
            square.show()


    # Spawn all pieces on the board
    for piece in pieces_on_board.values():
        piece.spawn()

    pygame.display.update()

# Quit Pygame
pygame.quit()
