import pygame
import sys
pygame.init()
# Access the GL instance to retrieve squares, if needed

# import sq_module
# squares = sq_module.sqrs


class Piece:
    def __init__(self, name, image_path, scale_size, type, number, letter, color, squares, Gamestate, Soundmanager):
        self.Gm = Gamestate
        self.Sm = Soundmanager
        self.name = name
        self.in_check = False
        self.checked_by = ""
        self.image_path = image_path
        self.scale_size = scale_size
        self.base_image = pygame.transform.scale(pygame.image.load(self.image_path), self.scale_size)
        self.flipped_base_image = pygame.transform.rotate(self.base_image, 180)
        self.lifted_image = pygame.transform.scale(
            self.base_image,
            (int(self.Gm.LIFT_SCALE), int(self.Gm.LIFT_SCALE))
        )
        self.flipped_lifted_image = pygame.transform.rotate(self.lifted_image, 180)
        self.image = self.base_image
        self.squares = squares
      
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
                        for piece in pieces_on_board.values():
                            piece.spawn()
                        self.Sm.sounds["game_end"].play()
                        self.Gm.display_game_over(side_lost=piece.color)
                        return False
                    else:
                        self.Sm.sounds["capture"].play()
      
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
                for sq in self.squares:
                    if sq.name == kingside_rook_new_square:
                        rook_new_square = sq  # Square for the rook in kingside castling
                for piece in pieces_on_board.values():
                    if piece.color == self.color and piece.square.name == kingside_rook_square:
                        rook = piece  # Identify the rook for castling
                        rook.move(rook_new_square)  # Move the rook to its new square
                        self.Sm.sounds["castle"].play()
     
              
                        break

            # Queenside castling (move king 2 squares to the left)
            elif ord(self.square.letter) - ord(new_square.letter) == 2:
                for sq in self.squares:
                    if sq.name == queenside_rook_new_square:
                        rook_new_square = sq  # Square for the rook in queenside castling
                for piece in pieces_on_board.values():
                    if piece.color == self.color and piece.square.name == queenside_rook_square:
                        rook = piece  # Identify the rook for castling
                        rook.move(rook_new_square)  # Move the rook to its new square
                        self.Sm.sounds["castle"].play()
          
                
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
                self.Sm.sounds["move_check"].play()
        
        else:
            if not_occ == True:
                  self.Sm.sounds["move_self"].play()

    def delete(self):
        for key in list(pieces_on_board.keys()):
            if pieces_on_board[key] == self:
                del pieces_on_board[key]
                break

    def spawn(self):
        self.Gm.screen.blit(self.image, self.rect.topleft)

    def image_for_board_orientation(self, flipped=False):
        if flipped:
            return self.flipped_lifted_image if self.lifted else self.flipped_base_image
        return self.lifted_image if self.lifted else self.base_image

    def lift(self):
        if not self.lifted:
            self.image = self.lifted_image
            self.rect = self.image.get_rect(center=self.rect.center)
            self.Gm.screen.blit(self.image, self.rect.topleft)
            self.lifted = True

    def drop(self):
        if self.lifted:
            self.image = self.base_image
            self.rect = self.image.get_rect(center=self.rect.center)
            self.lifted = False

    def show_options(self, c_check=False):
        squares_to_return = []
        king = False

        def show_square(sq):
            if not c_check:
                sq.show()
 
        def show_pawn_moves(color):
            move_direction = 1 if color else -1
            forward_square = f"{self.letter}{int(self.number) + move_direction}"
            first_square_free = False

            for sq in self.squares:
                if sq.name == forward_square and not sq.occupied:
                    show_square(sq)
                    squares_to_return.append(sq)
                    first_square_free = True

            if self.number_of_moves == 0 and first_square_free:
                two_square_forward = f"{self.letter}{int(self.number) + 2 * move_direction}"
                for sq in self.squares:
                    if sq.name == two_square_forward and not sq.occupied:
                        show_square(sq)
                        squares_to_return.append(sq)

            left_diagonal = f"{chr(ord(self.letter) - 1)}{int(self.number) + move_direction}"
            right_diagonal = f"{chr(ord(self.letter) + 1)}{int(self.number) + move_direction}"

            for sq in self.squares:
                if sq.name == left_diagonal and sq.occupied and sq.occupied_by_color != self.color:
                    show_square(sq)
                    squares_to_return.append(sq)
                if sq.name == right_diagonal and sq.occupied and sq.occupied_by_color != self.color:
                    show_square(sq)
                    squares_to_return.append(sq)
            return squares_to_return
        def show_rook_moves():
            forward_sqs, backward_sqs, left_sqs, right_sqs = [], [], [], []

            for sq in self.squares:
                if sq.letter == self.letter and int(sq.number) > int(self.number):
                    forward_sqs.append(sq)
                elif sq.letter == self.letter and int(sq.number) < int(self.number):
                    backward_sqs.append(sq)
                elif sq.number == self.number and ord(sq.letter) < ord(self.letter):
                    left_sqs.append(sq)
                elif sq.number == self.number and ord(sq.letter) > ord(self.letter):
                    right_sqs.append(sq)

            forward_sqs = sorted(forward_sqs, key=lambda sq: sq.number)
            backward_sqs = sorted(backward_sqs, key=lambda sq: sq.number, reverse=True)
            left_sqs = sorted(left_sqs, key=lambda sq: sq.letter, reverse=True)
            right_sqs = sorted(right_sqs, key=lambda sq: sq.letter)

            def see_line(sq_list):
                for sq in sq_list:
                    if king and sq.occupied_by_color != self.color:
                        squares_to_return.append(sq)
                        break
                    if sq.occupied:
                        if sq.occupied_by_color != self.color:
                            show_square(sq)
                            squares_to_return.append(sq)
                        break
                    else:
                        show_square(sq)
                        squares_to_return.append(sq)

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
                
            for sq in self.squares:
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
                            show_square(sq)  # Show the square as a valid move (to capture)
                            squares_to_return.append(sq)
                        break  # Stop after encountering the first occupied square
                    else:
                        show_square(sq)  # Show the square as a valid move
                        squares_to_return.append(sq)

            # Check all diagonals
            for direction in diagonals:
                see_diagonal(diagonals[direction])

            return squares_to_return
        def show_knight_moves():
            for sq in self.squares:
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
                    if rook and rook.number_of_moves == 0:
                        king_side_castle = True
                    if rook1 and rook1.number_of_moves == 0:
                        queen_side_castle = True
                
                if queen_side_castle or king_side_castle:
                    return True
                return False

            def path_clear(king_letter, rook_letter, rook1_letter):
                """Check if the path between king and rook is clear for castling."""
                nonlocal king_side_castle, queen_side_castle  # Access the outer variables
              

                # Iterate through squares to check if the path is blocked
                for sq in self.squares:
                    # Checking path for king-side castling (right side)
                    if ord(king_letter) < ord(rook_letter) and king_side_castle:
                        if ord(sq.letter) in range(ord(king_letter) + 1, ord(rook_letter)) and sq.number == self.number:
                            if not sq.occupied:
                                sq_between_rook.append(sq)
                      
                            else:
                                king_side_castle = False  # Set flag to False if any square is occupied
                       
                                break  # No need to check further if path is blocked
                for sq in self.squares:
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
            rook_letter = rook.letter if rook else self.letter
            rook1_letter = rook1.letter if rook1 else self.letter
            
            # Check if the king and rook haven't moved and the path is clear
            print("Start_____________________________________________________________")
            if self.in_check == False:
                if not_moved(self, rook, rook1):# works cathes if has moved
                    print("hasn't moved")
                    if path_clear(self.letter, rook_letter=rook_letter, rook1_letter=rook1_letter):
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
                            
                            for sq in self.squares:
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
            if not c_check:
                show_castling_moves()
        if self.type == "knight":
            show_knight_moves()
        return squares_to_return
def create_pieces(squares, Gm, Sm):
    piece_order = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
    pieces_on_board = {}

    for i, piece in enumerate(piece_order):
        # White pieces (bottom side)
        pieces_on_board[f"{chr(97 + i)}_wp"] = Piece(
            name=f"White Pawn {chr(97 + i)}2",
            image_path=Gm.pieces[f"white_pawn"],  # Access pieces from Gm
            scale_size=(Gm.STRAIGHT_DISTANCE, Gm.STRAIGHT_DISTANCE),
            type="pawn",
            letter=f"{chr(97 + i)}",
            number="2",
            color=True,
            squares=squares,
            Gamestate=Gm,
            Soundmanager=Sm
        )

        pieces_on_board[f"{chr(97 + i)}_w{piece[0]}"] = Piece(
            name=f"White {piece.capitalize()} {chr(97 + i)}1",
            image_path=Gm.pieces[f"white_{piece}"],  # Access pieces from Gm
            scale_size=(Gm.STRAIGHT_DISTANCE, Gm.STRAIGHT_DISTANCE),
            type=piece,
            letter=f"{chr(97 + i)}",
            number="1",
            color=True,
            squares=squares,
            Gamestate=Gm,
            Soundmanager=Sm
        )

        # Black pieces (top side)
        pieces_on_board[f"{chr(97 + i)}_bp"] = Piece(
            name=f"Black Pawn {chr(97 + i)}7",
            image_path=Gm.pieces[f"black_pawn"],  # Access pieces from Gm
            scale_size=(Gm.STRAIGHT_DISTANCE, Gm.STRAIGHT_DISTANCE),
            type="pawn",
            letter=f"{chr(97 + i)}",
            number="7",
            color=False,
            squares=squares,
            Gamestate=Gm,
            Soundmanager=Sm
            
        )
        pieces_on_board[f"{chr(97 + i)}_b{piece[0]}"] = Piece(
            name=f"Black {piece.capitalize()} {chr(97 + i)}8",
            image_path=Gm.pieces[f"black_{piece}"],  # Access pieces from Gm
            scale_size=(Gm.STRAIGHT_DISTANCE, Gm.STRAIGHT_DISTANCE),
            type=piece,
            letter=f"{chr(97 + i)}",
            number="8",
            color=False,
            squares=squares,
            Gamestate=Gm,
            Soundmanager=Sm
        )

    return pieces_on_board
