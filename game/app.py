import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)

# Player attributes
player_width = 50
player_height = 50
player_x = screen_width // 2
player_y = screen_height - player_height
player_speed = 5

# Ball attributes
ball_radius = 20
ball_speed = 3  # Reduced speed
ball_spawn_time = 1500  # Increased time between ball spawns

# Bullet attributes
bullet_width = 5
bullet_height = 10
bullet_speed = 7

# Initialize screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Shooter Game")

# Clock
clock = pygame.time.Clock()

# Font
font = pygame.font.SysFont(None, 55)

# Initialize score and miss count
score = 0
miss_count = 0

# Ball and bullet lists
balls = []
bullets = []

# Function to display score
def display_score(score):
    text = font.render("Score: " + str(score), True, black)
    screen.blit(text, [10, 10])

# Function to display miss count
def display_miss_count(miss_count):
    text = font.render("Misses: " + str(miss_count), True, black)
    screen.blit(text, [10, 50])

# Function to display game over
def display_game_over():
    text = font.render("GAME OVER", True, red)
    screen.blit(text, [screen_width // 3, screen_height // 3])

# Main game loop
running = True
last_ball_spawn_time = pygame.time.get_ticks()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet_x = player_x + player_width // 2 - bullet_width // 2
                bullet_y = player_y
                bullets.append([bullet_x, bullet_y])

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < screen_width - player_width:
        player_x += player_speed

    # Ball spawning
    current_time = pygame.time.get_ticks()
    if current_time - last_ball_spawn_time > ball_spawn_time:
        ball_color = random.choice([red, yellow])
        ball_x = random.randint(0, screen_width - ball_radius * 2)
        ball_y = -ball_radius
        balls.append([ball_x, ball_y, ball_color])
        last_ball_spawn_time = current_time

    # Ball movement
    for ball in balls[:]:
        ball[1] += ball_speed  # Move the ball downwards

        if ball[1] > screen_height:
            if ball[2] == yellow:
                miss_count += 1
                if miss_count >= 3:
                    screen.fill(white)
                    display_game_over()
                    pygame.display.flip()
                    pygame.time.wait(3000)
                    running = False
                    break
            balls.remove(ball)

    # Bullet movement
    for bullet in bullets[:]:
        bullet[1] -= bullet_speed  # Move the bullet upwards
        if bullet[1] < 0:
            bullets.remove(bullet)

    # Collision detection
    for ball in balls[:]:
        ball_rect = pygame.Rect(ball[0], ball[1], ball_radius * 2, ball_radius * 2)
        for bullet in bullets[:]:
            bullet_rect = pygame.Rect(bullet[0], bullet[1], bullet_width, bullet_height)
            if ball_rect.colliderect(bullet_rect):
                if ball[2] == red:
                    score -= 1
                else:
                    score += 1
                balls.remove(ball)
                bullets.remove(bullet)
                break

    screen.fill(white)

    # Draw player
    pygame.draw.rect(screen, black, [player_x, player_y, player_width, player_height])

    # Draw balls
    for ball in balls:
        pygame.draw.circle(screen, ball[2], (ball[0] + ball_radius, ball[1] + ball_radius), ball_radius)

    # Draw bullets
    for bullet in bullets:
        pygame.draw.rect(screen, black, [bullet[0], bullet[1], bullet_width, bullet_height])

    # Display score and miss count
    display_score(score)
    display_miss_count(miss_count)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
