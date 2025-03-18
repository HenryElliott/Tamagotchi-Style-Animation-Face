import pygame
import random
import time
import ctypes
import pyautogui
import math

pygame.init()

WINDOW_SIZE = 200
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE), pygame.RESIZABLE)
pygame.display.set_caption("Blinking Eyes")
hwnd = pygame.display.get_wm_info()["window"]
ctypes.windll.user32.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 1 | 2)

BG_COLOR = (255, 255, 255)
EYE_COLOR = (255, 255, 255)
MOUTH_COLOR = (255, 255, 255)
EYE_WIDTH, EYE_HEIGHT, EYE_SPACING, EYE_Y = 40, 50, 70, 65

BLINK_FRAMES, FRAME_DELAY = 15, 4
OPEN_TIME_MIN, OPEN_TIME_MAX = 1, 4

eye_positions = [(WINDOW_SIZE // 2 - EYE_SPACING // 2, EYE_Y), (WINDOW_SIZE // 2 + EYE_SPACING // 2, EYE_Y)]
blink_state = 0
is_blinking = False
last_blink_time = time.time()
open_time = random.uniform(OPEN_TIME_MIN, OPEN_TIME_MAX)

CHANGE_EYES_CHANCE = 0.1
LAST_CHANGE_TIME = time.time()
CHANGE_TIME_MIN, CHANGE_TIME_MAX = 2, 5

DEAD_EYES_TIME = 5
dead_eyes_start_time = None
is_dead_eyes = False

DEAD_EYES_EVENT_INTERVAL = 10 * 60
last_dead_eyes_event_time = time.time()

font = pygame.font.SysFont("Consolas", 24)

def draw_ellipse(surface, color, center, width, height):
    temp_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.ellipse(temp_surface, color, (0, 0, width, height))
    surface.blit(temp_surface, (center[0] - width // 2, center[1] - height // 2))

def draw_mouth(surface, color, center, width, height):
    pygame.draw.arc(surface, color, [center[0] - width // 2, center[1] - height // 2, width, height], 3.14, 0, 3)

def create_mask():
    mask_surface = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE), pygame.SRCALPHA)
    pygame.draw.circle(mask_surface, (255, 255, 255), (WINDOW_SIZE // 2, WINDOW_SIZE // 2), WINDOW_SIZE // 2, 2)
    return mask_surface

def update_positions():
    mx, my = pyautogui.position()
    eye_center = (WINDOW_SIZE // 2, EYE_Y + EYE_HEIGHT // 2)
    dx, dy = mx - eye_center[0], my - eye_center[1]
    distance = math.sqrt(dx**2 + dy**2)
    max_distance = EYE_WIDTH // 2
    if distance > max_distance:
        dx, dy = dx / distance * max_distance, dy / distance * max_distance
    eye_positions[0] = (eye_center[0] - EYE_SPACING // 2 + dx, eye_center[1] + dy)
    eye_positions[1] = (eye_center[0] + EYE_SPACING // 2 + dx, eye_center[1] + dy)
    return WINDOW_SIZE // 2 + dx, 150 + dy

def draw_dead_eyes(surface, center, width, height):
    pygame.draw.line(surface, (255, 255, 255), (center[0] - width // 2, center[1] - height // 2), 
                     (center[0] + width // 2, center[1] + height // 2), 5)
    pygame.draw.line(surface, (255, 255, 255), (center[0] + width // 2, center[1] - height // 2), 
                     (center[0] - width // 2, center[1] + height // 2), 5)

def draw_face():
    global LAST_CHANGE_TIME, is_dead_eyes, dead_eyes_start_time, last_dead_eyes_event_time

    screen.fill(BG_COLOR)
    screen.blit(create_mask(), (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    if time.time() - last_dead_eyes_event_time >= DEAD_EYES_EVENT_INTERVAL:
        last_dead_eyes_event_time = time.time()  
        if random.random() < CHANGE_EYES_CHANCE and not is_dead_eyes:
            is_dead_eyes = True
            dead_eyes_start_time = time.time()  

    if is_dead_eyes:
        if time.time() - dead_eyes_start_time < DEAD_EYES_TIME:
            for pos in eye_positions:
                draw_dead_eyes(screen, pos, EYE_WIDTH, EYE_HEIGHT)
        else:
            is_dead_eyes = False
    else:
        current_height = max(5, int(EYE_HEIGHT * (1 if not is_blinking else blink_progress)))
        for pos in eye_positions:
            draw_ellipse(screen, EYE_COLOR, pos, EYE_WIDTH, current_height)
    
    mouth_center_x, mouth_center_y = update_positions()
    draw_mouth(screen, MOUTH_COLOR, (mouth_center_x, mouth_center_y), 60, 30)

def blink_logic():
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
    update_positions()
    draw_face()
    blink_logic()
    pygame.display.flip()
    clock.tick(1000 // FRAME_DELAY)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
