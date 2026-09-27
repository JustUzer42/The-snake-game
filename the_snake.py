from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

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
pygame.init()

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, position=None, body_color=None):
        """Инициализация базовых атрибутов объекта.

        Args:
            position: Позиция объекта на игровом поле. По умолчанию — центр экрана.
            body_color: Цвет объекта в формате RGB. По умолчанию — SNAKE_COLOR.
        """
        if position is None:
            position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        if body_color is None:
            body_color = SNAKE_COLOR

        self.position = position
        self.body_color = body_color

    def draw(self):
        """Отрисовка объекта на экране. Переопределяется в дочерних классах."""
        pass


class Apple(GameObject):
    """Класс для яблока на игровом поле."""

    def __init__(self, position=None, body_color=APPLE_COLOR):
        """Инициализация яблока.

        Args:
            position: Позиция яблока. По умолчанию — случайная позиция.
            body_color: Цвет яблока (красный по умолчанию).
        """
        super().__init__(position, body_color)
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайное положение яблока на игровом поле."""
        x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (x, y)

    def draw(self):
        """Отрисовка яблока на игровой поверхности."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс для змейки на игровом поле."""

    def __init__(self, position=None, body_color=SNAKE_COLOR):
        """Инициализация змейки.

        Args:
            position: Начальная позиция головы змейки. По умолчанию — центр экрана.
            body_color: Цвет змейки (зелёный по умолчанию).
        """
        super().__init__(position, body_color)
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        """Возвращает позицию головы змейки.

        Returns:
            Кортеж с координатами головы змейки.
        """
        return self.positions[0]

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            # Запрет разворота на 180 градусов
            if self.next_direction[0] + self.direction[0] != 0 or \
               self.next_direction[1] + self.direction[1] != 0:
                self.direction = self.next_direction
                self.next_direction = None

    def move(self):
        """Обновляет позицию змейки, двигая её в текущем направлении."""
        head = self.get_head_position()
        dx = self.direction[0] * GRID_SIZE
        dy = self.direction[1] * GRID_SIZE

        new_x = (head[0] + dx) % SCREEN_WIDTH
        new_y = (head[1] + dy) % SCREEN_HEIGHT

        new_head = (new_x, new_y)

        self.last = self.positions[-1] if self.positions else None
        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        """Отрисовка змейки на экране."""
        # Затирание следа
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

        # Отрисовка тела змейки
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None


def handle_keys(game_object):
    """Обрабатывает события клавиш для управления змейкой.

    Args:
        game_object: Объект змейки для управления направлением.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная функция игры. Запускает игровой цикл."""
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)

        # Очистка экрана
        screen.fill(BOARD_BACKGROUND_COLOR)

        # Обработка нажатий клавиш
        handle_keys(snake)

        # Обновление направления
        snake.update_direction()

        # Движение змейки
        snake.move()

        # Проверка столкновения с яблоком
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        # Проверка столкновения с собой
        if len(snake.positions) > len(set(snake.positions)):
            snake.reset()

        # Отрисовка объектов
        snake.draw()
        apple.draw()

        # Обновление экрана
        pygame.display.update()


if __name__ == '__main__':
    main()
