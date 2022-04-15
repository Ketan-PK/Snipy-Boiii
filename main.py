import random
import math
import pygame
import sys
from button import Button
from random import randrange

# Initialize Pygame
pygame.init()

# Making the game window
Window = pygame.display.set_mode((800, 600))

# Title and Icon
pygame.display.set_caption("Snipy Boi")
icon = pygame.image.load("pistol.png")
pygame.display.set_icon(icon)


# Font Set for menu
def get_font(size):
    return pygame.font.Font("freesansbold.ttf", size)


# Backgrounds
background = pygame.image.load("background.png")
main_background = pygame.image.load("main_background.jpg")


# Game Window
def play():

    global bullet_img, bulletX, bulletY, bulletX_change, bulletY_change, bullet_state, score_value, playerX, playerY, playerX_change, playerY_change, enemy_img, num_of_enemies

    # Player
    player_img = pygame.image.load("sniper.png")
    playerX = 20
    playerY = 500
    playerX_change = 0
    playerY_change = 0

    # Enemy
    global enemy_img, enemyX, enemyY, enemyX_change, enemyY_change, i, j
    enemy_img = ["enemy.png"]
    enemyX = []
    enemyY = []
    enemyX_change = []
    enemyY_change = []
    num_of_enemies = 3

    for i in range(num_of_enemies):
        enemy_img.append(pygame.image.load("enemy.png"))
        enemyX.append(randrange(500, 730))
        enemyY.append(randrange(0, 200))
        enemyX_change.append(random.uniform(-0.15, 0))
        enemyY_change.append(random.uniform(0, 0.15))

    # Bullet
    bullet_img = pygame.image.load("bullet.png")
    bulletX = 0
    bulletY = 0
    bulletX_change = 1
    bulletY_change = 1
    bullet_state = "ready"

    # Score
    score_value = 0

    # Player draw on window
    def player(x, y):
        Window.blit(player_img, (x, y))

    # Enemy draw on window
    def enemy(x, y, i):
        Window.blit(enemy_img[i], (x, y))

    # Bullet draw on window
    def fire_bullet(x, y):
        global bullet_state
        bullet_state = "fire"
        Window.blit(bullet_img, (x + 32, y))

    # Bullet and enemy collision detection
    def isCollision(enemyX, enemyY, bulletX, bulletY):
        distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
        if distance <= 27:
            return True
        else:
            return False

    def show_score(x, y):
        score = font.render("Score: " + str(score_value), True, (255, 255, 255))
        Window.blit(score, (x, y))

    # Game over text
    game_over_font = pygame.font.Font("freesansbold.ttf", 70)

    font = pygame.font.Font("freesansbold.ttf", 32)
    textX = 10
    textY = 10

    def game_over_text():
        over_text = game_over_font.render("Game Over", True, (255, 255, 255))
        Window.blit(over_text, (200, 250))

    # Game Loop
    running = True
    while running:

        Window.fill((162, 82, 45))

        # Background
        Window.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Keystrokes
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change -= 0.4
                if event.key == pygame.K_RIGHT:
                    playerX_change += 0.4
                if event.key == pygame.K_UP:
                    playerY_change -= 0.4
                if event.key == pygame.K_DOWN:
                    playerY_change += 0.4
                if event.key == pygame.K_SPACE:
                    if bullet_state == "ready":
                        bulletX = playerX
                        bulletY = playerY
                        fire_bullet(bulletX, bulletY)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    playerX_change = 0
                    playerY_change = 0

        # Enemy Movement
        for i in range(num_of_enemies):

            # Game Over
            if enemyY[i] >= 380:
                for j in range(num_of_enemies):
                    enemyY[j] = 1000

                game_over_text()
                break

            enemyX[i] += enemyX_change[i]
            enemyY[i] += enemyY_change[i]
            if enemyX[i] <= 275:
                enemyX[i] = randrange(500, 730)

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletX = 0
            bulletY = 0
            bullet_state = "ready"
            enemyX[i] = randrange(500, 730)
            enemyY[i] = randrange(0, 200)
            enemy(enemyX[i], enemyY[i], i)
            score_value += 1

        # Player Movement
        playerX += playerX_change
        playerY += playerY_change

        if playerX <= 0:
            playerX = 0
        if playerX >= 736:
            playerX = 736
        if playerY >= 536:
            playerY = 536
        if playerY <= 420:
            playerY = 420

        # Bullet Movement
        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletX += bulletX_change
            bulletY -= bulletY_change

        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"

        player(playerX, playerY)
        show_score(textX, textY)

        pygame.display.update()


def main_menu():
    while True:
        Window.blit(main_background, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("Snipy Boiii", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("my_button.png"), pos=(400, 250),
                             text_input="PLAY", font=get_font(20), base_color="White", hovering_color="Black")
        OPTIONS_BUTTON = Button(image=pygame.image.load("my_button.png"), pos=(400, 400),
                                text_input="OPTIONS", font=get_font(20), base_color="White", hovering_color="Black")
        QUIT_BUTTON = Button(image=pygame.image.load("my_button.png"), pos=(400, 550),
                             text_input="QUIT", font=get_font(20), base_color="White", hovering_color="Black")

        Window.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(Window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pass
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()
