import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Set up display
WIDTH = 800
HEIGHT = 400
FULLSCREEN = False
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("T-Rex Runner")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BACKGROUND_COLOR = (200, 200, 200)

# Load T-Rex image
trex_image = pygame.image.load("mo.jpg")
trex_image = pygame.transform.scale(trex_image, (50, 60))  # Resize image

# Load sounds
point_sound = pygame.mixer.Sound("omar2_[cut_2sec].wav")
game_over_sound = pygame.mixer.Sound("omar_.wav")

# Game variables
GRAVITY = 0.8
JUMP_SPEED = -15
GROUND_HEIGHT = HEIGHT - 100
LAST_CACTUS_TIME = time.time()
CACTUS_MIN_INTERVAL = 2  # Minimum interval in seconds
CACTUS_SPEED = 5  # Initial speed

class TRex:
    def __init__(self):
        self.x = 50
        self.y = GROUND_HEIGHT
        self.width = 50
        self.height = 60
        self.vel_y = 0
        self.is_jumping = False
        
    def jump(self):
        if not self.is_jumping:
            self.vel_y = JUMP_SPEED
            self.is_jumping = True
            
    def update(self):
        self.vel_y += GRAVITY
        self.y += self.vel_y
        if self.y > GROUND_HEIGHT:
            self.y = GROUND_HEIGHT
            self.vel_y = 0
            self.is_jumping = False
            
    def draw(self):
        screen.blit(trex_image, (self.x, self.y))

class Cactus:
    def __init__(self, speed):
        self.x = WIDTH
        self.y = GROUND_HEIGHT + 10
        self.width = 20
        self.height = 50
        self.speed = speed
        
    def update(self):
        self.x -= self.speed
        
    def draw(self):
        pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height))
        
    def offscreen(self):
        return self.x < -self.width
        
    def collide(self, trex):
        return (self.x < trex.x + trex.width and 
                self.x + self.width > trex.x and
                self.y < trex.y + trex.height and
                self.y + self.height > trex.y)

def toggle_fullscreen():
    global FULLSCREEN, screen
    if FULLSCREEN:
        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    else:
        screen = pygame.display.set_mode((pygame.display.Info().current_w, pygame.display.Info().current_h), pygame.FULLSCREEN)
    FULLSCREEN = not FULLSCREEN

def main():
    global LAST_CACTUS_TIME, CACTUS_SPEED
    clock = pygame.time.Clock()
    trex = TRex()
    cacti = []
    score = 0
    game_over = False
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game_over:
                        trex = TRex()
                        cacti = []
                        score = 0
                        game_over = False
                        LAST_CACTUS_TIME = time.time()
                        CACTUS_SPEED = 5  # Reset speed
                    else:
                        trex.jump()
                if event.key == pygame.K_f:
                    toggle_fullscreen()
                        
        if not game_over:
            trex.update()
            current_time = time.time()
            if len(cacti) == 0 or (current_time - LAST_CACTUS_TIME) > CACTUS_MIN_INTERVAL + random.uniform(0, 2):
                cacti.append(Cactus(CACTUS_SPEED))
                LAST_CACTUS_TIME = current_time
            
            for cactus in cacti[:]:
                cactus.update()
                if cactus.offscreen():
                    cacti.remove(cactus)
                    score += 1
                    point_sound.play()
                    
                    # Increase speed at certain score milestones
                    if score % 10 == 0:
                        CACTUS_SPEED += 1
                        
                if cactus.collide(trex):
                    game_over = True
                    game_over_sound.play()
                    
        screen.fill(BACKGROUND_COLOR)
        pygame.draw.line(screen, BLACK, (0, GROUND_HEIGHT + 60), (WIDTH, GROUND_HEIGHT + 60))
        trex.draw()
        for cactus in cacti:
            cactus.draw()
            
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {score}', True, BLACK)
        screen.blit(score_text, (10, 10))
        
        if game_over:
            game_over_text = font.render('Game Over! Press SPACE to restart', True, BLACK)
            text_rect = game_over_text.get_rect(center=(WIDTH/2, HEIGHT/2))
            screen.blit(game_over_text, text_rect)
            
        pygame.display.flip()
        clock.tick(60)
        
    pygame.quit()

if __name__ == "__main__":
    main()
