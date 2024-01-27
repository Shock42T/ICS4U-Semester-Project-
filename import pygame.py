import pygame
import random

pygame.init()


# Load background image
background = pygame.image.load('background.jpg')

character_images = [
    pygame.image.load('R1.png'),
    pygame.image.load('R2.png'),
    pygame.image.load('R3.png'),
    pygame.image.load('R4.png'),
    pygame.image.load('R5.png'),
    pygame.image.load('R6.png'),
    pygame.image.load('R7.png'),
    pygame.image.load('R8.png'),
    pygame.image.load('R9.png')
]
obstacle_images = [
    pygame.image.load('L1E.png'),
    pygame.image.load('L2E.png'),
    pygame.image.load('L3E.png'),
    pygame.image.load('L4E.png'),
    pygame.image.load('L5E.png'),
    pygame.image.load('L6E.png'),
    pygame.image.load('L7E.png'),
    pygame.image.load('L8E.png'),
    pygame.image.load('L9E.png'),
    pygame.image.load('L10E.png'),
    pygame.image.load('L11E.png')
   
]
 
# Set window dimensions based on the background image size
WIDTH, HEIGHT = background.get_size()
WIDTH = 1000
HEIGHT = 554

player_x = 20
player_y = 20
y_change = 0
gravity = 1
x_change = 0
MAX_PLATFORMS = 10
obstacles = [300, 450, 600]
obstacle_speed = 2
platform_group_speed = 2
active = False
score = 0
character_frame = 0


platform_image = pygame.image.load('yellow_dot.jpg')

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(platform_image, (width, 10))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

def add_platform():
    p_w = random.randint(10, 10)
    p_x = WIDTH + random.randint(100, 100)  # Start the platform off-screen to the right
    p_y = random.randint(200, 400)  # Adjust the y-coordinate range as needed
    platform = Platform(p_x, p_y, p_w)
    platform_group.add(platform)

platform_group = pygame.sprite.Group()

for p in range(MAX_PLATFORMS):
    p_w = random.randint(10, 10)
    p_x = random.randint(10, WIDTH - p_w)
    p_y = random.randint(200, 400)  # Adjust the y-coordinate range as needed
    platform = Platform(p_x, p_y, p_w)
    platform_group.add(platform)

# create temporary platforms
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('endless runner')
fps = 60
font = pygame.font.Font('freesansbold.ttf', 16)
text_color = (0, 0, 0)
timer = pygame.time.Clock()

running = True
while running:
    timer.tick(fps)

    screen.blit(background, (0, 0))  # Draw background

    platform_group.draw(screen)

    screen.blit(character_images[character_frame], (player_x, player_y - character_images[character_frame].get_height()))

    character_frame = (character_frame + 1) % len(character_images)

    screen.blit(obstacle_images[character_frame], [obstacles[0], HEIGHT - 86])
    screen.blit(obstacle_images[character_frame], [obstacles[1], HEIGHT - 86])
    screen.blit(obstacle_images[character_frame], [obstacles[2], HEIGHT - 86])
   
    score_text = font.render(f"Score: {score}", True, text_color)
    screen.blit(score_text, (20, 20))

    if not active:
        # Draw "You died, press space to restart" message
            game_over_text = font.render("Press space to start/restart", True, text_color)
            screen.blit(game_over_text, (400, 40))
            title_text = font.render(f"Welcome to Endless Runner", True, text_color)
            screen.blit(title_text, (400, 20))
            pygame.display.flip()
   
        for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not active and not is_jumping:
                obstacles = [300, 450, 600]
                player_x = 50
                score = 0
                active = True
                y_change = 20  # Set a positive value for upward motion when space is pressed
                is_jumping = True
            if active:
                if event.key == pygame.K_SPACE and not is_jumping:
                    active = True
                    y_change = 22  # Set a positive value for upward motion when space is pressed
                    is_jumping = True
                if event.key == pygame.K_RIGHT:
                    x_change = 2
                if event.key == pygame.K_LEFT:
                    x_change = -2
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                x_change = 0

    for i in range(len(obstacles)):
        if active:
            obstacles[i] -= obstacle_speed
        if obstacles[i] < -20:
            obstacles[i] = random.randint(470, 520)
            score += 1

     # Increase difficulty based on the score
    obstacle_speed = 2 + 0.1 * score

     player_rect = pygame.Rect(player_x, player_y - character_images[character_frame].get_height(),
                              character_images[character_frame].get_width(), character_images[character_frame].get_height())
    player_rect = pygame.Rect(player_x, player_y - character_images[character_frame].get_height(),
                          4,30)  # Adjust the width and height as needed
   
    obstacle_rect_margin = 1 # Adjust the margin as needed
    obstacle_rects = [pygame.Rect(obstacle, HEIGHT - 60, 0, 0) for obstacle in obstacles]

    obstacle_rect0 = pygame.Rect(obstacles[0], HEIGHT - 60, 0, 0).inflate(-obstacle_rect_margin, -obstacle_rect_margin)
    obstacle_rect1 = pygame.Rect(obstacles[1], HEIGHT - 60, 0, 0).inflate(-obstacle_rect_margin, -obstacle_rect_margin)
    obstacle_rect2 = pygame.Rect(obstacles[2], HEIGHT - 60, 0, 0).inflate(-obstacle_rect_margin, -obstacle_rect_margin)
 
    for platform in platform_group:
     platform.rect.x -= platform_group_speed  # Move the platform to the left

    last_platform = platform_group.sprites()[-1]
    if last_platform.rect.right < WIDTH:
        add_platform()

    for obstacle_rect in obstacle_rects:
        obstacle_rect.width += 20
        obstacle_rect.y -= 24
        obstacle_rect.x += 16
        obstacle_rect.height += 40
       
    # Collision detection
    if player_rect.colliderect(obstacle_rect):
        active = False
 
    for platform in platform_group:
        if player_rect.colliderect(platform.rect):
            y_change = 5
            player_y = platform.rect.top - character_images[character_frame].get_height()
            is_jumping = False

     if player_rect.colliderect(obstacle_rect0) or player_rect.colliderect(obstacle_rect1) or player_rect.colliderect(obstacle_rect2):
        active = False
   
    player_rect = pygame.Rect(player_x, player_y, 20, 20)
    for obstacle_rect in obstacle_rects:
     if player_rect.colliderect(obstacle_rect):
        # Check if player is above the obstacle or head-on collision
        if player_rect.y < obstacle_rect.y:
            active = False
        else:
            # If the player is below the obstacle, stop jumping
            y_change = 0
            player_y = obstacle_rect.y + obstacle_rect.height

    if 0 <= player_x <= 430:
        player_x += x_change
    if player_x < 0:
        player_x = 0
    if player_x > 430:
        player_x = 430

    if y_change > 0 or player_y < HEIGHT - 25:
        player_y -= y_change
    y_change -= gravity
    if player_y > HEIGHT - 25:
        player_y = HEIGHT - 25
    if player_y == HEIGHT - 25 and y_change < 0:
        y_change = 0
        is_jumping = False

    pygame.display.flip()


pygame.quit()







