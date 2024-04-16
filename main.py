import pygame_menu
import gra
if __name__ == '__main__':
    menu = pygame_menu.Menu("Block Breaker", 600, 800)
    menu.add.button('Play', gra.game())