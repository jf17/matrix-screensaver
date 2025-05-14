import pygame
import random
import sys
import math


# Настройки экрана
WIDTH, HEIGHT = 1024, 768
FONT_SIZE = 40
FPS = 7
TRAIL_LENGTH_FOREGROUND = 13
TRAIL_LENGTH_BACKGROUND = 8

SYMBOLS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%&*"

COMMANDS = [
    "system boot",
    "access granted",
    "connection established",
    "node 192.168.0.42",
    "kill -9 target",
    "auth=OK",
    "traceroute 10.0.0.1",
    "load_module(kernel32.dll)",
    "override enabled",
    "upload complete",
    "decrypting...",
    "monitor online"
]

# Инициализация
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Matrix Screensaver - Double Layer")
clock = pygame.time.Clock()

# Цвета
foreground_colors = [
    (0, 255, 0),
    (0, 200, 0),
    (0, 150, 0),
    (0, 100, 0),
    (0, 60, 0),
    (0, 30, 0)
]
background_colors = [
    (0, 100, 0),
    (0, 80, 0),
    (0, 60, 0),
    (0, 40, 0)
]

font = pygame.font.SysFont("Courier", FONT_SIZE, bold=True)
columns = WIDTH // FONT_SIZE

# Передний план: с вращением
foreground_drops = [random.randint(-HEIGHT, 0) for _ in range(columns)]
foreground_tails = [[] for _ in range(columns)]

# Фон: обычный текст
background_drops = [random.randint(-HEIGHT, 0) for _ in range(columns)]
background_tails = [[] for _ in range(columns)]

# Команды
frame_counter = 0
command_timer = 0
COMMAND_INTERVAL = 150
command_text = ""
command_alpha = 0
COMMAND_FADE_SPEED = 5

def draw_rotated_char(surface, char, color, x, y, angle):
    text_surf = font.render(char, True, color)
    rotated = pygame.transform.rotate(text_surf, angle)
    rect = rotated.get_rect(center=(x + FONT_SIZE // 2, y + FONT_SIZE // 2))
    surface.blit(rotated, rect)

def draw_static_char(surface, char, color, x, y):
    symbol_surface = font.render(char, True, color)
    surface.blit(symbol_surface, (x, y))

def draw_background():
    for i in range(columns):
        x = i * FONT_SIZE
        y = background_drops[i]
        char = random.choice(SYMBOLS)
        background_tails[i].insert(0, (char, y))

        for j, (c, pos_y) in enumerate(background_tails[i][:TRAIL_LENGTH_BACKGROUND]):
            if 0 <= pos_y < HEIGHT:
                color_index = min(j, len(background_colors) - 1)
                color = background_colors[color_index]
                draw_static_char(screen, c, color, x, pos_y)

        background_drops[i] += FONT_SIZE

        if len(background_tails[i]) > TRAIL_LENGTH_BACKGROUND:
            background_tails[i] = background_tails[i][:TRAIL_LENGTH_BACKGROUND]

        if background_drops[i] > HEIGHT + random.randint(0, HEIGHT // 2):
            background_drops[i] = random.randint(-100, 0)
            background_tails[i] = []

def draw_foreground():
    global frame_counter
    for i in range(columns):
        x = i * FONT_SIZE
        y = foreground_drops[i]
        char = random.choice(SYMBOLS)
        foreground_tails[i].insert(0, (char, y))

        for j, (c, pos_y) in enumerate(foreground_tails[i][:TRAIL_LENGTH_FOREGROUND]):
            if 0 <= pos_y < HEIGHT:
                color_index = min(j, len(foreground_colors) - 1)
                color = foreground_colors[color_index]
                angle = math.sin((frame_counter + j + i) * 0.1) * 30
                draw_rotated_char(screen, c, color, x, pos_y, angle)

        foreground_drops[i] += FONT_SIZE

        if len(foreground_tails[i]) > TRAIL_LENGTH_FOREGROUND:
            foreground_tails[i] = foreground_tails[i][:TRAIL_LENGTH_FOREGROUND]

        if foreground_drops[i] > HEIGHT + random.randint(0, HEIGHT // 2):
            foreground_drops[i] = random.randint(-100, 0)
            foreground_tails[i] = []

    frame_counter += 1

def draw_command_overlay():
    global command_text, command_alpha, command_timer

    if frame_counter - command_timer > COMMAND_INTERVAL:
        command_text = random.choice(COMMANDS)
        command_timer = frame_counter
        command_alpha = 255

    if command_text and command_alpha > 0:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        text_surface = font.render(command_text, True, (0, 255, 0))
        text_surface.set_alpha(command_alpha)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        overlay.blit(text_surface, text_rect)
        screen.blit(overlay, (0, 0))
        command_alpha = max(0, command_alpha - COMMAND_FADE_SPEED)

def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or \
               (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

        screen.fill((0, 0, 0))
        draw_background()
        draw_foreground()
        draw_command_overlay()
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
