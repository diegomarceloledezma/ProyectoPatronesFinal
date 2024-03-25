import pygame
import random
import math
import sys
import os

# Inicializar pygame
pygame.init()

# Establece el tamaño de la pantalla
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Función para obtener la ruta de los recursos
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# Clase para representar a los enemigos
class Enemy:
    def __init__(self, image_path, x, y, x_change, y_change):
        self.image = pygame.image.load(image_path)
        self.x = x
        self.y = y
        self.x_change = x_change
        self.y_change = y_change

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def move(self):
        self.x += self.x_change
        if self.x <= 0:
            self.x_change = 5
            self.y += self.y_change
        elif self.x >= 736:
            self.x_change = -5
            self.y += self.y_change


# Fábrica para crear enemigos
class EnemyFactory:
    @staticmethod
    def create_enemy():
        enemy_type = random.choice(['enemy1', 'enemy2'])  # Se elige un tipo de enemigo al azar
        image_path = resource_path(f'assets/images/{enemy_type}.png')
        x = random.randint(0, 736)
        y = random.randint(0, 150)
        x_change = 5
        y_change = 20
        return Enemy(image_path, x, y, x_change, y_change)


# Cargar recursos
asset_background = resource_path('assets/images/background.png')
background = pygame.image.load(asset_background)

asset_icon = resource_path('assets/images/ufo.png')
icon = pygame.image.load(asset_icon)

asset_sound = resource_path('assets/audios/background_music.mp3')
background_sound = pygame.mixer.music.load(asset_sound)

asset_playerimg = resource_path('assets/images/space-invaders.png')
playerimg = pygame.image.load(asset_playerimg)

asset_bulletimg = resource_path('assets/images/bullet.png')
bulletimg = pygame.image.load(asset_bulletimg)

asset_over_font = resource_path('assets/fonts/RAVIE.TTF')
over_font = pygame.font.Font(asset_over_font, 60)

asset_font = resource_path('assets/fonts/comicbd.ttf')
font = pygame.font.Font(asset_font, 32)

# Establecer título e ícono de la ventana
pygame.display.set_caption("Space Destiny")
pygame.display.set_icon(icon)

# Reproducir sonido de fondo en loop
pygame.mixer.music.play(-1)

# Crear reloj para controlar la velocidad del juego
clock = pygame.time.Clock()

# Posición inicial del jugador
playerX = 370
playerY = 470
playerX_change = 0

# Inicializar lista para enemigos
enemies = []

# Crear enemigos usando la fábrica
for _ in range(10):
    enemy = EnemyFactory.create_enemy()
    enemies.append(enemy)

# Función para mostrar la puntuación en la pantalla
def show_score(score):
    score_value = font.render("SCORE " + str(score), True, (255, 255, 255))
    screen.blit(score_value, (10, 10))


# Función para disparar la bala
def fire_bullet(x, y):
    screen.blit(bulletimg, (x + 16, y + 10))


# Función para comprobar si hubo colisión entre la bala y el enemigo
def isCollision(enemy, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemy.x - bulletX, 2)) + (math.pow(enemy.y - bulletY, 2)))
    return distance < 27


# Función para mostrar el texto de game over en pantalla
def game_over_text(): 
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    text_rect = over_text.get_rect(center=(int(screen_width / 2), int(screen_height / 2)))
    screen.blit(over_text, text_rect)


# Inicializar lista para enemigos
enemies = []

# Definir el número máximo de enemigos que quieres crear
max_enemies = 5

# Contador para el número total de enemigos creados
total_enemies_created = 0




# Función principal del juego
def gameloop():
    # Variables globales
    global total_enemies_created  # Declarar como global para modificar la variable exterior
    global playerX, playerX_change  # Declarar playerX_change como global

    bulletX = 0
    bulletY = 480
    bullet_state = "ready"
    score = 0

    # Crear nuevos enemigos si el total de enemigos creados es menor que el límite
    while total_enemies_created < max_enemies:
        enemy = EnemyFactory.create_enemy()
        enemies.append(enemy)
        total_enemies_created += 1

    in_game = True
    while in_game:
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_game = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -5
                if event.key == pygame.K_RIGHT:
                    playerX_change = 5
                if event.key == pygame.K_SPACE:
                    if bullet_state == "ready":
                        bulletX = playerX
                        bullet_state = "fire"

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

        playerX += playerX_change

        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        for enemy in enemies:
            enemy.move()
            enemy.draw()

            if enemy.y > 440:
                game_over_text()
                in_game = False

            collision = isCollision(enemy, bulletX, bulletY)
            if collision:
                bulletY = 454
                bullet_state = "ready"
                score += 1
                enemies.remove(enemy)
                enemy = EnemyFactory.create_enemy()
                enemies.append(enemy)

        if bulletY < 0:
            bulletY = 454
            bullet_state = "ready"
        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= 10

        screen.blit(playerimg, (playerX, playerY))
        show_score(score)

        pygame.display.update()
        clock.tick(60)

gameloop()