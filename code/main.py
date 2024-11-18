from settings import *
from player import Player
from sprites import *
from pytmx.util_pygame import load_pygame
from groups import AllSprites
from random import randint, choice
from puntuacion import mostrar_puntuacion  # Importar la función para mostrar la puntuación

# Definir la función dibujar_texto
def dibujar_texto(texto, fuente, color, x, y):
    superficie_texto = fuente.render(texto, True, color)
    rect_texto = superficie_texto.get_rect()
    rect_texto.topleft = (x, y)
    pantalla = pygame.display.get_surface()
    pantalla.blit(superficie_texto, rect_texto)

class MainGame:  # Clase principal del juego
    def __init__(self):
        pygame.init()
        pygame.font.init()  # Inicializar el módulo de fuentes de Pygame
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Survivor')
        self.clock = pygame.time.Clock()
        self.running = True
        self.score = 0  # Inicializar la puntuación
        self.lives = 5  # Inicializar las vidas
        self.invulnerable = False  # Estado de invulnerabilidad
        self.invulnerable_time = 0  # Tiempo de inicio de la invulnerabilidad
        self.invulnerable_duration = 2000  # Duración de la invulnerabilidad en milisegundos

        # Groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

        # Gun timer
        self.can_shoot = True
        self.shoot_time = 0
        self.gun_cooldown = 100

        # Enemy timer
        self.enemy_event = pygame.event.custom_type()
        pygame.time.set_timer(self.enemy_event, 300)
        self.spawn_positions = []

        # Audio
        self.shoot_sound = pygame.mixer.Sound(join('audio', 'shoot.wav'))
        self.shoot_sound.set_volume(0.2)
        self.impact_sound = pygame.mixer.Sound(join('audio', 'impact.ogg'))
        self.music = pygame.mixer.Sound(join('audio', 'music.wav'))
        self.music.set_volume(0.5)

        # Load images and setup
        self.load_images()
        self.setup()

    def load_images(self):
        self.bullet_surf = pygame.image.load(join('images', 'gun', 'bullet.png')).convert_alpha()
        heart_image = pygame.image.load(join('images', 'fondo', 'corazon.png')).convert_alpha()  # Cargar la imagen del corazón
        self.heart_surf = pygame.transform.scale(heart_image, (30, 30))  # Redimensionar la imagen del corazón

        folders = list(walk(join('images', 'enemies')))[0][1]
        self.enemy_frames = {}
        for folder in folders:
            for folder_path, _, file_names in walk(join('images', 'enemies', folder)):
                self.enemy_frames[folder] = []
                for file_name in sorted(file_names, key=lambda name: int(name.split('.')[0])):
                    full_path = join(folder_path, file_name)
                    surf = pygame.image.load(full_path).convert_alpha()
                    self.enemy_frames[folder].append(surf)

    def input(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            self.shoot_sound.play()
            pos = self.gun.rect.center + self.gun.player_direction * 50
            Bullet(self.bullet_surf, pos, self.gun.player_direction, (self.all_sprites, self.bullet_sprites))
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()

    def gun_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= self.gun_cooldown:
                self.can_shoot = True

    def setup(self):
        map = load_pygame(join('data', 'maps', 'world.tmx'))

        for x, y, image in map.get_layer_by_name('Ground').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)

        for obj in map.get_layer_by_name('Objects'):
            CollisionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))

        for obj in map.get_layer_by_name('Collisions'):
            CollisionSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites)

        for obj in map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites)
                self.gun = Gun(self.player, self.all_sprites)
            else:
                self.spawn_positions.append((obj.x, obj.y))

    def bullet_collision(self):
        if self.bullet_sprites:
            for bullet in self.bullet_sprites:
                collision_sprites = pygame.sprite.spritecollide(bullet, self.enemy_sprites, False, pygame.sprite.collide_mask)
                if collision_sprites:
                    self.impact_sound.play()
                    for sprite in collision_sprites:
                        sprite.destroy()
                        self.score += 50  # Incrementar la puntuación
                    bullet.kill()

    def player_collision(self):
        if not self.invulnerable and pygame.sprite.spritecollide(self.player, self.enemy_sprites, False, pygame.sprite.collide_mask):
            self.lives -= 1  # Reducir una vida
            self.invulnerable = True  # Activar invulnerabilidad
            self.invulnerable_time = pygame.time.get_ticks()  # Registrar el tiempo de inicio de la invulnerabilidad
            if self.lives <= 0:
                self.running = False
                from menu import Game  # Importar aquí para evitar la importación circular
                mostrar_puntuacion(self.score, MainGame, Game)  # Mostrar la ventana de puntuación

    def check_invulnerability(self):
        if self.invulnerable:
            current_time = pygame.time.get_ticks()
            if current_time - self.invulnerable_time >= self.invulnerable_duration:
                self.invulnerable = False  # Desactivar invulnerabilidad

    def draw_lives(self):
        for i in range(self.lives):
            self.display_surface.blit(self.heart_surf, (10 + i * 35, 10))  # Dibujar corazones en la parte superior izquierda

    def run(self):
        pygame.font.init()  # Asegurarse de inicializar pygame.font aquí también
        while self.running:
            # dt
            dt = self.clock.tick() / 1000

            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == self.enemy_event:
                    Enemy(choice(self.spawn_positions), choice(list(self.enemy_frames.values())), (self.all_sprites, self.enemy_sprites), self.player, self.collision_sprites)

            # update
            self.gun_timer()
            self.input()
            self.all_sprites.update(dt)
            self.bullet_collision()
            self.player_collision()
            self.check_invulnerability()  # Verificar invulnerabilidad

            dibujar_texto("Forest War",
                          pygame.font.SysFont("Arial", 30),
                          (255, 255, 255), 300, 100)

            # draw
            self.display_surface.fill('black')
            self.all_sprites.draw(self.player.rect.center)
            self.draw_lives()  # Dibujar las vidas
            pygame.display.update()

        pygame.quit()

if __name__ == '__main__':
    game = MainGame()
    game.run()