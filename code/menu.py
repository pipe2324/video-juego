import pygame
import sys
from random import choice
from os.path import join
from os import walk
from pytmx.util_pygame import load_pygame
from main import MainGame  # Importación absoluta
from groups import AllSprites
from player import Player
from sprites import *
from settings import *

# Función para dibujar_texto
def dibujar_texto(texto, fuente, color, x, y):
    superficie_texto = fuente.render(texto, True, color)
    rect_texto = superficie_texto.get_rect()
    rect_texto.topleft = (x, y)
    pantalla = pygame.display.get_surface()
    pantalla.blit(superficie_texto, rect_texto)

class Menu:
    def __init__(self, display_surface):
        self.display_surface = display_surface
        self.font = pygame.font.Font(None, 74)
        self.title_font = pygame.font.Font(None, 100)

        # Cargar la imagen de fondo
        self.background_image = pygame.image.load(join('images', 'fondo', 'fund.jpeg')).convert()

        # Texto del título
        self.title_text = self.title_font.render('Survivor', True, 'Black')  # Cambiar el color del título a negro
        self.title_rect = self.title_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4))

    def draw(self):
        # Dibujar la imagen de fondo
        self.display_surface.blit(self.background_image, (0, 0))
        
        # Dibujar el contorno del título
        for offset in [(1, 1), (-1, -1), (1, -1), (-1, 1)]:
            contour_rect = self.title_rect.move(offset)
            contour_text = self.title_font.render('Survivor', True, 'White')
            self.display_surface.blit(contour_text, contour_rect)
        
        # Dibujar el título del juego
        self.display_surface.blit(self.title_text, self.title_rect)

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  # Salir del juego
        return None

class Game:
    def __init__(self):
        pygame.font.init()  # Inicializar el módulo de fuentes de Pygame
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Survivor')
        self.clock = pygame.time.Clock()
        self.running = True

        # Crear una instancia del menú
        self.menu = Menu(self.display_surface)

        # Texto y botones
        self.font = pygame.font.Font(None, 74)  # Usar la misma fuente y tamaño de letra
        self.boton_jugar_text = self.font.render('Jugar', True, 'Black')
        self.boton_jugar_rect = self.boton_jugar_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 25))
        self.boton_jugar = pygame.Rect(self.boton_jugar_rect.left - 70, self.boton_jugar_rect.top - 10, 280, self.boton_jugar_rect.height + 20)

        self.boton_salir_text = self.font.render('Salir', True, 'Black')
        self.boton_salir_rect = self.boton_salir_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
        self.boton_salir = pygame.Rect(self.boton_salir_rect.left - 81, self.boton_salir_rect.top - 10, 279, self.boton_salir_rect.height + 20)

    def run(self):
        """Función principal del juego."""
        while self.running:
            self.eventos_menu()
            pygame.display.update()
        pygame.quit()

    def eventos_menu(self):
        self.display_surface.fill('black')
        self.menu.draw()  # Dibujar el menú
        # Dibujar botones
        pygame.draw.rect(self.display_surface, (0, 128, 0), self.boton_jugar)
        pygame.draw.rect(self.display_surface, (0, 0, 0), self.boton_jugar, 3)  # Contorno negro
        self.display_surface.blit(self.boton_jugar_text, self.boton_jugar_rect)

        pygame.draw.rect(self.display_surface, (128, 0, 0), self.boton_salir)
        pygame.draw.rect(self.display_surface, (0, 0, 0), self.boton_salir, 3)  # Contorno negro
        self.display_surface.blit(self.boton_salir_text, self.boton_salir_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.boton_jugar.collidepoint(event.pos):
                    self.juego(MainGame)
                elif self.boton_salir.collidepoint(event.pos):
                    self.running = False

    def juego(self, main_game_class):
        """Pantalla del juego principal."""
        main_game = main_game_class()  # Crear una instancia del juego principal
        main_game.run()  # Ejecutar el juego principal
        self.running = True  # Reiniciar el menú después de que el juego principal termine

if __name__ == '__main__':
    game = Game()
    game.run()