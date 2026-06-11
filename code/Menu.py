import pygame
import sys
from game_state import GameState
import main

# Initialize GameState
Gm = GameState()

def main_menu():
    BG = pygame.image.load("pictures/actual/chess_bg.png")
    
    class Button:
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
            return self.rect.collidepoint(position)

        def changeColor(self, position):
            color = self.hovering_color if self.rect.collidepoint(position) else self.base_color
            self.text = self.font.render(self.text_input, True, color)

        def draw_hover_outline(self, screen, position):
            if self.rect.collidepoint(position):
                pygame.draw.rect(screen, "#d7fcd4", self.rect.inflate(18, 14), 4, border_radius=6)
    
    def get_font(size):
        """Load font with the specified size."""
        return pygame.font.Font("pictures/actual/font.ttf", size)

    def draw_title(text, y):
        shadow = get_font(100).render(text, True, "#17322b")
        shadow_rect = shadow.get_rect(center=(Gm.image_width / 2 + 6, y + 6))
        Gm.screen.blit(shadow, shadow_rect)
        title = get_font(100).render(text, True, "#b68f40")
        title_rect = title.get_rect(center=(Gm.image_width / 2, y))
        Gm.screen.blit(title, title_rect)

    def mode_menu():
        while True:
            MODE_MOUSE_POS = pygame.mouse.get_pos()

            Gm.screen.blit(BG, (0, 0))
            overlay = pygame.Surface((780, 560), pygame.SRCALPHA)
            overlay.fill((13, 34, 30, 150))
            Gm.screen.blit(overlay, overlay.get_rect(center=(Gm.image_width / 2, Gm.image_height / 2)))

            draw_title("PLAY", 230)

            SINGLEPLAYER_BUTTON = Button(
                image=pygame.image.load("pictures/actual/Options Rect.png"),
                pos=(Gm.image_width / 2, 410),
                text_input="SINGLEPLAYER",
                font=get_font(44),
                base_color="#d7fcd4",
                hovering_color="White"
            )

            MULTIPLAYER_BUTTON = Button(
                image=pygame.image.load("pictures/actual/Options Rect.png"),
                pos=(Gm.image_width / 2, 560),
                text_input="MULTIPLAYER",
                font=get_font(44),
                base_color="#d7fcd4",
                hovering_color="White"
            )

            BACK_BUTTON = Button(
                image=pygame.image.load("pictures/actual/Quit Rect.png"),
                pos=(Gm.image_width / 2, 710),
                text_input="BACK",
                font=get_font(60),
                base_color="#d7fcd4",
                hovering_color="White"
            )

            for button in [SINGLEPLAYER_BUTTON, MULTIPLAYER_BUTTON, BACK_BUTTON]:
                button.draw_hover_outline(Gm.screen, MODE_MOUSE_POS)
                button.changeColor(MODE_MOUSE_POS)
                button.update(Gm.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if SINGLEPLAYER_BUTTON.checkForInput(MODE_MOUSE_POS):
                        main.run(selected_board_num=Gm.selected_board__num)
                        Gm.screen = pygame.display.get_surface()
                    if MULTIPLAYER_BUTTON.checkForInput(MODE_MOUSE_POS):
                        main.run_multiplayer(selected_board_num=Gm.selected_board__num)
                        Gm.screen = pygame.display.get_surface()
                    if BACK_BUTTON.checkForInput(MODE_MOUSE_POS):
                        return

            pygame.display.update()
    
    def options():
        # Load and scale down the board images
        main_board = pygame.image.load("pictures/actual/boards/classical board crop.png")
        main_board = pygame.transform.scale(main_board, (400, 400))
        
        board2 = pygame.image.load("pictures/actual/boards/blue board crop.png")
        board2 = pygame.transform.scale(board2, (400, 400))
        
        board3 = pygame.image.load("pictures/actual/boards/black board crop.png")
        board3 = pygame.transform.scale(board3, (400, 400))

        # Define positions for the pictures
        main_board_pos = (Gm.image_width / 4, Gm.image_height / 2)
        board2_pos = (Gm.image_width / 2, Gm.image_height / 2)
        board3_pos = (Gm.image_width * 3 / 4, Gm.image_height / 2)

        # Define rectangles for the pictures (for interaction)
        main_rect = main_board.get_rect(center=main_board_pos)
        board2_rect = board2.get_rect(center=board2_pos)
        board3_rect = board3.get_rect(center=board3_pos)
        
        if Gm.selected_board__num == 1:
            Gm.selected_board = main_rect

        while True:
            OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

            Gm.screen.fill("white")

            OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "Black")
            OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(Gm.image_width / 2, Gm.image_height / 2 - 250))
            Gm.screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

            # Display the board images
            Gm.screen.blit(main_board, main_rect)
            Gm.screen.blit(board2, board2_rect)
            Gm.screen.blit(board3, board3_rect)

            # Draw black outlines for all boards
            pygame.draw.rect(Gm.screen, "Black", main_rect, 5)
            pygame.draw.rect(Gm.screen, "Black", board2_rect, 5)
            pygame.draw.rect(Gm.screen, "Black", board3_rect, 5)

            # Highlight the selected board in green
            if Gm.selected_board:
                pygame.draw.rect(Gm.screen, "Green", Gm.selected_board, 5)

            # Highlight picture if hovering over it
            if main_rect.collidepoint(OPTIONS_MOUSE_POS):
                pygame.draw.rect(Gm.screen, "Green", main_rect, 5)
            if board2_rect.collidepoint(OPTIONS_MOUSE_POS):
                pygame.draw.rect(Gm.screen, "Green", board2_rect, 5)
            if board3_rect.collidepoint(OPTIONS_MOUSE_POS):
                pygame.draw.rect(Gm.screen, "Green", board3_rect, 5)

            # Back button
            OPTIONS_BACK = Button(image=None, pos=(Gm.image_width / 2, Gm.image_height / 2 + 400),
                                  text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

            OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
            OPTIONS_BACK.update(Gm.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if main_rect.collidepoint(OPTIONS_MOUSE_POS):
                        Gm.selected_board = main_rect
                        Gm.selected_board__num = 1
                        print("Selected Classical Board")
                    elif board2_rect.collidepoint(OPTIONS_MOUSE_POS):
                        Gm.selected_board = board2_rect
                        Gm.selected_board__num = 2
                        print("Selected Blue Board")
                    elif board3_rect.collidepoint(OPTIONS_MOUSE_POS):
                        Gm.selected_board = board3_rect
                        Gm.selected_board__num = 3 
                        print("Selected Black Board")
                    if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                        main_menu()

            pygame.display.update()

    while True:
        Gm.screen.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()
        button_width = 250  
        button_height = 220

        PLAY_BUTTON = Button(
            image=pygame.image.load("pictures/actual/Play Rect.png"), 
            pos=(Gm.image_width / 2, button_height * 2),
            text_input="PLAY", 
            font=get_font(75), 
            base_color="#d7fcd4", 
            hovering_color="White"
        )

        OPTIONS_BUTTON = Button(
            image=pygame.image.load("pictures/actual/Options Rect.png"), 
            pos=(Gm.image_width / 2, button_height * 3),
            text_input="OPTIONS", 
            font=get_font(75), 
            base_color="#d7fcd4", 
            hovering_color="White"
        )

        QUIT_BUTTON = Button(
            image=pygame.image.load("pictures/actual/Quit Rect.png"), 
            pos=(Gm.image_width / 2, button_height * 4),
            text_input="QUIT", 
            font=get_font(75), 
            base_color="#d7fcd4", 
            hovering_color="White"
        )

        draw_title("MAIN MENU", button_width)
        
        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.draw_hover_outline(Gm.screen, MENU_MOUSE_POS)
            button.changeColor(MENU_MOUSE_POS)
            button.update(Gm.screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    mode_menu()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

if __name__ == "__main__":
    main_menu()
