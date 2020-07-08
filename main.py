import pygame
import os
import random

# Set window position
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (50, 50)

pygame.init()
font = pygame.font.SysFont("monospace", 20)

TITLE = "Snake"
WIDTH = 800
HEIGHT = 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
RECT_SIZE = 20
KEYS = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]


class Snake:
    def __init__(self, start_x, start_y, length=10, height=10):
        self.x = start_x
        self.y = start_y
        self.length = length
        self.height = height
        self.snake = [(self.x, self.y)]
        for x in range(1, length):
            self.add(self.x - (x * height), self.y)

    def grow(self):
        x = 0
        y = 0
        s1 = self.snake[-1]
        s2 = self.snake[-2]

        if s1[1] == s2[1]:
            x = s1[0] + (s1[0] - s2[0])
            y = s1[1]
        if s1[0] == s2[0]:
            x = s1[0]
            y = s1[1] + (s1[1] - s2[1])
        self.snake.append((x, y))

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
            pygame.draw.rect(surface, (0, 255, 0), (s[0], s[1], self.height, self.height))


def draw_food(surface, x, y):
    pygame.draw.rect(surface, (255, 255, 255), (x, y, RECT_SIZE, RECT_SIZE))


def new_food(width, height):
    while True:
        x = random.randrange(0, width)
        y = random.randrange(0, height)
        if x % RECT_SIZE == 0 and y % RECT_SIZE == 0:
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
    keys_pressed = []

    # icon = pygame.image.load(os.path.join("assets", "HelloWorld_32x32.png"))
    pygame.display.set_caption(TITLE)
    # pygame.display.set_icon(icon)

    # Game loop
    running = True
    food = new_food(WIDTH, HEIGHT - 50)
    clock = pygame.time.Clock()
    snake = Snake(WIDTH - RECT_SIZE, pos_y, 10, RECT_SIZE)

    def process_input():
        d = direction
        if len(keys_pressed) != 0:
            key = keys_pressed[0]
            if key == pygame.K_LEFT and pos_x > 0 and direction != 1:
                d = 0
            if key == pygame.K_RIGHT and pos_x < WIDTH - 10 and direction != 0:
                d = 1
            if key == pygame.K_UP and pos_y < HEIGHT - 10 and direction != 3:
                d = 2
            if key == pygame.K_DOWN and pos_y > 0 and direction != 2:
                d = 3
            del keys_pressed[0]
        return d

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
        if ticks < 8:
            ticks += 1
        else:
            if dead:
                running = False

            ticks = 0
            if not dead:
                direction = process_input()
                dead = not snake.move(direction, WIDTH, HEIGHT - 50)
                if snake.contains(food):
                    score += 1
                    snake.grow()
                    food = new_food(WIDTH, HEIGHT - 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                quit()
            if event.type == pygame.KEYUP:
                if event.key in KEYS:
                    keys_pressed.append(event.key)
                if event.key == pygame.K_q:
                    running = False

        SCREEN.fill((0, 0, 0))
        pos_x, pos_y = update(pos_x, pos_y)
        pygame.display.update()


def main_menu():
    run = True

    while run:
        title_label = font.render("Press space to start...", 1, (255, 255, 255))
        SCREEN.blit(title_label, (WIDTH / 2 - title_label.get_width() / 2, HEIGHT / 2 - (title_label.get_height() / 2)))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                main()
    pygame.quit()
    quit()


if __name__ == '__main__':
    main_menu()
