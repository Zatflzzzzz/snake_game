import pygame
import random

pygame.init()

SCREEN_WIDTH = 700
SCREEN_HEIGHT= 700

GRID_SIZE = 20

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Змейка")


GREEN = (34, 139, 34)
DARK_GREEN = (0, 100, 0)
RED = (255, 69, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

clock = pygame.time.Clock()

class Snake:

    def __init__(self):

        self.body = [(100, 100), (80, 100), (60, 100)]
        self.direction = (GRID_SIZE, 0)
        self.grow_next = False

    def move(self):

        head_x, head_y = self.body[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])

        if not self.grow_next:
            self.body.pop()

        self.body.insert(0, new_head)
        self.grow_next = False

    def grow(self):
        self.grow_next = True

    def check_collision(self):

        head_x, head_y = self.body[0]

        return (
            head_x < 0 or head_x >= SCREEN_WIDTH or
            head_y < 0 or head_y >= SCREEN_HEIGHT or
            (head_x, head_y) in self.body[1:]
        )

    def draw(self):

        for i, (x, y) in enumerate(self.body):
            color = DARK_GREEN if i == 0 else GREEN

            pygame.draw.rect(screen, color, (x, y, GRID_SIZE, GRID_SIZE))

class Food:
    def __init__(self):
        self.position = self.get_random_position([])

    def get_random_position(self, snake_body):

        while True:

            new_position = (
                random.randint(0, (SCREEN_WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE,
                random.randint(0, (SCREEN_HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
            )

            if new_position not in snake_body:
                return new_position

    def respawn(self, snake_body):
        self.position = self.get_random_position(snake_body)

    def draw(self):
        pygame.draw.rect(screen, RED, (self.position[0], self.position[1], GRID_SIZE, GRID_SIZE))

def game_loop(difficulty):

    snake = Snake()
    food = Food()
    score = 0
    speed = difficulty
    running = True
    game_over = False
    win = False

    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:

                if not game_over and not win:

                    if event.key == pygame.K_UP and snake.direction != (0, GRID_SIZE):
                        snake.direction = (0, -GRID_SIZE)
                    elif event.key == pygame.K_DOWN and snake.direction != (0, -GRID_SIZE):
                        snake.direction = (0, GRID_SIZE)
                    elif event.key == pygame.K_LEFT and snake.direction != (GRID_SIZE, 0):
                        snake.direction = (-GRID_SIZE, 0)
                    elif event.key == pygame.K_RIGHT and snake.direction != (-GRID_SIZE, 0):
                        snake.direction = (GRID_SIZE, 0)

                if event.key == pygame.K_RETURN and (game_over or win):
                    game_loop(difficulty)
                    return

        if not game_over and not win:
            snake.move()

            if snake.body[0] == food.position:
                snake.grow()
                food.respawn(snake.body)

                score += 1
                speed = min(20, speed + 1)

            if snake.check_collision():
                game_over = True

            if score >= 20:
                win = True

        snake.draw()
        food.draw()

        font = pygame.font.SysFont("Arial", 25)
        text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(text, (10, 10))

        if game_over:
            game_over_text = font.render(f"Game Over! Score: {score}. Press Enter to Restart", True, WHITE)
            screen.blit(game_over_text, (SCREEN_WIDTH // 6, SCREEN_HEIGHT // 2))
        elif win:
            win_text = font.render("You Win! Press Enter to Play Again", True, BLUE)
            screen.blit(win_text, (SCREEN_WIDTH // 6, SCREEN_HEIGHT // 2))

        pygame.display.flip()
        clock.tick(speed)

    pygame.quit()

def choose_difficulty():

    screen.fill(BLACK)

    font = pygame.font.SysFont("Arial", 30)
    text = font.render("Choose Difficulty: 1-Easy, 2-Medium, 3-Hard", True, WHITE)

    screen.blit(text, (SCREEN_WIDTH // 6, SCREEN_HEIGHT // 2))
    pygame.display.flip()

    choosing = True

    while choosing:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 10
                elif event.key == pygame.K_2:
                    return 15
                elif event.key == pygame.K_3:
                    return 20
            elif event.type == pygame.QUIT:
                pygame.quit()
                return

# Запуск игры
if __name__ == "__main__":
    difficulty = choose_difficulty()
    game_loop(difficulty)