import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH = 800
HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

class Snake:
    def __init__(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.length = 1
        
    def get_head_position(self):
        return self.positions[0]
    
    def update(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = ((cur[0] + x) % GRID_WIDTH, (cur[1] + y) % GRID_HEIGHT)
        
        if new in self.positions[3:]:
            return False
            
        self.positions.insert(0, new)
        if len(self.positions) > self.length:
            self.positions.pop()
        return True
        
    def reset(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.length = 1

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.randomize_position()
        
    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH-1),
                        random.randint(0, GRID_HEIGHT-1))

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.snake.direction != (0, 1):
                    self.snake.direction = (0, -1)
                elif event.key == pygame.K_DOWN and self.snake.direction != (0, -1):
                    self.snake.direction = (0, 1)
                elif event.key == pygame.K_LEFT and self.snake.direction != (1, 0):
                    self.snake.direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and self.snake.direction != (-1, 0):
                    self.snake.direction = (1, 0)
        return True
        
    def update(self):
        if not self.snake.update():
            self.snake.reset()
            self.score = 0
            
        if self.snake.get_head_position() == self.food.position:
            self.snake.length += 1
            self.score += 1
            self.food.randomize_position()
            
    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw snake
        for pos in self.snake.positions:
            rect = pygame.Rect(pos[0]*GRID_SIZE, pos[1]*GRID_SIZE, GRID_SIZE-2, GRID_SIZE-2)
            pygame.draw.rect(self.screen, GREEN, rect)
            
        # Draw food
        rect = pygame.Rect(self.food.position[0]*GRID_SIZE, 
                          self.food.position[1]*GRID_SIZE, 
                          GRID_SIZE-2, GRID_SIZE-2)
        pygame.draw.rect(self.screen, RED, rect)
        
        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        pygame.display.update()
        
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(10)
            
if __name__ == '__main__':
    game = Game()
    game.run()
    pygame.quit()
