import pygame
import random
import time 
import os
import sys

pygame.init()
pygame.mixer.init()

#Load sounds
import pygame

# Initialize pygame mixer
pygame.mixer.init()

# Dictionary to store sound effects
sounds = {
    "achievement": pygame.mixer.Sound("pictures/actual/game sounds/standard/achievement.mp3"),
    "capture": pygame.mixer.Sound("pictures/actual/game sounds/standard/capture.mp3"),
    "castle": pygame.mixer.Sound("pictures/actual/game sounds/standard/castle.mp3"),
    "click": pygame.mixer.Sound("pictures/actual/game sounds/standard/click.mp3"),
    "correct": pygame.mixer.Sound("pictures/actual/game sounds/standard/correct.mp3"),
    "decline": pygame.mixer.Sound("pictures/actual/game sounds/standard/decline.mp3"),
    "drawoffer": pygame.mixer.Sound("pictures/actual/game sounds/standard/drawoffer.mp3"),
    "event_end": pygame.mixer.Sound("pictures/actual/game sounds/standard/event-end.mp3"),
    "event_start": pygame.mixer.Sound("pictures/actual/game sounds/standard/event-start.mp3"),
    "event_warning": pygame.mixer.Sound("pictures/actual/game sounds/standard/event-warning.mp3"),
    "game_draw": pygame.mixer.Sound("pictures/actual/game sounds/standard/game-draw.mp3"),
    "game_end": pygame.mixer.Sound("pictures/actual/game sounds/standard/game-end.mp3"),
    "game_lose": pygame.mixer.Sound("pictures/actual/game sounds/standard/game-lose.mp3"),
    "game_lose_long": pygame.mixer.Sound("pictures/actual/game sounds/standard/game-lose-long.mp3"),
    "game_start": pygame.mixer.Sound("pictures/actual/game sounds/standard/game-start.mp3"),
    "game_win": pygame.mixer.Sound("pictures/actual/game sounds/standard/game-win.mp3"),
    "game_win_long": pygame.mixer.Sound("pictures/actual/game sounds/standard/game-win-long.mp3"),
    "illegal": pygame.mixer.Sound("pictures/actual/game sounds/standard/illegal.mp3"),
    "incorrect": pygame.mixer.Sound("pictures/actual/game sounds/standard/incorrect.mp3"),
    "lesson_fail": pygame.mixer.Sound("pictures/actual/game sounds/standard/lesson-fail.mp3"),
    "lesson_pass": pygame.mixer.Sound("pictures/actual/game sounds/standard/lesson-pass.mp3"),
    "move_check": pygame.mixer.Sound("pictures/actual/game sounds/standard/move-check.mp3"),
    "move_opponent": pygame.mixer.Sound("pictures/actual/game sounds/standard/move-opponent.mp3"),
    "move_self": pygame.mixer.Sound("pictures/actual/game sounds/standard/move-self.mp3"),
    "notification": pygame.mixer.Sound("pictures/actual/game sounds/standard/notification.mp3"),
    "notify": pygame.mixer.Sound("pictures/actual/game sounds/standard/notify.mp3"),
    "premove": pygame.mixer.Sound("pictures/actual/game sounds/standard/premove.mp3"),
    "promote": pygame.mixer.Sound("pictures/actual/game sounds/standard/promote.mp3"),
    "puzzle_correct": pygame.mixer.Sound("pictures/actual/game sounds/standard/puzzle-correct.mp3"),
}

# Load background image
background_image = pygame.image.load("pictures/actual/chess_bg.png")

screen_info = pygame.display.Info()
screen_width, screen_height = screen_info.current_w, screen_info.current_h
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Menu")


image_width, image_height = background_image.get_size()
#print(image_height, image_width)
#screen = pygame.display.set_mode((image_width, image_width))
#pygame.display.set_caption("CHESS")
# Constants for the board layout
EDGE = 417
STRAIGHT_DISTANCE = 135.5  # Distance between the centers of squares
BOARD_LEN = 1168
LIFT_SCALE = STRAIGHT_DISTANCE * 1.3
SHOW_MOVE = "pictures/actual/options.png"

def create_red_overlay(sq):
    # Inflate the hitbox by 30% in both width and height
    inflated_hitbox = sq.hitbox.inflate(sq.hitbox.width * 0.1, sq.hitbox.height * 0.1)
    
    # Create a Surface the size of the inflated hitbox
    rect_surface = pygame.Surface(inflated_hitbox.size)  # Surface size matches the inflated hitbox size
    rect_surface.set_alpha(128)  # Set transparency to 50% (128/255)
    rect_surface.fill((255, 0, 0))  # Fill the surface with red color
    
    # Blit the semi-transparent red surface over the square's hitbox on the main screen
    screen.blit(rect_surface, inflated_hitbox.topleft)  # Blit at the top-left corner of the inflated hitbox



round_num = 1
rset = False
game_over_font = pygame.font.Font("pictures/actual/font.ttf", 40)  # Adjust the font size as needed'
game_over_font2 = pygame.font.Font("pictures/actual/font.ttf", 40) # Adjust the font size as needed'



def priner(list):
    for one in list:
        print(one.name)
def reset():
    global rset
    rset = True
def GAME_OVER(side):
    if side:
        game_over_text = "Game Over, White Lost!"
    else:
        game_over_text = "Game Over, Black Lost!"
    rst = "(press 'r' to reset)"



    text_surface = game_over_font.render(game_over_text, True, (255, 0, 0))  # Red text
    text2_surface = game_over_font.render(rst, True, (0, 0, 0))
    text2_rect = text2_surface.get_rect(center=(image_width // 2, image_height // 2 + 100))
    text_rect = text_surface.get_rect(center=(image_width // 2, image_height // 2))
    screen.blit(text_surface, text_rect)
    screen.blit(text2_surface, text2_rect)

    not_clicked = True

    while not_clicked:
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Optionally allow mouse click to also exit game over screen
            if event.type == pygame.MOUSEBUTTONDOWN:
                not_clicked = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Check if the 'R' key was pressed
                    not_clicked = False
                    print('reset happnes in game over ')
                    reset()  # Call the reset function

    # Reset game state for restarting (you need to implement this logic)
    

    # You may need to reinitialize any other variables used in your game


# Load piece images
base_path = os.path.join("pictures", "actual", "pieces")

pieces = {
    "black_bishop": os.path.join(base_path, "bb.png"),
    "black_king": os.path.join(base_path, "bk.png"),
    "black_knight": os.path.join(base_path, "bn.png"),
    "black_pawn": os.path.join(base_path, "bp.png"),
    "black_queen": os.path.join(base_path, "bq.png"),
    "black_rook": os.path.join(base_path, "br.png"),
    "white_bishop": os.path.join(base_path, "wb.png"),
    "white_king": os.path.join(base_path, "wk.png"),
    "white_knight": os.path.join(base_path, "wn.png"),
    "white_pawn": os.path.join(base_path, "wp.png"),
    "white_queen": os.path.join(base_path, "wq.png"),
    "white_rook": os.path.join(base_path, "wr.png")
}

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
        self.image = pygame.image.load(SHOW_MOVE)
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 0.2), int(self.image.get_height() * 0.2)))
        self.option_rect = self.image.get_rect(center=self.circle_pos)
        screen.blit(self.image, self.option_rect.topleft)
    
    def draw_hitbox(self):
        pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)
        pygame.draw.circle(screen, (255, 0, 0), self.circle_pos, 10)



class Piece:
    def __init__(self,name, image_path, scale_size, type, number, letter, color):
        self.name = name
        self.in_check = False
        self.checked_by = ""
        self.image_path = image_path
        self.scale_size =scale_size
        self.image = pygame.image.load(self.image_path)
        self.image = pygame.transform.scale(self.image, self.scale_size)
      
        self.lifted = False
        self.type = type
        self.number = int(number)
        self.letter = letter
        self.square_name = f'{self.letter}{str(self.number)}'
        self.square_index = next((i for i, sq in enumerate(squares) if sq.name == self.square_name), None)
        self.square = squares[self.square_index]
        self.start_pos = self.square.piece_pos
        self.square.occupied = True
        self.square.occupied_by_color = color
        self.color = color
        self.number_of_moves = 0
        self.rect = self.image.get_rect(center=self.start_pos)
        self.hitbox = self.rect.inflate(self.rect.width * 0.1, self.rect.height * 0.1)



        self.square.occupied = True

    def move(self, new_square):
        """Move the piece to the new square."""
        # Move the piece to the center of the new square
        self.rect.center = new_square.circle_pos
        self.square.occupied = False  # Free up the old square
        self.square.occupied_by_color = ''
        not_occ = True
        

        # If there is an opponent's piece, delete it
        if new_square.occupied:
            not_occ = False
            for piece in list(pieces_on_board.values()):
                if piece.square == new_square:
                    piece.delete()

                    # Check if the captured piece is a king
                    if piece.type == "king":
                        self.square = new_square
                        self.square.occupied = True
                        self.square.occupied_by_color = self.color
                        self.number_of_moves += 1
                        self.letter = new_square.letter
                        self.number = int(new_square.number)
                        screen.blit(background_image, (0, 0))
                        for piece in pieces_on_board.values():
                            piece.spawn()
                        sounds["game_end"].play()
                        GAME_OVER(side=piece.color)
                        return False
                    else:
                        sounds["capture"].play()
      
        # Handle castling logic for both white and black
        if self.type == "king":
            # For white pieces, use ranks 1 (e.g., f1, d1)
            if self.color:  # True represents white
                kingside_rook_square = "h1"
                queenside_rook_square = "a1"
                kingside_rook_new_square = "f1"
                queenside_rook_new_square = "d1"
            else:  # For black pieces, use ranks 8 (e.g., f8, d8)
                kingside_rook_square = "h8"
                queenside_rook_square = "a8"
                kingside_rook_new_square = "f8"
                queenside_rook_new_square = "d8"

            # Kingside castling (move king 2 squares to the right)
            if ord(self.square.letter) - ord(new_square.letter) == -2:
                for sq in squares:
                    if sq.name == kingside_rook_new_square:
                        rook_new_square = sq  # Square for the rook in kingside castling
                for piece in pieces_on_board.values():
                    if piece.color == self.color and piece.square.name == kingside_rook_square:
                        rook = piece  # Identify the rook for castling
                        rook.move(rook_new_square)  # Move the rook to its new square
                        sounds["castle"].play()
     
              
                        break

            # Queenside castling (move king 2 squares to the left)
            elif ord(self.square.letter) - ord(new_square.letter) == 2:
                for sq in squares:
                    if sq.name == queenside_rook_new_square:
                        rook_new_square = sq  # Square for the rook in queenside castling
                for piece in pieces_on_board.values():
                    if piece.color == self.color and piece.square.name == queenside_rook_square:
                        rook = piece  # Identify the rook for castling
                        rook.move(rook_new_square)  # Move the rook to its new square
                        sounds["castle"].play()
          
                
                        break
      
        self.square = new_square
        self.square.occupied = True
        self.square.occupied_by_color = self.color
        self.number_of_moves += 1
        self.letter = new_square.letter
        self.number = int(new_square.number)

        # Check if the opponent's king is in check
        opponent_color = not self.color
 
        def is_king_in_check(king_color):
            """Check if the king of the given color is in check."""

            
            white_king = None
            black_king = None
            
            for piece in pieces_on_board.values():

                if piece.type == "king":
                    if piece.color == True:
                        white_king = piece
                    else:
                        black_king = piece
                    if white_king != None and black_king != None:
                     break

            # Check if any of the opponent's pieces can move to the king's square
            for piece in pieces_on_board.values():
                possible_moves = piece.show_options(c_check = True)  # Get possible moves
                if white_king.square in possible_moves:
                    white_king.in_check = True
                    white_king.checked_by = piece.name
                    return True
                else:
                    white_king.in_check = False
            for piece in pieces_on_board.values():
                possible_moves = piece.show_options(c_check = True)  # Get possible moves           
                if black_king.square in possible_moves:
                    black_king.in_check = True
                    black_king.checked_by = piece.name
                    return True
                else:
                    black_king.in_check = False
          
        
        if is_king_in_check(opponent_color):
                print("The king is in check")
                sounds["move_check"].play()
        
        else:
            if not_occ == True:
                  sounds["move_self"].play()


    def delete(self):
        for key in list(pieces_on_board.keys()):
            if pieces_on_board[key] == self:
                del pieces_on_board[key]
                break

    def spawn(self):
        screen.blit(self.image, self.rect.topleft)

    def lift(self):
 
        if not self.lifted:
            self.image = pygame.image.load(self.image_path)
            self.image = pygame.transform.scale(self.image, self.scale_size)
            self.image = pygame.transform.scale(self.image, (int(LIFT_SCALE), int(LIFT_SCALE)))
            self.rect = self.image.get_rect(center=self.rect.center)  # Corrected
            screen.blit(self.image, self.rect.topleft)
            self.lifted = True


    def drop(self):
        if self.lifted:
            self.image = pygame.transform.scale(self.image, (STRAIGHT_DISTANCE, STRAIGHT_DISTANCE))
            self.rect = self.image.get_rect(center=self.rect.center)
            self.lifted = False

    def show_options(self, c_check = False):
        squares_to_return = []
        king = False

        def show_pawn_moves(color):
            move_direction = 1 if color else -1  # 1 for white, -1 for black

            # Single square forward move
            forward_square = f"{self.letter}{int(self.number) + move_direction}"
            first_square_free = False  # Flag to track if the first square is free

            for sq in squares:
                if sq.name == forward_square and not sq.occupied:
                    sq.show()
                    squares_to_return.append(sq)
                    first_square_free = True  # First square is free to move

            # Two squares forward move, only allowed if the first square is free and pawn hasn't moved yet
            if self.number_of_moves == 0 and first_square_free:
                two_square_forward = f"{self.letter}{int(self.number) + 2 * move_direction}"
                for sq in squares:
                    if sq.name == two_square_forward and not sq.occupied:
                        sq.show()
                        squares_to_return.append(sq)

            # Diagonal captures (left and right)
            left_diagonal = f"{chr(ord(self.letter) - 1)}{int(self.number) + move_direction}"
            right_diagonal = f"{chr(ord(self.letter) + 1)}{int(self.number) + move_direction}"

            for sq in squares:
                # Left diagonal capture
                if sq.name == left_diagonal and sq.occupied and sq.occupied_by_color != self.color:
                    sq.show()
                    squares_to_return.append(sq)
                
                # Right diagonal capture
                if sq.name == right_diagonal and sq.occupied and sq.occupied_by_color != self.color:
                    sq.show()
                    squares_to_return.append(sq)
        def show_rook_moves():
                


                forward_sqs = []
                backward_sqs = []
                left_sqs = []
                right_sqs = []
               

                # Collect squares in each direction
                for sq in squares:
                    if sq.letter == self.letter and int(sq.number) > int(self.number):
                        forward_sqs.append(sq)
                    elif sq.letter == self.letter and int(sq.number) < int(self.number):
                        backward_sqs.append(sq)
                    elif sq.number == self.number and ord(sq.letter) < ord(self.letter):
                        left_sqs.append(sq)
                    elif sq.number == self.number and ord(sq.letter) > ord(self.letter):
                        right_sqs.append(sq)


                # Sort squares in each direction based on proximity
                forward_sqs = sorted(forward_sqs, key=lambda sq: sq.number)
                backward_sqs = sorted(backward_sqs, key=lambda sq: sq.number, reverse=True)
                left_sqs = sorted(left_sqs, key=lambda sq: sq.letter, reverse=True)  # Left goes from higher to lower letter (reverse=True)
                right_sqs = sorted(right_sqs, key=lambda sq: sq.letter)  # Right goes from lower to higher letter

                

                # Function to display possible moves in a line until blocked

                def see_line(sq_list):
                    for sq in sq_list:
                        if king == True and sq.occupied_by_color != self.color:
                            squares_to_return.append(sq)
                            break
                        if sq.occupied:
                                if sq.occupied_by_color != self.color:
                                    sq.show()  # Show the square as a valid move
                                    squares_to_return.append(sq)  # Capture opponent piece
                                break  # Stop after first occupied square (either capture or block)
                        else:
                            sq.show()  # Show the square as a valid move
                            squares_to_return.append(sq)

                # Check all directions
                see_line(forward_sqs)
                see_line(backward_sqs)
                see_line(left_sqs)
                see_line(right_sqs)
                return squares_to_return
            
        def show_bishop_moves():
            diagonals = {
                "top_right": [],
                "top_left": [],
                "bottom_right": [],
                "bottom_left": []
            }
                
            for sq in squares:
                # Calculate diagonal direction: top-right, top-left, bottom-right, bottom-left
                letter_diff = ord(sq.letter) - ord(self.letter)
                number_diff = sq.number - self.number

                if letter_diff == number_diff > 0:  # Top-right diagonal
                    diagonals["top_right"].append(sq)
                elif letter_diff == number_diff < 0:  # Bottom-left diagonal
                    diagonals["bottom_left"].append(sq)
                elif letter_diff == -number_diff > 0:  # Top-left diagonal
                    diagonals["top_left"].append(sq)
                elif letter_diff == -number_diff < 0:  # Bottom-right diagonal
                    diagonals["bottom_right"].append(sq)

            # Sort the squares by proximity to the bishop
            for direction in diagonals:
                diagonals[direction] = sorted(diagonals[direction], key=lambda sq: abs(sq.number - self.number))

            # Function to display possible moves in a diagonal line until blocked

            def see_diagonal(sq_list):
                for sq in sq_list:
                    if king == True and sq.occupied_by_color != self.color:
                        squares_to_return.append(sq)
                        break
                    if sq.occupied:
                        if sq.occupied_by_color != self.color:
                            sq.show()  # Show the square as a valid move (to capture)
                            squares_to_return.append(sq)
                        break  # Stop after encountering the first occupied square
                    else:
                        sq.show()  # Show the square as a valid move
                        squares_to_return.append(sq)

            # Check all diagonals
            for direction in diagonals:
                see_diagonal(diagonals[direction])

            return squares_to_return
        def show_knight_moves():
            for sq in squares:
                letter_diff = ord(sq.letter) - ord(self.letter)
                number_diff = sq.number - self.number
            
                if (number_diff == 2 and abs(letter_diff) == 1) or (number_diff == -2 and abs(letter_diff) == 1):
                        if sq.occupied_by_color != self.color:
                           squares_to_return.append(sq)

                if (letter_diff == 2 and abs(number_diff) == 1) or (letter_diff == -2 and abs(number_diff) == 1):
                    if sq.occupied_by_color != self.color:
                        squares_to_return.append(sq)
        def show_castling_moves():
            # Initialize the castling flags
            king_side_castle = False
            queen_side_castle = False
            sq_between_rook1 = []
            sq_between_rook = []
            nonlocal squares_to_return

            def not_moved(king, rook, rook1):
                """Check if the king and rooks haven't moved."""
                nonlocal king_side_castle, queen_side_castle  # Access the outer variables
                if king.number_of_moves == 0:
                    if rook.number_of_moves == 0:
                        king_side_castle = True
                    if rook1.number_of_moves == 0:
                        queen_side_castle = True
                
                if queen_side_castle or king_side_castle:
                    return True
                return False

            def path_clear(king_letter, rook_letter, rook1_letter):
                """Check if the path between king and rook is clear for castling."""
                nonlocal king_side_castle, queen_side_castle  # Access the outer variables
              

                # Iterate through squares to check if the path is blocked
                for sq in squares:
                    # Checking path for king-side castling (right side)
                    if ord(king_letter) < ord(rook_letter) and king_side_castle:
                        if ord(sq.letter) in range(ord(king_letter) + 1, ord(rook_letter)) and sq.number == self.number:
                            if not sq.occupied:
                                sq_between_rook.append(sq)
                      
                            else:
                                king_side_castle = False  # Set flag to False if any square is occupied
                       
                                break  # No need to check further if path is blocked
                for sq in squares:
                    # Checking path for queen-side castling (left side)
                    if ord(rook1_letter) < ord(king_letter) and queen_side_castle:
                        if ord(sq.letter) in range(ord(rook1_letter) + 1, ord(king_letter)) and sq.number == self.number:
                            if not sq.occupied:
                                sq_between_rook1.append(sq)
                            
                            else:
                                queen_side_castle = False  # Set flag to False if any square is occupied

                                break  # No need to check further if path is blocked

                # Return True only if both castling options are blocked
                if not queen_side_castle and not king_side_castle:
                    return False
                return True


            def not_attacked():
                """Check if the squares between the king and rook are under attack for castling."""
                nonlocal king_side_castle, queen_side_castle  # Access the outer variables

                # Helper function to check if any squares are attacked
                def is_square_attacked(squares_to_check):
                    for sq in squares_to_check:
                        for piece in pieces_on_board.values():
                            if piece.color != self.color:  # Only check opponent's pieces
                                possible_moves = piece.show_options(c_check= True)  # Get the piece's possible moves
                                if sq in possible_moves:
                                    print(f"Square {sq.name} is under attack by {piece.type} at {piece.square.name}")
                                    return True  # Square is under attack
                    return False  # No square in the path is under attack

                # Check for king-side castling
                if king_side_castle:
                    print("Checking king-side castling")
                    if is_square_attacked(sq_between_rook):  # Check if any of the squares between the king and the rook are attacked
                        king_side_castle = False
                        print("King-side castling not possible due to attack on the path")

                # Check for queen-side castling
                if queen_side_castle:
                    print("Checking queen-side castling")
                    if is_square_attacked(sq_between_rook1):  # Check if any of the squares between the king and the rook1 are attacked
                        queen_side_castle = False
                        print("Queen-side castling not possible due to attack on the path")

                # Return True if either castling option is still valid
                return king_side_castle or queen_side_castle


            # Determine rook positions based on king's color
            if self.color == True:
                color = "White"
                rook_pos = "h1"
                rook1_pos = "a1"
            else:
                color = "Black"
                rook_pos = "h8"
                rook1_pos = "a8"


            # Find the rooks
            rook = next((piece for piece in pieces_on_board.values() if piece.name == f"{color} Rook {rook_pos}"), None)
            rook1 = next((piece for piece in pieces_on_board.values() if piece.name == f"{color} Rook {rook1_pos}"), None)
            
            # Check if the king and rook haven't moved and the path is clear
            print("Start_____________________________________________________________")
            if self.in_check == False:
                if not_moved(self, rook, rook1):# works cathes if has moved
                    print("hasn't moved")
                    if path_clear(self.letter, rook_letter=rook.letter, rook1_letter=rook1.letter):
                        print("Path is clear")
                        if not_attacked():
                            print("Not under attack")
    
                            if king_side_castle:
                                # Add the king's destination square for king-side castling
                                if self.color == True:
                                    king_dest_square_k  = "g1"
                                else:
                                    king_dest_square_k = "g8"
                            
                            if queen_side_castle:
                                # Add the king's destination square for queen-side castling
                                if self.color == True:
                                    king_dest_square_q  = "c1"
                                else:
                                    king_dest_square_q = "c8"
                            
                            for sq in squares:
                                if queen_side_castle:
                                    if sq.name == king_dest_square_q:
                                        squares_to_return.append(sq)
                                
                                if king_side_castle:
                                    if sq.name == king_dest_square_k:
                                        squares_to_return.append(sq)
                                    

                    
        if self.type == "pawn":
            show_pawn_moves(self.color)
        if self.type == "rook": 
            king = False
            show_rook_moves()
        if self.type == "bishop":
         king = False
         show_bishop_moves()
        if self.type =="queen":
            king = False
            show_rook_moves()
            show_bishop_moves()
        if self.type == "king":
            king = True
            show_rook_moves()
            show_bishop_moves()
            if c_check == False:
             show_castling_moves()
            print("final squares")
            priner(squares_to_return)
        if self.type == "knight":
            show_knight_moves()
        return squares_to_return
        
# Create squares
def create_squares():
    squares = []
    for row in range(8):
        for col in range(8):
            square_name = f"{chr(97 + col)}{8 - row}"  # Naming like 'a8', 'b8', ..., 'h1'
            x_start = EDGE + col * STRAIGHT_DISTANCE
            x_end = x_start + STRAIGHT_DISTANCE
            y_start = row * STRAIGHT_DISTANCE
            y_end = y_start + STRAIGHT_DISTANCE  
            piece_pos = (x_start + (x_end - x_start)/2, y_start + (y_end - y_start)/2 )
            occupied = False

            Show_move_position_x = x_start + ((x_end - x_start) / 2)  # Corrected X calculation
            Show_move_position_y = y_start + ((y_end - y_start) / 2)  # Corrected Y calculation

            square = Square(square_name, [x_start, x_end], [y_start, y_end], occupied, Show_move_position_x, Show_move_position_y, letter=f'{chr(97+ col)}', number=int(8-row), piece_pos = piece_pos)
            squares.append(square)
    return squares
def create_pieces():
    piece_order = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
    pieces_on_board = {}

    for i, piece in enumerate(piece_order):
        # White pieces (bottom side)
        pieces_on_board[f"{chr(97 + i)}_wp"] = Piece(
            name=f"White Pawn {chr(97 + i)}2",  # Adding the name
            image_path=pieces[f"white_pawn"],
            scale_size=(STRAIGHT_DISTANCE, STRAIGHT_DISTANCE),
            type="pawn",
            letter=f"{chr(97 + i)}",
            number="2",
            color=True
        )
        pieces_on_board[f"{chr(97 + i)}_w{piece[0]}"] = Piece(
            name=f"White {piece.capitalize()} {chr(97 + i)}1",  # Adding the name
            image_path=pieces[f"white_{piece}"],
            scale_size=(STRAIGHT_DISTANCE, STRAIGHT_DISTANCE),
            type=piece,
            letter=f"{chr(97 + i)}",
            number="1",
            color=True
        )

        # Black pieces (top side)
        pieces_on_board[f"{chr(97 + i)}_bp"] = Piece(
            name=f"Black Pawn {chr(97 + i)}7",  # Adding the name
            image_path=pieces[f"black_pawn"],
            scale_size=(STRAIGHT_DISTANCE, STRAIGHT_DISTANCE),
            type="pawn",
            letter=f"{chr(97 + i)}",
            number="7",
            color=False
        )
        pieces_on_board[f"{chr(97 + i)}_b{piece[0]}"] = Piece(
            name=f"Black {piece.capitalize()} {chr(97 + i)}8",  # Adding the name
            image_path=pieces[f"black_{piece}"],
            scale_size=(STRAIGHT_DISTANCE, STRAIGHT_DISTANCE),
            type=piece,
            letter=f"{chr(97 + i)}",
            number="8",
            color=False
        )

    return pieces_on_board

def run(selected_board_num):
    
    if selected_board_num:
        if selected_board_num==1:
            background_image = pygame.image.load("pictures/actual/boards/classical board.png")
        elif selected_board_num ==2:
            background_image = pygame.image.load("pictures/actual/boards/blue board.png")
        elif selected_board_num ==3:
            background_image = pygame.image.load("pictures/actual/boards/black board.png")
    else:
        selected_board = pygame.image.load("pictures/actual/boards/classical board.png")
    sounds['game_start'].play()
    image_width, image_height = background_image.get_size()
    print(image_height, image_width)
    screen = pygame.display.set_mode((image_width, image_width))
    pygame.display.set_caption("Chess")
    global squares
    global rset
    squares = create_squares()
   
    global pieces_on_board
    pieces_on_board = create_pieces()
    global round_num
    round_num = 1
    squares_to_blit = []
    running = True
    lifted_piece = False
    print("printing at the start of run----------------------================")
    for sq in squares:
        print(sq)
    for piece in pieces_on_board:
      print(piece)


    while running:   
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
              if event.key == pygame.K_ESCAPE:
                  main_menu()
              if event.key == pygame.K_r:  # Check if the "R" key is pressed
                    round_num = 1
                    rset = False
                    print("round", round_num)
                    print("Game has been reset")
                    run(selected_board_num=selected_board__num)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if lifted_piece:
                    for sq in squares:
                        if sq in squares_to_blit:
                            if sq.hitbox.collidepoint(mouse):
                                pieces_on_board[piece_lifted].move(sq)
                                round_num +=1
                                if rset:
      
                                    rset = False
                                    print("round", round_num)
                                    print("Game has been reset")
                                    run()
                        if sq not in squares_to_blit and sq != pieces_on_board[piece_lifted].square:
                            for piece in pieces_on_board.values():
                                if sq.occupied_by_color != pieces_on_board[piece_lifted].color:
                                    if sq.hitbox.collidepoint(mouse):
                                            sounds['incorrect'].play()
                for piece in pieces_on_board.values():
                        if piece.lifted == True:
                            piece.drop()
                            squares_to_blit = []
                            lifted_piece = False
                        elif round_num % 2 != 0:
                            if piece.square.hitbox.collidepoint(mouse) and not lifted_piece and piece.color == True:
                                piece.lift()
                                squares_to_blit = piece.show_options()
                            #  for sq in squares_to_blit:
                            #     print(sq.name)

                                piece_lifted = next(key for key, value in pieces_on_board.items() if value == piece)
                                lifted_piece = True

                        elif round_num % 2 == 0:
                            if piece.square.hitbox.collidepoint(mouse) and not lifted_piece and piece.color == False:
                                piece.lift()
                                squares_to_blit = piece.show_options()
                                lifted_piece = True
                                piece_lifted = next(key for key, value in pieces_on_board.items() if value == piece)
        screen.blit(background_image, (0,0))

        #for sq in squares:
        #    # Assuming 'sq' has a 'hitbox' attribute with the position and size (a pygame.Rect)
        #    # Draw a red outline (not a filled box) around the hitbox
        #    pygame.draw.rect(screen, (255, 0, 0), sq.hitbox, 2)  # 2 is the thickness of the border\
        #    pygame.draw.circle(screen, (0, 0, 255), sq.piece_pos, 10)  # Draw a blue circle with radius 10 at piece_pos

        for piece in pieces_on_board.values():
            if piece.in_check == True:
                create_red_overlay(piece.square)


        for sq in squares_to_blit:
            sq.show()
        
            


        for piece in pieces_on_board.values():
            piece.spawn()
        pygame.display.update()
   
    pygame.quit()



global selected_board
selected_board = None
global selected_board__num
selected_board__num = 1
def main_menu():
    BG = pygame.image.load("pictures/actual/chess_bg.png")
    class Button():
        def __init__(self, image, pos, text_input, font, base_color, hovering_color):
            self.image = image
            self.x_pos = pos[0]
            self.y_pos = pos[1]
            self.font = font
            self.base_color, self.hovering_color = base_color, hovering_color
            self.text_input = text_input
            self.text = self.font.render(self.text_input, True, self.base_color)
            if self.image is None:
                self.image = self.text
            self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
            self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

        def update(self, screen):
            if self.image is not None:
                screen.blit(self.image, self.rect)
            screen.blit(self.text, self.text_rect)

        def checkForInput(self, position):
            if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
                return True
            return False

        def changeColor(self, position):
            if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
                self.text = self.font.render(self.text_input, True, self.hovering_color)
            else:
                self.text = self.font.render(self.text_input, True, self.base_color)
    def get_font(size):
        """
        This function loads a .ttf font file and returns a font object with the specified size.
        """
        return pygame.font.Font("pictures/actual/font.ttf", size)
    def options():
        global selected_board
        global selected_board__num
        # Load and scale down the board images
        main_board = pygame.image.load("pictures/actual/boards/classical board crop.png")
        main_board = pygame.transform.scale(main_board, (400, 400))
        
        board2 = pygame.image.load("pictures/actual/boards/blue board crop.png")
        board2 = pygame.transform.scale(board2, (400, 400))
        
        board3 = pygame.image.load("pictures/actual/boards/black board crop.png")
        board3 = pygame.transform.scale(board3, (400, 400))

        # Define positions for the pictures
        main_board_pos = (screen_width / 4, screen_height / 2)
        board2_pos = (screen_width / 2, screen_height / 2)
        board3_pos = (screen_width * 3 / 4, screen_height / 2)

        # Define rectangles for the pictures (for interaction)
        main_rect = main_board.get_rect(center=main_board_pos)
        board2_rect = board2.get_rect(center=board2_pos)
        board3_rect = board3.get_rect(center=board3_pos)
        if selected_board__num == 1:
            selected_board = main_rect

        while True:
            OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

            screen.fill("white")

            OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "Black")
            OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(screen_width / 2, screen_height / 2 - button_width - 100))
            screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

            # Display the board images
            screen.blit(main_board, main_rect)
            screen.blit(board2, board2_rect)
            screen.blit(board3, board3_rect)

            # Draw black outlines for all boards
            pygame.draw.rect(screen, "Black", main_rect, 5)
            pygame.draw.rect(screen, "Black", board2_rect, 5)
            pygame.draw.rect(screen, "Black", board3_rect, 5)

            # Highlight the selected board in green
            if selected_board:
                pygame.draw.rect(screen, "Green", selected_board, 5)

            # Highlight picture if hovering over it
            if main_rect.collidepoint(OPTIONS_MOUSE_POS):
                pygame.draw.rect(screen, "Green", main_rect, 5)
            if board2_rect.collidepoint(OPTIONS_MOUSE_POS):
                pygame.draw.rect(screen, "Green", board2_rect, 5)
            if board3_rect.collidepoint(OPTIONS_MOUSE_POS):
                pygame.draw.rect(screen, "Green", board3_rect, 5)

            # Back button
            OPTIONS_BACK = Button(image=None, pos=(screen_width / 2, screen_height / 2 + 400),
                                text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

            OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
            OPTIONS_BACK.update(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if main_rect.collidepoint(OPTIONS_MOUSE_POS):
                        selected_board = main_rect
                        selected_board__num = 1
                        print("Selected Classical Board")
                    elif board2_rect.collidepoint(OPTIONS_MOUSE_POS):
                        selected_board = board2_rect
                        selected_board__num = 2
                        print("Selected Blue Board")
                    elif board3_rect.collidepoint(OPTIONS_MOUSE_POS):
                        selected_board = board3_rect
                        selected_board__num = 3 
                        print("Selected Black Board")
                    if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                        main_menu()

            pygame.display.update()
    while True:
        screen.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()
                 # Calculate button positions based on screen width and height
        button_width = 250  
        button_height = 220


        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(screen_width / 2,  button_width))

       
        PLAY_BUTTON = Button(
            image=pygame.image.load("pictures/actual/Play Rect.png"), 
            pos=(screen_width / 2, button_height * 2),
            text_input="PLAY", 
            font=get_font(75), 
            base_color="#d7fcd4", 
            hovering_color="White"
        )

        OPTIONS_BUTTON = Button(
            image=pygame.image.load("pictures/actual/Options Rect.png"), 
            pos=(screen_width / 2, button_height * 3),
            text_input="OPTIONS", 
            font=get_font(75), 
            base_color="#d7fcd4", 
            hovering_color="White"
        )

        QUIT_BUTTON = Button(
            image=pygame.image.load("pictures/actual/Quit Rect.png"), 
            pos=(screen_width / 2, button_height * 4),
            text_input="QUIT", 
            font=get_font(75), 
            base_color="#d7fcd4", 
            hovering_color="White"
        )


        screen.blit(MENU_TEXT, MENU_RECT)
        
        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    run(selected_board_num=selected_board__num)
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
main_menu()

