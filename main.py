import pygame
import os
import time
import random

# Set window position
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (50,50)

pygame.init()
font = pygame.font.SysFont("monospace", 20)

TITLE = "Snake"
WIDTH = 800
HEIGHT = 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60


class Snake:
    def __init__(self, start_x, start_y, length=10, height=10):
        self.x = start_x
        self.y = start_y
        self.length = length
        self.height = height
        self.snake = [(self.x, self.y)]
        for x in range(1, length):
            self.add(self.x - (x * height), self.y)

    def add(self, x, y):
        self.snake.insert(0, (x, y))

    def contains(self, obj):
        return self.snake.__contains__(obj)

    def move(self, direction, width, height):
        x, y = self.snake[0]
        if direction == 0:  # Left
            x -= self.height
        if direction == 1:  # Right
            x += self.height
        if direction == 2:  # Up
            y -= self.height
        if direction == 3:  # Down
            y += self.height

        # Check for collision between the edge of the screen
        if x > width or x < 0:
            return False
        if y > height or y < 0:
            return False

        # Check for collision between new head position and snake body
        if self.snake.__contains__((x, y)):
            return False

        self.add(x, y)
        self.snake.pop()
        return True

    def draw(self, surface):
        for s in self.snake:
            pygame.draw.rect(surface, (0, 255, 0), (s[0], s[1], 10, 10))


def draw_food(surface, x, y):
    pygame.draw.rect(surface, (255, 255, 255), (x, y, 10, 10))


def new_food(width, height):
    while True:
        x = random.randrange(0, width)
        y = random.randrange(0, height)
        if x % 10 == 0 and y % 10 == 0:
            break
    return x, y


def draw_text(surface, text, x, y):
    text_label = font.render(text, 1, (255, 255, 255))
    surface.blit(text_label, (x, y))


def draw_score(surface, score):
    draw_text(surface, "Score: " + str(score), 20, HEIGHT - 40)


def draw_game_over():
    pass


def main():
    # Left
    direction = 0
    pos_x = 300
    pos_y = 300
    food = (0, 0)
    ticks = 0
    dead = False
    score = 0
    # icon = pygame.image.load(os.path.join("assets", "HelloWorld_32x32.png"))
    pygame.display.set_caption(TITLE)
    # pygame.display.set_icon(icon)

    # Game loop
    running = True
    food = new_food(WIDTH, HEIGHT - 50)
    clock = pygame.time.Clock()
    snake = Snake(pos_x, pos_y)

    def update(x, y):
        # SCREEN.blit(text_label, (x, y))
        snake.draw(SCREEN)
        draw_food(SCREEN, food[0], food[1])
        draw_score(SCREEN, score)

        if dead:
            draw_text(SCREEN, "Game over!", (WIDTH / 2) - 70, (HEIGHT / 2) - 30)

        pygame.display.flip()
        pygame.display.update()
        return x, y

    while running:
        clock.tick(FPS)
        if ticks < 10:
            ticks += 1
        else:
            ticks = 0
            if not dead:
                dead = not snake.move(direction, WIDTH, HEIGHT - 50)
                if snake.contains(food):
                    score += 1
                    food = new_food(WIDTH, HEIGHT - 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_q:
                    running = False
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and pos_x > 0:
            direction = 0
        if keys[pygame.K_RIGHT] and pos_x < WIDTH - 10:
            direction = 1
        if keys[pygame.K_UP] and pos_y < HEIGHT - 10:
            direction = 2
        if keys[pygame.K_DOWN] and pos_y > 0:
            direction = 3

        SCREEN.fill((0, 0, 0))
        pos_x, pos_y = update(pos_x, pos_y)
        pygame.display.update()
    pygame.quit()


main()
