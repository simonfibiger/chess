import pygame
import os
class GameState:
    def __init__(self):
        # Initialize pygame and load assets
        pygame.init()
        pygame.font.init()
        
        # Load background image and set screen dimensions
        self.background_image = pygame.image.load("pictures/actual/chess_bg.png")
        self.image_width, self.image_height = self.background_image.get_size()
        
        # Set up the display screen
        self.screen = pygame.display.set_mode((self.image_width, self.image_height))
        pygame.display.set_caption("Chess Game")

        # Game constants
        self.EDGE = 417
        self.STRAIGHT_DISTANCE = 135.5  # Distance between centers of squares
        self.BOARD_LEN = 1168
        self.LIFT_SCALE = self.STRAIGHT_DISTANCE * 1.3
        self.SHOW_MOVE = "pictures/actual/options.png"

        # Game fonts
        self.game_over_font = pygame.font.Font("pictures/actual/font.ttf", 40)
        
        # Game state variables
        self.round_num = 1
        self.selected_board = None
        self.selected_board__num = 1
        self.local_multiplayer = False
        self.clock_start_seconds = 5 * 60
        self.clock_times = {True: self.clock_start_seconds, False: self.clock_start_seconds}
        
        # Images for pieces
        self.pieces = self.load_piece_image()  # Call the function to load piece images

        
    

    def load_piece_image(self):
        # Define base path for piece images
        base_path = "pictures/actual/pieces"
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
        return pieces

    def create_red_overlay(self, square):
        """Draws a semi-transparent red overlay on the specified square."""
        inflated_hitbox = square.hitbox.inflate(square.hitbox.width * 0.1, square.hitbox.height * 0.1)
        rect_surface = pygame.Surface(inflated_hitbox.size)
        rect_surface.set_alpha(128)  # Set transparency to 50%
        rect_surface.fill((255, 0, 0))  # Fill with red
        self.screen.blit(rect_surface, inflated_hitbox.topleft)

    def set_game(self, piece, board, Gm, Sm):
        """Resets the game state for a new game."""
        self.lifted_piece = False 
        self.piece_lifted = None
        self.squares_to_blit = []
        self.piece = piece
        self.board = board
        self.gm = Gm
        self.sm = Sm

        self.board.Gm = self
        self.squares = self.board.create_squares()
        self.pieces_on_board = self.piece.create_pieces(self.squares, Gm=self.gm , Sm=self.sm)
        self.piece.pieces_on_board = self.gm.pieces_on_board
        self.round_num = 1
        self.clock_times = {True: self.clock_start_seconds, False: self.clock_start_seconds}
        

    def display_game_over(self, side_lost):
        """Displays game over text when a player loses."""
        game_over_text = "Game Over, White Lost!" if side_lost else "Game Over, Black Lost!"
        reset_text = "(press 'R' to reset)"
        
        # Render text surfaces
        text_surface = self.game_over_font.render(game_over_text, True, (255, 0, 0))
        reset_surface = self.game_over_font.render(reset_text, True, (0, 0, 0))
        
        # Position text on screen
        text_rect = text_surface.get_rect(center=(self.image_width // 2, self.image_height // 2))
        reset_rect = reset_surface.get_rect(center=(self.image_width // 2, self.image_height // 2 + 100))
        
        # Draw game over text and reset instructions
        self.screen.blit(text_surface, text_rect)
        self.screen.blit(reset_surface, reset_rect)
        # Wait for user to click or press 'R' to reset
        not_clicked = True
        while not_clicked:
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_r):
                    not_clicked = False
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                        print('Game reset from game over screen')
                        self.set_game(piece=self.piece, board=self.board, Gm = self.gm, Sm = self.sm)
                        self.round_num = 0

    def next_round(self):
        """Advances to the next round in the game."""
        self.round_num += 1
        print(f"Round: {self.round_num}")

    def is_white_turn(self):
        return self.round_num % 2 != 0
