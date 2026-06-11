import pygame


class Player:
    def __init__(self, x, y, width, height, color, vel=5):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.vel = vel
        self.rect = pygame.Rect(x, y, width, height)  # Create a rectangle for the player
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
def redrawWindow(win, base_color):
    win.fill(base_color)  # Fill the window with the base color
    pygame.display.update()  # Update the display to show changes
def main():
    pygame.init()  # Initialize Pygame
    width, height = 500, 500  # Set the dimensions of the window
    win = pygame.display.set_mode((width, height))  # Create the window
    pygame.display.set_caption("Multiplayer Test")  # Set the window title

    run = True
    base_color = (0, 0, 0)  # Base color for the window
    clock = pygame.time.Clock()  # Create a clock to control the frame rate

    while run:
        clock.tick(60)  # Limit the frame rate to 60 FPS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False  # Exit the loop if the window is closed
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False  # Exit the loop if Escape is pressed

        redrawWindow(win, base_color)  # Redraw the window with the base color

    pygame.quit()  # Quit Pygame when done