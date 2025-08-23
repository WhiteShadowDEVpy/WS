import pygame
import sys
import math
import random
from time import time

# Pygame başlat
pygame.init()
WIDTH, HEIGHT = 1200, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Göz Animasyonu - Hediye")

# Renkler
WHITE = (0, 0, 0)
BLACK = (0, 0, 0)
BLUE = (50, 50, 255)
RED = (255, 0, 0)

# Saat ve font
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

# Kalp verisi
hearts = []

def draw_heart(surface, x, y, size):
    points = []
    for t in range(0, 360, 5):
        angle = math.radians(t)
        x1 = size * 16 * math.sin(angle) ** 3
        y1 = -size * (13 * math.cos(angle) - 5 * math.cos(2 * angle) -
                      2 * math.cos(3 * angle) - math.cos(4 * angle))
        points.append((x + x1, y + y1))
    pygame.draw.polygon(surface, RED, points)

class Eye:
    def __init__(self, x, y):
        self.base_width = 100
        self.base_height = 100
        self.x = x
        self.y = y
        self.blink_timer = 0
        self.blink_duration = 0.4
        self.blink_interval = 3
        self.last_blink_time = time()
        self.blinking = False
        self.blink_progress = 0

    def update(self, dt, looking_direction):
        current_time = time()
        if not self.blinking and current_time - self.last_blink_time >= self.blink_interval:
            self.blinking = True
            self.blink_timer = 0

        if self.blinking:
            self.blink_timer += dt
            progress = self.blink_timer / self.blink_duration
            if progress < 0.5:
                self.blink_progress = 1 - 2 * progress  # kapanma
            else:
                self.blink_progress = 2 * progress - 1  # açılma
            if self.blink_timer >= self.blink_duration:
                self.blinking = False
                self.last_blink_time = current_time

    def draw(self, surface, is_left, looking_direction):
        # Bakış yönüne göre büyüklüğü etkileyelim
        bias = 1.0 if (is_left and looking_direction == 'left') or (not is_left and looking_direction == 'right') else 1.0
        width = int(self.base_width * bias)
        height = int(self.base_height * self.blink_progress * bias)
        height = max(height, 10)

        eye_rect = pygame.Rect(self.x - width // 2, self.y - height // 2, width, height)
        pygame.draw.rect(surface, BLUE, eye_rect, border_radius=12)

class Heart:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 0.5
        self.max_size = 1.5
        self.growth_speed = 1.5
        self.lifetime = 1.5
        self.age = 0

    def update(self, dt):
        self.age += dt
        if self.size < self.max_size:
            self.size += self.growth_speed * dt

    def draw(self, surface):
        if self.age < self.lifetime:
            draw_heart(surface, self.x, self.y, self.size)

# Gözleri oluştur
left_eye = Eye(WIDTH // 3, HEIGHT // 2)
right_eye = Eye(2 * WIDTH // 3, HEIGHT // 2)

# Bakış yönü
looking_direction = 'center'
direction_timer = 0
direction_interval = 5

# Ana döngü
running = True
last_time = time()

while running:
    SCREEN.fill(WHITE)
    current_time = time()
    dt = current_time - last_time
    last_time = current_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            hearts.append(Heart(mx, my))

    # Göz yönü güncelle
    direction_timer += dt
    if direction_timer > direction_interval:
        looking_direction = random.choice(['left', 'right', 'center'])
        direction_timer = 0

    # Gözleri güncelle
    left_eye.update(dt, looking_direction)
    right_eye.update(dt, looking_direction)

    # Gözleri çiz
    left_eye.draw(SCREEN, is_left=True, looking_direction=looking_direction)
    right_eye.draw(SCREEN, is_left=False, looking_direction=looking_direction)

    # Kalpleri güncelle ve çiz
    for heart in hearts[:]:
        heart.update(dt)
        heart.draw(SCREEN)
        if heart.age > heart.lifetime:
            hearts.remove(heart)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
