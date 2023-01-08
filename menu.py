import pygame
import sys
from button import Button
import main

pygame.init()

SCREEN = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/Background.png")



def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def play():
    if main.play():
        gameover()

def gameover():
    while True:
        SCREEN.blit(BG, (0, 0))

        GO_POS = pygame.mouse.get_pos()

        GO_TEXT = get_font(40).render("GAME OVER", True, "#b68f40")
        GO_RECT = GO_TEXT.get_rect(center=(320, 100))

        AGAIN_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(200, 200),
                            text_input="Again", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
        TOMENU_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(200, 400),
                            text_input="Menu", font=get_font(40), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(GO_TEXT, GO_RECT)

        for button in [AGAIN_BUTTON, TOMENU_BUTTON]:
            button.changeColor(GO_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if AGAIN_BUTTON.checkForInput(GO_POS):
                    play()
                if TOMENU_BUTTON.checkForInput(GO_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(40).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(320, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(200, 200),
                            text_input="PLAY", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(200, 400),
                            text_input="QUIT", font=get_font(40), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()