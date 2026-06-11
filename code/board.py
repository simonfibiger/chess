from game_state import GameState
import pygame


Gm = GameState()

class Square:
    def __init__(self, name, x_range, y_range, occupied, show_move_position_x, show_move_position_y, letter, number, piece_pos):
        self.name = name
        self.piece_pos = piece_pos
        self.x_range = x_range
        self.y_range = y_range
        self.occupied = occupied
        self.occupied_by_color = ""
        self.xmove_pos = show_move_position_x
        self.ymove_pos = show_move_position_y
        self.circle_pos = (self.xmove_pos, self.ymove_pos)
        self.letter = letter
        self.number = int(number)
        
        # Create a hitbox (rectangle) based on the x and y ranges
        self.hitbox = pygame.Rect(self.x_range[0], self.y_range[0], self.x_range[1] - self.x_range[0], self.y_range[1] - self.y_range[0])

    def show(self):
        self.image = pygame.image.load(Gm.SHOW_MOVE)
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 0.2), int(self.image.get_height() * 0.2)))
        self.option_rect = self.image.get_rect(center=self.circle_pos)
        Gm.screen.blit(self.image, self.option_rect.topleft)
    
    def draw_hitbox(self):
        pygame.draw.rect(Gm.screen, (255, 0, 0), self.hitbox, 2)
        pygame.draw.circle(Gm.screen, (255, 0, 0), self.circle_pos, 10)

def create_squares():

    squares = []
    for row in range(8):
        for col in range(8):
            square_name = f"{chr(97 + col)}{8 - row}"  # Naming like 'a8', 'b8', ..., 'h1'
            x_start = Gm.EDGE + col * Gm.STRAIGHT_DISTANCE
            x_end = x_start + Gm.STRAIGHT_DISTANCE
            y_start = row * Gm.STRAIGHT_DISTANCE
            y_end = y_start + Gm.STRAIGHT_DISTANCE  
            piece_pos = (x_start + (x_end - x_start)/2, y_start + (y_end - y_start)/2 )
            occupied = False

            Show_move_position_x = x_start + ((x_end - x_start) / 2)  # Corrected X calculation
            Show_move_position_y = y_start + ((y_end - y_start) / 2)  # Corrected Y calculation

            square = Square(square_name, [x_start, x_end], [y_start, y_end], occupied, Show_move_position_x, Show_move_position_y, letter=f'{chr(97+ col)}', number=int(8-row), piece_pos = piece_pos)
            squares.append(square)
    return squares
