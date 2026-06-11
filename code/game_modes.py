import pygame
import sys


class ChessGame:
    def __init__(self, game_state, sound_manager, piece_module, board_module):
        self.gm = game_state
        self.sm = sound_manager
        self.piece_module = piece_module
        self.board_module = board_module
        self.background_image = None
        self.screen = None
        self.image_width = 0
        self.image_height = 0

    def load_board_image(self, selected_board_num):
        if selected_board_num == 1:
            return pygame.image.load("pictures/actual/boards/classical board.png")
        if selected_board_num == 2:
            return pygame.image.load("pictures/actual/boards/blue board.png")
        if selected_board_num == 3:
            return pygame.image.load("pictures/actual/boards/black board.png")
        return pygame.image.load("pictures/actual/boards/classical board.png")

    def setup_screen(self, selected_board_num, title):
        self.background_image = self.load_board_image(selected_board_num)
        self.image_width, self.image_height = self.background_image.get_size()
        self.screen = pygame.display.set_mode((self.image_width, self.image_height))
        pygame.display.set_caption(title)
        self.reset_game()

    def play_sound(self, sound_name):
        sound = self.sm.sounds.get(sound_name)
        if sound:
            sound.play()

    def reset_game(self):
        self.gm.screen = self.screen
        self.gm.set_game(piece=self.piece_module, board=self.board_module, Gm=self.gm, Sm=self.sm)
        self.play_sound("game_start")

    def drop_piece_after_move(self, piece_key):
        piece = self.gm.pieces_on_board.get(piece_key)
        if piece and piece.lifted:
            piece.drop()

    def clear_lifted_piece(self):
        for piece in self.gm.pieces_on_board.values():
            if piece.lifted:
                piece.drop()
        self.gm.lifted_piece = False
        self.gm.piece_lifted = None
        self.gm.squares_to_blit = []

    def draw_game(self):
        self.gm.screen.blit(self.background_image, (0, 0))

        for piece in self.gm.pieces_on_board.values():
            if piece.in_check:
                self.gm.create_red_overlay(piece.square)

        for sq in self.gm.squares_to_blit:
            sq.show()

        for piece in self.gm.pieces_on_board.values():
            piece.spawn()

    def finish_move(self, moved_piece_key):
        self.drop_piece_after_move(moved_piece_key)
        self.gm.round_num += 1
        self.gm.pieces_on_board = self.piece_module.pieces_on_board
        self.gm.lifted_piece = False
        self.gm.piece_lifted = None
        self.gm.squares_to_blit = []

    def click_selected_piece(self, mouse):
        moved_piece_key = self.gm.piece_lifted

        for sq in self.gm.squares:
            if sq in self.gm.squares_to_blit and sq.hitbox.collidepoint(mouse):
                self.gm.pieces_on_board[moved_piece_key].move(sq)
                self.finish_move(moved_piece_key)
                return True

            if sq not in self.gm.squares_to_blit and sq != self.gm.pieces_on_board[moved_piece_key].square:
                if sq.occupied_by_color != self.gm.pieces_on_board[moved_piece_key].color and sq.hitbox.collidepoint(mouse):
                    self.play_sound("incorrect")

        return False

    def select_piece(self, piece):
        piece.lift()
        self.gm.squares_to_blit = piece.show_options()
        self.gm.piece_lifted = next(
            key for key, value in self.gm.pieces_on_board.items() if value == piece
        )
        self.gm.lifted_piece = True

    def handle_quit(self):
        pygame.quit()
        sys.exit()


class SingleplayerGame(ChessGame):
    def run(self, selected_board_num):
        self.setup_screen(selected_board_num, "Chess")
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.handle_quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_r:
                        print("Game has been reset")
                        self.reset_game()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(pygame.mouse.get_pos())

            self.draw_game()
            pygame.display.update()

    def handle_click(self, mouse):
        if self.gm.lifted_piece and self.click_selected_piece(mouse):
            return

        for piece in self.gm.pieces_on_board.values():
            if piece.lifted:
                self.clear_lifted_piece()
                return

            if self.is_selectable_piece(piece, mouse):
                self.select_piece(piece)
                return

    def is_selectable_piece(self, piece, mouse):
        if self.gm.lifted_piece or not piece.square.hitbox.collidepoint(mouse):
            return False

        if self.gm.round_num % 2 != 0:
            return piece.color
        return not piece.color


class LocalMultiplayerGame(ChessGame):
    def run(self, selected_board_num):
        self.setup_screen(selected_board_num, "Chess - Multiplayer")
        self.clock_font = pygame.font.Font("pictures/actual/font.ttf", 34)
        self.small_font = pygame.font.Font("pictures/actual/font.ttf", 26)
        self.frame_clock = pygame.time.Clock()
        running = True

        while running:
            delta_seconds = self.frame_clock.tick(60) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.handle_quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_r:
                        print("Game has been reset")
                        self.reset_game()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = self.mouse_to_board_position(pygame.mouse.get_pos())
                    self.handle_click(mouse)

            self.update_clock(delta_seconds)
            self.draw_frame()

    def is_white_turn(self):
        return self.gm.round_num % 2 != 0

    def board_is_flipped(self):
        return not self.is_white_turn()

    def mouse_to_board_position(self, mouse_pos):
        if self.board_is_flipped():
            return self.image_width - mouse_pos[0], self.image_height - mouse_pos[1]
        return mouse_pos

    def handle_click(self, mouse):
        if self.gm.lifted_piece and self.click_selected_piece(mouse):
            return

        for piece in self.gm.pieces_on_board.values():
            if piece.lifted:
                self.clear_lifted_piece()
                return

            if self.is_selectable_piece(piece, mouse):
                self.select_piece(piece)
                return

    def is_selectable_piece(self, piece, mouse):
        if self.gm.lifted_piece or not piece.square.hitbox.collidepoint(mouse):
            return False

        if self.is_white_turn():
            return piece.color
        return not piece.color

    def format_clock(self, seconds):
        seconds = max(0, int(seconds))
        return f"{seconds // 60:02}:{seconds % 60:02}"

    def draw_clock_box(self, label, seconds, rect, active):
        color = (35, 115, 55) if active else (35, 35, 35)
        pygame.draw.rect(self.screen, color, rect, border_radius=6)
        pygame.draw.rect(self.screen, (235, 235, 235), rect, 2, border_radius=6)
        label_surface = self.small_font.render(label, True, (245, 245, 245))
        time_surface = self.clock_font.render(self.format_clock(seconds), True, (255, 255, 255))
        self.screen.blit(label_surface, (rect.x + 16, rect.y + 12))
        self.screen.blit(time_surface, (rect.x + 16, rect.y + 45))

    def mirrored_point(self, point):
        return self.image_width - point[0], self.image_height - point[1]

    def mirrored_rect(self, rect):
        return pygame.Rect(
            self.image_width - rect.right,
            self.image_height - rect.bottom,
            rect.width,
            rect.height,
        )

    def draw_flipped_red_overlay(self, square):
        inflated_hitbox = square.hitbox.inflate(square.hitbox.width * 0.1, square.hitbox.height * 0.1)
        rect_surface = pygame.Surface(inflated_hitbox.size)
        rect_surface.set_alpha(128)
        rect_surface.fill((255, 0, 0))
        self.screen.blit(rect_surface, self.mirrored_rect(inflated_hitbox).topleft)

    def draw_flipped_move_marker(self, square):
        image = pygame.image.load(self.gm.SHOW_MOVE)
        image = pygame.transform.scale(image, (int(image.get_width() * 0.2), int(image.get_height() * 0.2)))
        rect = image.get_rect(center=self.mirrored_point(square.circle_pos))
        self.screen.blit(image, rect.topleft)

    def draw_flipped_piece(self, piece):
        rotated_image = piece.image_for_board_orientation(flipped=True)
        rect = rotated_image.get_rect(center=self.mirrored_point(piece.rect.center))
        self.screen.blit(rotated_image, rect.topleft)

    def draw_flipped_game(self):
        self.screen.blit(pygame.transform.rotate(self.background_image, 180), (0, 0))

        for piece in self.gm.pieces_on_board.values():
            if piece.in_check:
                self.draw_flipped_red_overlay(piece.square)

        for sq in self.gm.squares_to_blit:
            self.draw_flipped_move_marker(sq)

        for piece in self.gm.pieces_on_board.values():
            self.draw_flipped_piece(piece)

    def draw_frame(self):
        if self.board_is_flipped():
            self.draw_flipped_game()
        else:
            self.gm.screen = self.screen
            self.draw_game()

        self.draw_clock_box("WHITE", self.gm.clock_times[True], pygame.Rect(38, 32, 190, 95), self.is_white_turn())
        self.draw_clock_box(
            "BLACK",
            self.gm.clock_times[False],
            pygame.Rect(self.image_width - 228, 32, 190, 95),
            not self.is_white_turn(),
        )
        pygame.display.update()

    def update_clock(self, delta_seconds):
        turn = self.is_white_turn()
        self.gm.clock_times[turn] -= delta_seconds
        if self.gm.clock_times[turn] <= 0:
            self.gm.clock_times[turn] = 0
            self.draw_frame()
            self.play_sound("game_end")
            self.gm.display_game_over(side_lost=turn)
            self.reset_game()
            self.frame_clock.tick(60)
