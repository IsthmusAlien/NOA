import pygame
import main

WIDTH, HEIGHT = 1000, 750
BUTTON_WIDTH,  BUTTON_HEIGHT = 150, 50

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("NOA The Ambush")
MENU_BG = pygame.transform.scale(pygame.image.load("imgs\\menu_bg.png"), (WIDTH, HEIGHT))
START_BUTTON = pygame.transform.scale(pygame.image.load("imgs\\strtbutn.png"), (BUTTON_WIDTH, BUTTON_HEIGHT))
ICON = pygame.transform.scale(pygame.image.load("imgs\\icon.png"), (60, 20))
pygame.display.set_icon(ICON)

def menu_draw():

    WIN.blit(MENU_BG, (0, 0))
    WIN.blit(START_BUTTON, (425, 350))
    pygame.display.update()

def menu_main():

    run = True

    while run:

        mouse_x, mouse_y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        if pygame.mouse.get_pressed()[0] and 427 <= mouse_x <= 574 and 353 <= mouse_y <= 399:
            main.main()

        menu_draw()


if __name__ == "__main__":
    menu_main()