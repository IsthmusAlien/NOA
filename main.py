import pygame
import random
import time
import retry_menu
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1000, 750
PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_VEL = 75, 60, 5
STAR_WIDTH, STAR_HEIGHT, STAR_VEL = 20, 25, 3
OBSTACLE_WIDTH, OBSTACLE_HEIGHT, OBSTACLE_VEL = 60, 65, 1
BULLET_WIDTH, BULLET_HEIGHT, BULLET_VEL = 70, 100, 5
EXPLOSION1_WIDTH, EXPLOSION1_HEIGHT = 70, 70
EXPLOSION2_WIDTH, EXPLOSION2_HEIGHT = 150, 65
HEALTHBAR_WIDTH, HEALTHBAR_HEIGHT = 120, 50

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("NOA The Ambush")
FONT = pygame.font.Font("tme.ttf", 30)
BG = pygame.transform.scale(pygame.image.load("imgs\\bg.png"), (WIDTH, HEIGHT))
player_img = pygame.transform.scale(pygame.image.load("imgs\\plyr.png"), (PLAYER_WIDTH, PLAYER_HEIGHT))
star_img = pygame.transform.scale(pygame.image.load("imgs\\str.png"), (STAR_WIDTH, STAR_HEIGHT))
rock_img = pygame.transform.scale(pygame.image.load("imgs\\sprck.png"), (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
bullet_img = pygame.transform.scale(pygame.image.load("imgs\\bult.png"), (BULLET_WIDTH, BULLET_HEIGHT))
explosion1_img = pygame.transform.scale(pygame.image.load("imgs\\exp_1.png"), (EXPLOSION1_WIDTH, EXPLOSION1_HEIGHT))
explosion2_img = pygame.transform.scale(pygame.image.load("imgs\\exp_2.png"), (EXPLOSION2_WIDTH, EXPLOSION2_HEIGHT))
healthbar_full_img = pygame.transform.scale(pygame.image.load("imgs\\flhel.png"), (HEALTHBAR_WIDTH, HEALTHBAR_HEIGHT))
healthbar_moremid_img = pygame.transform.scale(pygame.image.load("imgs\\mmidhel.png"), (HEALTHBAR_WIDTH, HEALTHBAR_HEIGHT))
healthbar_lowmid_img = pygame.transform.scale(pygame.image.load("imgs\\lmidhel.png"), (HEALTHBAR_WIDTH, HEALTHBAR_HEIGHT))
healthbar_empty_img = pygame.transform.scale(pygame.image.load("imgs\\ehel.png"), (HEALTHBAR_WIDTH, HEALTHBAR_HEIGHT))
intro_img = pygame.transform.scale(pygame.image.load("imgs\\char.png"), (WIDTH, HEIGHT))
ICON = pygame.transform.scale(pygame.image.load("imgs\\icon.png"), (60, 20))
pygame.display.set_icon(ICON)

bullet_sfx = pygame.mixer.Sound("sfx\\shoot.mp3")
impact_sfx = pygame.mixer.Sound("sfx\\impact.mp3")
explosion1_sfx = pygame.mixer.Sound("sfx\\explosion_rock.mp3")



def draw(player, stars, rocks, bullets, elapsed_time, explosion1_x, explosion1_y, explosion1, star_hitcount):

    WIN.blit(BG, (0, 0))

    pygame.draw.rect(WIN, (255, 0, 0), player, -1)

    WIN.blit(player_img, (player.x - 5, player.y - 18))

    for bullet in bullets:
        WIN.blit(bullet_img, (bullet.x - 31, bullet.y - 35))
        pygame.draw.rect(WIN, (255, 0, 0), bullet, -1)

    for rock in rocks:
        WIN.blit(rock_img, (rock.x - 5, rock.y - 10))
        pygame.draw.rect(WIN, (255, 0, 0), rock, -1)

    for star in stars:
        WIN.blit(star_img, (star.x - 5, star.y - 9))
        pygame.draw.rect(WIN, (255, 0, 0), star, -1)

    if explosion1:
        WIN.blit(explosion1_img, (explosion1_x - 10, explosion1_y))

    if star_hitcount == 0:
        WIN.blit(healthbar_full_img, (10, 10))
    elif star_hitcount == 1:
        WIN.blit(healthbar_moremid_img, (10, 10))
    elif star_hitcount == 2:
        WIN.blit(healthbar_lowmid_img, (10, 10))

    time_text = FONT.render(f"Repairs: {round(elapsed_time)}%", 1, (255, 255, 255))

    WIN.blit(time_text, (10, 710))

    pygame.display.update()

def main():
    for _ in range(400):
        WIN.blit(intro_img, (0, 0))
        pygame.display.update()

    run = True

    start_time = time.time()

    player = pygame.Rect(200, 500, PLAYER_WIDTH - 10, PLAYER_HEIGHT - 30)

    stars = []

    rocks = []

    bullets = []

    add_increament = 2000

    obstacle_count = 0

    bullet_count = 0

    clock = pygame.time.Clock()

    explosion1_x = -200

    explosion1_y = -200

    explosion1 = False

    explosion1_displaytime = 0

    star_hitcount = 0

    hit = False

    while run:

        explosion1_displaytime += 1

        if explosion1_displaytime > 25:
            explosion1 = False
            explosion1_displaytime = 0

        obstacle_count += clock.tick(60)
        bullet_count += 1

        elapsed_time = time.time() - start_time

        if obstacle_count > add_increament:

            for _ in range(1):
                rock_x = random.randint(0, WIDTH - OBSTACLE_WIDTH)
                rock = pygame.Rect(rock_x, -OBSTACLE_HEIGHT, OBSTACLE_WIDTH - 10, OBSTACLE_HEIGHT - 20)
                rocks.append(rock)

            for _ in range(1):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH - 10, STAR_HEIGHT - 10)
                stars.append(star)

            add_increament = max(500, add_increament - 80)
            obstacle_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + PLAYER_WIDTH <= 1000:
            player.x += PLAYER_VEL
        if keys[pygame.K_UP] and player.y - PLAYER_VEL >= 0:
            player.y -= PLAYER_VEL
        if keys[pygame.K_DOWN] and player.y + PLAYER_VEL + PLAYER_HEIGHT <= 750:
            player.y += PLAYER_VEL
        if keys[pygame.K_SPACE] and bullet_count > 25:
            bullet = pygame.Rect(player.x + 29, player.y - 40, BULLET_WIDTH - 61, BULLET_HEIGHT - 70)
            bullet_sfx.play(0, 200, 200)
            bullets.append(bullet)
            bullet_count = 0

        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player):
                impact_sfx.play(0, 300, 0)
                stars.remove(star)
                star_hitcount += 1
                if star_hitcount >= 3:
                    hit = True
                    break

        for rock in rocks[:]:
            rock.y += OBSTACLE_VEL
            if rock.y > HEIGHT:
                rocks.remove(rock)
            elif rock.y + rock.height >= player.y and rock.colliderect(player):
                impact_sfx.play(0, 300, 0)
                rocks.remove(rock)
                hit = True
                break

        for bullet in bullets[:]:
            bullet.y -= BULLET_VEL
            if bullet.y > HEIGHT:
                bullets.remove(bullet)
            for rock in rocks[:]:
                if bullet.colliderect(rock):
                    explosion1 = True
                    explosion1_sfx.play(0, 300, 0)
                    explosion1_x = rock.x
                    explosion1_y = rock.y
                    rocks.remove(rock)
                    bullets.remove(bullet)

        if round(elapsed_time) == 101:
            pygame.display.update()
            pygame.time.delay(2000)
            break

        if hit:
            WIN.blit(healthbar_empty_img, (10, 10))
            WIN.blit(explosion2_img, (player.x - 45, player.y - 20))
            pygame.display.update()
            pygame.time.delay(2000)
            retry_menu.retry_menu_main()


        draw(player, stars, rocks, bullets, elapsed_time, explosion1_x, explosion1_y, explosion1, star_hitcount)




if __name__ == "__main__":
    main()
