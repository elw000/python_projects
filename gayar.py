import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1200, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ruler and Ball Game")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Load Adel Shakal Image
adil_shakal_image = pygame.image.load("gayar.jpg")  # Ensure the image is in the same folder
image_width, image_height = 80, 80  # Resize as needed
adil_shakal_image = pygame.transform.scale(adil_shakal_image, (image_width, image_height))

# Load sound effect
hit_sound = pygame.mixer.Sound("gayar_2.wav")  # Ensure the sound file is in the same folder

# Power-up settings
enlarged_paddle_duration = 5000  # 5 seconds

# Power-up types
POWERUP_EXTRA_BALL = "extra_ball"
POWERUP_LARGER_PADDLE = "larger_paddle"

def reset_game():
    global paddle, balls, blocks, power_ups, enlarged_paddle_timer, ball_released
    
    # Ruler (Paddle)
    paddle_width, paddle_height = 120, 10
    paddle = pygame.Rect(WIDTH//2 - paddle_width//2, HEIGHT - 50, paddle_width, paddle_height)
    
    # Balls
    ball_radius = 10
    balls = [
        {"rect": pygame.Rect(paddle.centerx - ball_radius, paddle.top - ball_radius * 2, ball_radius * 2, ball_radius * 2), "speed_x": 0, "speed_y": 0, "color": RED}
    ]
    
    # Generate image blocks
    blocks = []
    power_ups = []  # List to store falling power-ups
    enlarged_paddle_timer = 0
    ball_released = False  # Ball should not move until the paddle moves
    
    for row in range(5):
        for col in range(WIDTH // (image_width + 10)):
            x = col * (image_width + 10) + 10
            y = row * (image_height + 10) + 50
            blocks.append(pygame.Rect(x, y, image_width, image_height))
    
    return paddle, balls, blocks, power_ups

# Initialize game objects
paddle, balls, blocks, power_ups = reset_game()
clock = pygame.time.Clock()
running = True

while running:
    screen.fill(BLACK)
    current_time = pygame.time.get_ticks()
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Paddle movement
    keys = pygame.key.get_pressed()
    moved = False
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.move_ip(-6, 0)
        moved = True
    if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.move_ip(6, 0)
        moved = True
    
    # Release ball when paddle moves
    if moved and not ball_released:
        ball_released = True
        balls[0]["speed_x"] = 6
        balls[0]["speed_y"] = -6
    
    # Ball movement and collision detection
    for ball in balls[:]:
        if ball_released:
            ball["rect"].move_ip(ball["speed_x"], ball["speed_y"])
        else:
            ball["rect"].x = paddle.centerx - ball["rect"].width // 2
            ball["rect"].y = paddle.top - ball["rect"].height
        
        # Ball collision with walls
        if ball["rect"].left <= 0 or ball["rect"].right >= WIDTH:
            ball["speed_x"] *= -1
        if ball["rect"].top <= 0:
            ball["speed_y"] *= -1
        
        # Ball collision with paddle
        if ball["rect"].colliderect(paddle):
            ball["speed_y"] *= -1
        
        # Ball collision with image blocks
        for block in blocks[:]:
            if ball["rect"].colliderect(block):
                blocks.remove(block)
                ball["speed_y"] *= -1
                hit_sound.play()
                
                # Randomly drop a power-up
                if random.random() < 0.3:  # 30% chance of a power-up
                    power_up_type = random.choice([POWERUP_EXTRA_BALL, POWERUP_LARGER_PADDLE])
                    power_ups.append({"rect": pygame.Rect(block.x, block.y, 30, 30), "type": power_up_type})
                break
    
    # Move and process power-ups
    for power_up in power_ups[:]:
        power_up["rect"].move_ip(0, 3)  # Power-ups fall down
        if power_up["rect"].colliderect(paddle):
            if power_up["type"] == POWERUP_EXTRA_BALL:
                balls.append({"rect": pygame.Rect(WIDTH//2, HEIGHT//2, 20, 20), "speed_x": 6, "speed_y": -6, "color": RED})
            elif power_up["type"] == POWERUP_LARGER_PADDLE:
                paddle.width = 200
                enlarged_paddle_timer = current_time + enlarged_paddle_duration
            power_ups.remove(power_up)
        elif power_up["rect"].top > HEIGHT:
            power_ups.remove(power_up)
    
    # Reset paddle size after power-up duration ends
    if enlarged_paddle_timer and current_time > enlarged_paddle_timer:
        paddle.width = 120
        enlarged_paddle_timer = 0
    
    # Remove balls that fall off screen
    balls = [ball for ball in balls if ball["rect"].bottom < HEIGHT]
    
    # Ensure game continues if any ball is still in play
    if not balls:
        paddle, balls, blocks, power_ups = reset_game()
    
    # Draw elements
    pygame.draw.rect(screen, WHITE, paddle)
    for ball in balls:
        pygame.draw.ellipse(screen, ball["color"], ball["rect"])
    for block in blocks:
        screen.blit(adil_shakal_image, block.topleft)
    for power_up in power_ups:
        pygame.draw.polygon(screen, GREEN, [(power_up["rect"].x, power_up["rect"].y), (power_up["rect"].x + 30, power_up["rect"].y + 15), (power_up["rect"].x, power_up["rect"].y + 30), (power_up["rect"].x - 30, power_up["rect"].y + 15)])
    
    pygame.display.flip()
    clock.tick(65)

pygame.quit()
