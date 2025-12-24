import pygame
import time
import random
import math
pygame.font.init()
WIDTH, HEIGHT = 1280, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dodge")
BG = pygame.transform.scale(pygame.image.load("img/bg.jpg"), (WIDTH, HEIGHT))
PLAYER_WIDTH = 60
PLAYER_HEIGHT = 90
PLAYER_VEL = 8
STAR_WIDTH = 30
STAR_HEIGHT = 40
STAR_VEL = 3
STAR_COLORS = [
    "#FF3366",
    "#66FF33",
    "#3366FF",
    "#FFFF33",
    "#FF33FF",
    "#33FFFF"]
HIGH_SCORE = 750
FONT = pygame.font.SysFont("comicsans", 30)
player_img = pygame.transform.scale(pygame.image.load("img/player.png"), (PLAYER_WIDTH, PLAYER_HEIGHT))
star_img = pygame.transform.scale(pygame.image.load("img/star.png"), (STAR_WIDTH, STAR_HEIGHT))
try:
    with open("highscore.txt", "r") as f:
        HIGH_SCORE = int(f.read().strip())
except:
    HIGH_SCORE = HIGH_SCORE
BG_SCROLL = 0
player_glow = pygame.Surface((PLAYER_WIDTH * 3, PLAYER_HEIGHT * 3), pygame.SRCALPHA)
pygame.draw.ellipse(player_glow, (255, 255, 200, 40), player_glow.get_rect())
star_glow = pygame.Surface((STAR_WIDTH * 3, STAR_HEIGHT * 3), pygame.SRCALPHA)
pygame.draw.ellipse(star_glow, (255, 255, 220, 30), star_glow.get_rect())

def draw(player, elapsed_time, stars, score):
    WIN.blit(BG, (0, int(BG_SCROLL)))
    WIN.blit(BG, (0, int(BG_SCROLL) - HEIGHT))
    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "black")
    score_text = FONT.render(f"Score: {score}", 1, "black")
    high_score_text = FONT.render(f"High Score: {HIGH_SCORE}", 1, "black")
    WIN.blit(time_text, (10, 10))
    WIN.blit(score_text, (10, 50))
    WIN.blit(high_score_text, (10, 90))
    WIN.blit(player_glow, (player.x - player_glow.get_width()//2 + player.width//2, player.y - player_glow.get_height()//2 + player.height//2))
    WIN.blit(player_img, (player.x, player.y))
    for star, color in stars:
        WIN.blit(star_glow, (star.x - star_glow.get_width()//2 + star.width//2, star.y - star_glow.get_height()//2 + star.height//2))
        if color == "white":
            temp = star_img.copy()
            white_surf = pygame.Surface(temp.get_size(), pygame.SRCALPHA)
            white_surf.fill((255,255,255,180))
            temp.blit(white_surf, (0,0), special_flags=pygame.BLEND_RGBA_MIN)
            WIN.blit(temp, (star.x, star.y))
        else:
            tint = pygame.Surface(star_img.get_size(), pygame.SRCALPHA)
            c = pygame.Color(color)
            tint.fill((c.r, c.g, c.b, 0))
            temp = star_img.copy()
            temp.blit(tint, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
            WIN.blit(temp, (star.x, star.y))
    pygame.display.update()

def main():
    global HIGH_SCORE, BG_SCROLL
    run = True
    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT,
                        PLAYER_WIDTH, PLAYER_HEIGHT)
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0
    star_add_increment = 1500
    star_count = 0
    score = 0
    stars = []
    hit = False
    while run:
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time
        score = round(elapsed_time * 10)
        if star_count > star_add_increment:
            group_color = random.choice(STAR_COLORS)
            if random.random() < 0.15:
                group_color = "white"
            for i in range(3):
                section_width = WIDTH // 3
                star_x = random.randint(i * section_width, (i + 1) * section_width - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT,
                                STAR_WIDTH, STAR_HEIGHT)
                stars.append((star, group_color))
            star_add_increment = max(500, star_add_increment - 25)
            star_count = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:
            player.x += PLAYER_VEL
        current_vel = STAR_VEL + min(10, elapsed_time // 30)
        for star, color in stars[:]:
            star.y += current_vel
            wiggle = math.sin((star.y + star.x) * 0.05) * 2
            star.x += int(wiggle)
            if star.y > HEIGHT:
                stars.remove((star, color))
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove((star, color))
                hit = True
                break
        BG_SCROLL += 0.5
        if BG_SCROLL >= HEIGHT:
            BG_SCROLL = 0
        if hit:
            if score > HIGH_SCORE:
                HIGH_SCORE = score
                try:
                    with open("highscore.txt", "w") as f:
                        f.write(str(HIGH_SCORE))
                except:
                    pass
            lost_text = FONT.render("You Lost!", 1, "black")
            final_score_text = FONT.render(f"Final Score: {score}", 1, "black")
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            WIN.blit(final_score_text, (WIDTH/2 - final_score_text.get_width()/2, HEIGHT/2 + 50))
            pygame.display.update()
            pygame.time.delay(4000)
            break
        draw(player, elapsed_time, stars, score)
if __name__ == "__main__":
    main()