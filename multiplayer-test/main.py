import pygame
width = 500
height = 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Multiplayer Test")

clientNum = 0
class Player:
    def __init__(self, x, y, width, height, color, vel = 5):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.vel = vel
        self.rect = pygame.Rect(x,y,width,height)  # Create a rectangle for the player

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
    def move(self):
        keys = pygame.key.get_pressed()  # Update the state of all keys
        if keys[pygame.K_LEFT]:  # Move left
            self.x -= self.vel
        if keys[pygame.K_RIGHT]:  # Move right
            self.x += self.vel
        if keys[pygame.K_UP]:  # Move up
            self.y -= self.vel
        if keys[pygame.K_DOWN]:  # Move down
            self.y += self.vel
        if keys[pygame.K_SPACE]:  # Jump when space is pressed
            self.y -= self.vel * 2

        self.rect = (self.x, self.y, self.width, self.height)  # Update the rectangle position

def redrawWindow(win, player):

    win.fill((0,0,0))  # Fill the window with white color
    player.draw(win)  # Draw the player on the window
    pygame.display.update()

def main():
    run = True
    player = Player(50, 50, 100, 100, (0, 250, 0))  # Create a player instance
    clock = pygame.time.Clock()  # Create a clock to control the frame rate

    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False  # Exit the loop if the window is closed
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False  # Exit the loop if Escape is pressed
        player.move()
        redrawWindow(win, player)  # Redraw the window            

    pygame.quit()  # Quit Pygame when done 
main()  # Run the main function to start the game
# if __name__ == "__main__":