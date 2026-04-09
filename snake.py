import pygame
import time
import random

pygame.init()

# Enhanced Nokia 3310 / Retro LCD palette
bg_color = (135, 149, 113)      # Base LCD background (grey-green)
pixel_off = (127, 140, 105)     # Unlit LCD pixel (slightly darker than bg)
pixel_on = (40, 48, 30)         # Lit LCD pixel (dark green-black)
text_color = (10, 15, 5)        # Sharp text color

# Display dimensions
width = 600
height = 400
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Retro Snake - Nokia 3310 Edition')

clock = pygame.time.Clock()

# Game grid configurations
snake_block = 20
# Grid spacing for LCD effect
pixel_padding = 2

# Speeds
snake_speed = 8

# Fonts - using something built-in but monospaced/clean if possible
try:
    font_style = pygame.font.SysFont("courier new", 22, bold=True)
    score_font = pygame.font.SysFont("courier new", 24, bold=True)
    title_font = pygame.font.SysFont("courier new", 36, bold=True)
except:
    font_style = pygame.font.SysFont(None, 24)
    score_font = pygame.font.SysFont(None, 24)
    title_font = pygame.font.SysFont(None, 36)

def draw_lcd_grid():
    # Draw unlit pixels to simulate LCD screen background
    for x in range(0, width, snake_block):
        for y in range(0, height, snake_block):
            pygame.draw.rect(window, pixel_off, [x + pixel_padding, y + pixel_padding, snake_block - pixel_padding*2, snake_block - pixel_padding*2])

def draw_score(score):
    value = score_font.render(f"SCORE: {score:03d}", True, text_color)
    # Give a tiny background so it doesn't mesh with grid
    bg_surface = pygame.Surface(value.get_size())
    bg_surface.fill(bg_color)
    window.blit(bg_surface, [10, 10])
    window.blit(value, [10, 10])

def draw_snake(snake_list):
    for idx, x in enumerate(snake_list):
        pygame.draw.rect(window, pixel_on, [x[0] + pixel_padding, x[1] + pixel_padding, snake_block - pixel_padding*2, snake_block - pixel_padding*2])

def draw_food(foodx, foody):
    pygame.draw.rect(window, pixel_on, [foodx + pixel_padding, foody + pixel_padding, snake_block - pixel_padding*2, snake_block - pixel_padding*2])
    # Add a small hole in food to distinguish from snake
    pygame.draw.rect(window, bg_color, [foodx + snake_block//2 - 2, foody + snake_block//2 - 2, 4, 4])

def message(msg, color, y_disp=0):
    mesg = font_style.render(msg, True, color)
    text_rect = mesg.get_rect(center=(width/2, height/2 + y_disp))
    # Small background for readability
    bg_surface = pygame.Surface(mesg.get_size())
    bg_surface.fill(bg_color)
    window.blit(bg_surface, text_rect)
    window.blit(mesg, text_rect)

def title_screen():
    window.fill(bg_color)
    draw_lcd_grid()
    title = title_font.render("Nokia 3310 SNAKE", True, pixel_on)
    title_rect = title.get_rect(center=(width/2, height/2 - 40))
    bg_surf = pygame.Surface(title.get_size())
    bg_surf.fill(bg_color)
    window.blit(bg_surf, title_rect)
    window.blit(title, title_rect)
    
    message("Press SPACE to Start", pixel_on, 20)
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False

def gameLoop():
    game_over = False
    game_close = False

    # Start in middle
    x1 = round((width / 2) / snake_block) * snake_block
    y1 = round((height / 2) / snake_block) * snake_block

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, width - snake_block) / snake_block) * snake_block
    foody = round(random.randrange(0, height - snake_block) / snake_block) * snake_block

    while not game_over:

        while game_close == True:
            window.fill(bg_color)
            draw_lcd_grid()
            message("GAME OVER", text_color, -20)
            message("Press C to Retry or Q to Quit", text_color, 20)
            draw_score(Length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = snake_block
                    x1_change = 0

        # Boundary rules
        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True
            
        x1 += x1_change
        y1 += y1_change
        
        window.fill(bg_color)
        draw_lcd_grid()
        
        draw_food(foodx, foody)
        
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # Check self collision
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        draw_snake(snake_List)
        draw_score(Length_of_snake - 1)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, width - snake_block) / snake_block) * snake_block
            foody = round(random.randrange(0, height - snake_block) / snake_block) * snake_block
            Length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

if __name__ == '__main__':
    title_screen()
    gameLoop()
