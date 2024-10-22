import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A NEW HOPE")


# BACKGROUND = (255, 150, 50)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
DARKRED = (139, 0, 0)
YELLOW = (255, 255, 0)
BORDER = pygame.Rect(445, 0, 4, 500)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Grenade+1.mp3"))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Gun+Silencer.mp3"))

HEALTH_FONT = pygame.font.SysFont("newsgothic", 30)
WINNER_FONT = pygame.font.SysFont("newsgothic", 38)

FPS = 60
VEL = 6

BULLET_VEL = 9
MAX_BULLETS = 5
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 65, 50

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2
# picture input
yellow_spaceship_image = pygame.image.load(
    os.path.join("Assets", "milfalcon.png"))
yellow_spaceship = pygame.transform.rotate(pygame.transform.scale(yellow_spaceship_image, (90, 75)), 25)

red_spaceship_image = pygame.image.load(
    os.path.join("Assets", "tiefighter.png"))
red_spaceship = pygame.transform.rotate(pygame.transform.scale(
    red_spaceship_image, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 180)

SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join("Assets", "space.png")), (WIDTH, HEIGHT))
# shown window
def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    #health bar
    red_health_text = HEALTH_FONT.render("HEALTH: " + str(red_health), 1, YELLOW)
    yellow_health_text = HEALTH_FONT.render("HEALTH: " + str(yellow_health), 1, YELLOW)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() -10, 10))
    WIN.blit(yellow_health_text, (10, 10))
    #spaceships
    WIN.blit(yellow_spaceship, (yellow.x, yellow.y))
    WIN.blit(red_spaceship, (red.x, red.y))
    #bullets
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()

# spaceship movement key settings
def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 1:  # LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x + 10:  # RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  # UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15:  # DOWN
        yellow.y += VEL


def red_handel_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + 5:  # LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL < 860:  # RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:  # UP
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL < HEIGHT - 55:  # DOWN
        red.y += VEL

# shooting options
def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)
def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, YELLOW)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    yellow_bullets = []
    red_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            # shooting
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height//2 + 20, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                    BULLET_HIT_SOUND.play()

                if event.key == pygame.K_BACKSPACE and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x, red.y + red.height // 2 - 4, 10, 5)
                    red_bullets.append(bullet)
                    bullet = pygame.Rect(
                        red.x, red.y + red.height // 2 + 12, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                    BULLET_HIT_SOUND.play()


            if event.type == RED_HIT:
                red_health -= 1

            if event.type == YELLOW_HIT:
                yellow_health -= 0.5
        winner_text = ""
        if red_health <= 0:
            winner_text = "THE FORCE IS STRONG WITH YOU!"

        if yellow_health <= 0:
            winner_text = "GALACTIC EMPIRE WINS!"

        if winner_text != "":
            draw_winner(winner_text)
            break


        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handel_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red,)

        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

    main()

if __name__ == "__main__":
    main()