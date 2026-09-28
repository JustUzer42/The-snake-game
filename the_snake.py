import random
import sys

import pygame as pg


# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Начальная позиция змейки:
SNAKE_START_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - чёрный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Инициализация PyGame:
pg.init()

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Базовый класс игрового объекта."""

    def __init__(self, position=None, body_color=None):
        """Инициализация базового атрибута объекта."""
        self.position = position
        self.body_color = body_color

    def draw_cell(self, screen, position, cell_color,
                  border_color=BORDER_COLOR):
        """Отрисовать одну ячейку с указанными цветами."""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, cell_color, rect)
        pg.draw.rect(screen, border_color, rect, 1)

    def draw(self, screen):
        """Отрисовать объект на игровом поле."""


class Apple(GameObject):
    """Класс, описывающий яблоко на игровом поле."""

    def __init__(self, body_color=APPLE_COLOR):
        """Инициализация яблока с цветом и случайной позицией."""
        super().__init__(body_color=body_color)
        self.randomize_position()

    def randomize_position(self, occupied_positions=None):
        """Установить случайное положение яблока на игровом поле."""
        while True:
            grid_x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
            grid_y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            self.position = (grid_x, grid_y)
            if occupied_positions is None or \
                    self.position not in occupied_positions:
                break

    def draw(self, screen):
        """Отрисовать яблоко на игровой поверхности."""
        self.draw_cell(screen, self.position, self.body_color)


class Snake(GameObject):
    """Класс, описывающий змейку и её поведение."""

    def _init_state(self):
        """Инициализация общего состояния змейки."""
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def __init__(self, body_color=SNAKE_COLOR, position=SNAKE_START_POSITION):
        """Инициализация начального состояния змейки."""
        super().__init__(position=position, body_color=body_color)
        self.positions = [self.position]
        self._init_state()

    def update_direction(self):
        """Обновить направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновить позицию змейки."""
        self.last = self.positions[-1] if self.positions else None

        head = self.get_head_position()
        dx, dy = self.direction

        new_x = (head[0] + dx * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head[1] + dy * GRID_SIZE) % SCREEN_HEIGHT

        new_head = (new_x, new_y)
        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self, screen):
        """Отрисовать змейку на экране."""
        for position in self.positions:
            self.draw_cell(screen, position, self.body_color)
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвратить позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбросить змейку в начальное состояние."""
        screen.fill(BOARD_BACKGROUND_COLOR)
        self.positions = [SNAKE_START_POSITION]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self._init_state()


# Маппинг клавиш: клавиша -> (новое_направление, запрещённое_направление)
TURNS = {
    pg.K_UP: (UP, DOWN),
    pg.K_DOWN: (DOWN, UP),
    pg.K_LEFT: (LEFT, RIGHT),
    pg.K_RIGHT: (RIGHT, LEFT),
}


def handle_keys(game_object):
    """Обработать события клавиатуры."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                sys.exit()
            elif event.key in TURNS:
                new_direction, opposite = TURNS[event.key]
                if game_object.direction != opposite:
                    game_object.next_direction = new_direction


def main():
    """Основной цикл игры."""
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # Проверка: съела ли змейка яблоко или столкнулась с собой
        head = snake.get_head_position()
        if head == apple.position:
            snake.length += 1
            apple.randomize_position(occupied_positions=snake.positions[:-1])
        elif head in snake.positions[4:]:
            snake.reset()
            apple.randomize_position(occupied_positions=snake.positions)

        # Отрисовка
        apple.draw(screen)
        snake.draw(screen)
        pg.display.update()


if __name__ == '__main__':
    main()
