import pygame
import json
from os.path import exists, join

PUNTUACIONES_FILE = 'puntuaciones.json'

def guardar_puntuacion(score):
    if exists(PUNTUACIONES_FILE):
        with open(PUNTUACIONES_FILE, 'r') as file:
            puntuaciones = json.load(file)
    else:
        puntuaciones = []

    puntuaciones.append(score)
    puntuaciones.sort(reverse=True)
    puntuaciones = puntuaciones[:10]  # Limitar a 10 puestos

    with open(PUNTUACIONES_FILE, 'w') as file:
        json.dump(puntuaciones, file)

def cargar_puntuaciones():
    if exists(PUNTUACIONES_FILE):
        with open(PUNTUACIONES_FILE, 'r') as file:
            return json.load(file)
    return []

def mostrar_puntuacion(score, main_game_class, menu_class):
    guardar_puntuacion(score)
    puntuaciones = cargar_puntuaciones()

    pygame.init()
    pygame.font.init()  # Asegurarse de inicializar pygame.font
    display_surface = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Puntuación')
    font = pygame.font.SysFont(None, 50)
    small_font = pygame.font.SysFont(None, 30)
    running = True

    # Cargar la imagen de fondo
    background_image = pygame.image.load(join('images', 'fondo', 'fund.jpeg')).convert()

    boton_reiniciar = pygame.Rect(200, 500, 200, 50)
    boton_menu = pygame.Rect(400, 500, 200, 50)

    while running:
        # Dibujar la imagen de fondo
        display_surface.blit(background_image, (0, 0))
        
        dibujar_texto("Tabla de Puntuaciones", font, (255, 255, 255), 200, 50)  # Texto en blanco

        y_offset = 150
        for i, puntuacion in enumerate(puntuaciones[:10]):
            dibujar_texto(f"{i + 1}. {puntuacion}", small_font, (255, 255, 255), 300, y_offset)  # Texto en blanco
            y_offset += 40

        pygame.draw.rect(display_surface, (0, 128, 0), boton_reiniciar)
        dibujar_texto("Vuelva a jugar", small_font, (255, 255, 255), 220, 510)

        pygame.draw.rect(display_surface, (128, 0, 0), boton_menu)
        dibujar_texto("Volver al menú", small_font, (255, 255, 255), 420, 510)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if boton_reiniciar.collidepoint(event.pos):
                    main_game = main_game_class()
                    main_game.run()
                    running = False
                elif boton_menu.collidepoint(event.pos):
                    menu = menu_class()
                    menu.run()
                    running = False

    pygame.quit()

def dibujar_texto(texto, fuente, color, x, y):
    superficie_texto = fuente.render(texto, True, color)
    rect_texto = superficie_texto.get_rect()
    rect_texto.topleft = (x, y)
    pantalla = pygame.display.get_surface()
    pantalla.blit(superficie_texto, rect_texto)