import pygame
import time
import random
import os
from pygame import mixer

pygame.font.init()

WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dodge")

BG = pygame.transform.scale(pygame.image.load("TheGame/bkg.jpeg"), (WIDTH, HEIGHT))

# PLAYER
PLAYER_HEIGHT = 150
PLAYER_WIDTH = 90
PLAYER_VEL = 5

# STARS
STAR_WIDTH = 10
STAR_HEIGHT = 20
STAR_VEL = 5

# BULLETS
BULLET_HEIGHT = 10
BULLET_WIDTH = 5
BULLET_VEL = 7
BULLET_COOLDOWN = 500

FONT = pygame.font.SysFont("comicsans", 30)
font = pygame.font.SysFont("comicsans", 75)

# AUDIO FILES
pygame.mixer.init() 
bksound = pygame.mixer.music.load("TheGame/background.wav")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.3)

bulletsound = pygame.mixer.Sound("TheGame/laser.wav")
bulletsound.set_volume(0.5)

exsound = pygame.mixer.Sound("TheGame/explosion.wav")
exsound.set_volume(0.5)

HIGH_SCORE_FILE = "highscore.txt"

def load_highscore():
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, "r") as file:
            return int(file.read())
    return 0

def save_highscore(highscore):
    with open(HIGH_SCORE_FILE, "w") as file:
        file.write(str(highscore))

def draw_homescreen(highscore):
    WIN.fill("black")
    title_text = font.render("Space Dodge", 1, "white")
    highscore_text = FONT.render(f"High Score: {highscore}", 1, "white")
    start_text = FONT.render("Press space to start", 1, "white")

    WIN.blit(title_text, (WIDTH / 2 - title_text.get_width() / 2, HEIGHT / 3))
    WIN.blit(highscore_text, (WIDTH / 2 - highscore_text.get_width() / 2, HEIGHT / 2))
    WIN.blit(start_text, (WIDTH / 2 - start_text.get_width() / 2, HEIGHT / 1.5))

    pygame.display.update()

def draw_gameover_screen(score, highscore):
    WIN.fill("black")
    gameover_text = font.render("Game Over", 1, "white")
    score_text = FONT.render(f"Score: {score}", 1, "white")
    highscore_text = FONT.render(f"High Score: {highscore}", 1, "white")
    restart_text = FONT.render("Press any key to restart", 1, "white")

    WIN.blit(gameover_text, (WIDTH / 2 - gameover_text.get_width() / 2, HEIGHT / 4))
    WIN.blit(score_text, (WIDTH / 2 - score_text.get_width() / 2, HEIGHT / 2))
    WIN.blit(highscore_text, (WIDTH / 2 - highscore_text.get_width() / 2, HEIGHT / 1.8))
    WIN.blit(restart_text, (WIDTH / 2 - restart_text.get_width() / 2, HEIGHT / 1.5))

    pygame.display.update()

def draw(player, elapsed_time, stars, bullets, score, player_img):
    WIN.blit(BG, (0, 0))
    
    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    score_text = FONT.render(f"Score: {score}", 1, "white")
    WIN.blit(score_text, (WIDTH - score_text.get_width() - 10, 10))
    WIN.blit(time_text, (10, 10))

    # pygame.draw.rect(WIN, "TheGame/spaceship.jpeg", player)
    WIN.blit(player_img,(player.x,player.y))

    for bullet in bullets:
        pygame.draw.rect(WIN, "yellow", bullet)
    
    for star in stars:
        pygame.draw.rect(WIN, "white", star)
    
    pygame.display.update()

def main():
    run = True
    clock = pygame.time.Clock()
    
    highscore = load_highscore()
    game_state = "homepage"
    score = 0
    
    player_img = pygame.image.load("TheGame/spaceship2.png")
    player_img = pygame.transform.scale(player_img, (PLAYER_WIDTH,PLAYER_HEIGHT))
    
    while run:
        if game_state == "homepage":
            draw_homescreen(highscore)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    game_state = "playing"
                    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
                    score = 0
                    elapsed_time = 0
                    start_time = time.time()
                    star_add_increment = 2000
                    star_count = 0
                    stars = []
                    bullets = []
                    last_bullet_time = 0
                    hit = False
        
        elif game_state == "playing":
            clock.tick(60)  # Ensure the game runs at 60 FPS
            star_count += clock.get_time()
            elapsed_time = time.time() - start_time
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            
            if star_count > star_add_increment:
                for _ in range(3):
                    star_x = random.randint(0, WIDTH - STAR_WIDTH)
                    star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                    stars.append(star)
                    
                star_add_increment = max(200, star_add_increment - 50)
                star_count = 0    
                
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
                player.x -= PLAYER_VEL
            if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + PLAYER_WIDTH <= WIDTH:
                player.x += PLAYER_VEL
            if keys[pygame.K_UP] and player.y - PLAYER_VEL >= 0:
                player.y -= PLAYER_VEL
            if keys[pygame.K_DOWN] and player.y + PLAYER_VEL + PLAYER_HEIGHT <= HEIGHT:
                player.y += PLAYER_VEL
            if keys[pygame.K_SPACE]:
                current_time = pygame.time.get_ticks()
                if current_time - last_bullet_time > BULLET_COOLDOWN:
                    bulletsound.play()
                    bullet = pygame.Rect(player.x + PLAYER_WIDTH // 2, player.y, BULLET_WIDTH, BULLET_HEIGHT)
                    bullets.append(bullet)
                    last_bullet_time = current_time
                
            for bullet in bullets[:]:
                bullet.y -= BULLET_VEL
                if bullet.y < 0:
                    bullets.remove(bullet)
            
            for star in stars[:]:
                star.y += STAR_VEL
                if star.y >= HEIGHT:
                    stars.remove(star)
                elif star.y + STAR_HEIGHT >= player.y and star.colliderect(player):
                    stars.remove(star)
                    hit = True
                    break
            
            for bullet in bullets[:]:
                for star in stars[:]:
                    if star.colliderect(bullet):
                        exsound.play()
                        stars.remove(star)
                        bullets.remove(bullet)
                        score += 1
            
            if hit:
                exsound.play()
                if score > highscore:
                    highscore = score
                    save_highscore(highscore)
                game_state = "gameover"
            
            draw(player, elapsed_time, stars, bullets, score, player_img)
        
        elif game_state == "gameover":
            draw_gameover_screen(score, highscore)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    game_state = "homepage"
    
    pygame.quit()

if __name__ == "__main__":
    main()
