import pygame
from pygame.locals import *
from time import *

pygame.init()

# Ekran boyutları
WIN_WIDTH, WIN_HEIGHT = 800, 500
window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Pong")




# Renkler
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Raket ayarları
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 100
PADDLE_SPEED = 7

# Top ayarları
BALL_SIZE = 20
BALL_SPEED_X = 5
BALL_SPEED_Y = 5

# Oyuncular
left_paddle = pygame.Rect(30, WIN_HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(WIN_WIDTH-30-PADDLE_WIDTH, WIN_HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)

# Top
ball = pygame.Rect(WIN_WIDTH//2 - BALL_SIZE//2, WIN_HEIGHT//2 - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)

# Skorlar
score_left = 0
score_right = 0
font = pygame.font.SysFont("Arial", 50)

#KAZAN KAYBET



# Oyun döngüsü
clock = pygame.time.Clock()
running = True
ball_dx, ball_dy = BALL_SPEED_X, BALL_SPEED_Y

run=True

finish=False


while run:
    for e in pygame.event.get():
        if e.type == QUIT:
            run=False

    if not finish:
        pygame.display.update()

        keys = pygame.key.get_pressed()
        # Sol oyuncu (W/S)
        if keys[K_w] and left_paddle.top > 0:
            left_paddle.y -= PADDLE_SPEED
        if keys[K_s] and left_paddle.bottom < WIN_HEIGHT:
            left_paddle.y += PADDLE_SPEED
        # Sağ oyuncu (Yukarı/Aşağı ok)
        if keys[K_UP] and right_paddle.top > 0:
            right_paddle.y -= PADDLE_SPEED
        if keys[K_DOWN] and right_paddle.bottom < WIN_HEIGHT:
            right_paddle.y += PADDLE_SPEED

        # Top hareketi
        ball.x += ball_dx
        ball.y += ball_dy

        # Yukarı aşağı çarpma
        if ball.top <= 0 or ball.bottom >= WIN_HEIGHT:
            ball_dy *= -1

        # Rakete çarpma
        if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
            ball_dx *= -1

        # Skor kontrolü
        if ball.left <= 0:
            score_right += 1
            ball.center = (WIN_WIDTH//2, WIN_HEIGHT//2)
            ball_dx = BALL_SPEED_X
            ball_dy = BALL_SPEED_Y

        if ball.right >= WIN_WIDTH:
            score_left += 1
            ball.center = (WIN_WIDTH//2, WIN_HEIGHT//2)
            ball_dx = -BALL_SPEED_X
            ball_dy = BALL_SPEED_Y

                

        # Ekranı çiz
        window.fill(BLACK)
        pygame.draw.rect(window, WHITE, left_paddle)
        pygame.draw.rect(window, WHITE, right_paddle)
        pygame.draw.ellipse(window, WHITE, ball)
        pygame.draw.aaline(window, WHITE, (WIN_WIDTH//2, 0), (WIN_WIDTH//2, WIN_HEIGHT))

        # Skorları yazdır

            

        score_text = font.render(f"{score_left}   {score_right}", True, WHITE)
        window.blit(score_text, (WIN_WIDTH//2 - score_text.get_width()//2, 20))

        if score_left==3:
            kazansol = font.render("SOL TARAF KAZANDI", True, (255,255,255))
            window.blit(kazansol,(WIN_WIDTH//2 - kazansol.get_width()//2, 70))
            break

            score_left=0
            score_right=0

            

        if score_right==3:
            kazansag = font.render("SAĞ TARAF KAZANDI", True, WHITE)
            window.blit(kazansag, (WIN_WIDTH//2 - kazansag.get_width()//2, 70))
            break

            score_right=0
            score_left=0



        

        pygame.display.update()
        clock.tick(60)

    score_right=0
    score_left=0





#pygame.quit()
