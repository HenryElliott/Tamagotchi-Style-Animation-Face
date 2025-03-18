import pygame
import random
import time
import ctypes

pygame.init()
WINDOW_SIZE = 200

screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE), pygame.RESIZABLE)
pygame.display.set_caption("Blinking Eyes")

hwnd = pygame.display.get_wm_info()["window"]
ctypes.windll.user32.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 1 | 2)

BG_COLOR = (0, 0, 0)
EYE_COLOR = MOUTH_COLOR = (255, 255, 255)

EYE_WIDTH, EYE_HEIGHT, EYE_SPACING, EYE_Y = 40, 50, 70, 65
BLINK_FRAMES, FRAME_DELAY = 15, 4
OPEN_TIME_MIN, OPEN_TIME_MAX = 1, 4

eye_positions = [(WINDOW_SIZE // 2 - EYE_SPACING // 2, EYE_Y),
                 (WINDOW_SIZE // 2 + EYE_SPACING // 2, EYE_Y)]

blink_state = is_blinking = False
last_blink_time = time.time()
open_time = random.uniform(OPEN_TIME_MIN, OPEN_TIME_MAX)

dragging = False
offset_x = offset_y = 0

def draw_soft_ellipse(surface, color, center, width, height):
    temp_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.ellipse(temp_surface, color, (0, 0, width, height))
    surface.blit(temp_surface, (center[0] - width // 2, center[1] - height // 2))

def draw_smiley_mouth(surface, color, center, width, height):
    pygame.draw.arc(surface, color, 
                    [center[0] - width // 2, center[1] - height // 2, width, height], 
                    3.14, 0, 3)

def create_round_mask():
    mask_surface = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE), pygame.SRCALPHA)
    pygame.draw.circle(mask_surface, (255, 255, 255, 255), (WINDOW_SIZE // 2, WINDOW_SIZE // 2), WINDOW_SIZE // 2)
    return mask_surface

def draw_eyes_and_mouth():
    screen.fill(BG_COLOR)
    screen.blit(create_round_mask(), (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    
    current_height = max(5, int(EYE_HEIGHT * (1 if not is_blinking else blink_progress)))
    for pos in eye_positions:
        draw_soft_ellipse(screen, EYE_COLOR, pos, EYE_WIDTH, current_height)

    draw_smiley_mouth(screen, MOUTH_COLOR, (WINDOW_SIZE // 2, 150), 60, 30)

def blink_animation():
    global blink_state, is_blinking, last_blink_time, open_time, blink_progress

    if not is_blinking and (time.time() - last_blink_time >= open_time):
        is_blinking, blink_state = True, 0

    if is_blinking:
        blink_progress = 1.0 - ((blink_state / (BLINK_FRAMES / 2)) ** 2) if blink_state < BLINK_FRAMES // 2 else \
                         (blink_state - BLINK_FRAMES / 2) / (BLINK_FRAMES / 2) * (2 - ((blink_state - BLINK_FRAMES / 2) / (BLINK_FRAMES / 2)))
        blink_state += 1

        if blink_state >= BLINK_FRAMES:
            is_blinking = False
            last_blink_time = time.time()
            open_time = random.uniform(OPEN_TIME_MIN, OPEN_TIME_MAX)
            if random.random() < 0.1:
                open_time = 0.3

running = True
clock = pygame.time.Clock()

while running:
    draw_eyes_and_mouth()
    blink_animation()
    
    pygame.display.flip()
    clock.tick(1000 // FRAME_DELAY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
