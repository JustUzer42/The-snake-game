import random

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
    """Базовый класс игрового объекта.

    Содержит общие атрибуты позиции и цвета, а также заготовку
    метода для отрисовки на игровом поле.
    """

    def __init__(self, position=None, body_color=None):
        """Инициализация базового атрибута объекта.

        Args:
            position: Позиция объекта на игровом поле.
            body_color: Цвет объекта в формате RGB-кортежа.
        """
        self.position = position
        self.body_color = body_color

    def draw(self, screen):
        """Отрисовать объект на игровом поле.

        Абстрактный метод, должен быть переопределён в дочерних классах.

        Args:
            screen: Surface Pygame для отрисовки.
        """
        pass


class Apple(GameObject):
    """Класс, описывающий яблоко на игровом поле.

    Наследуется от GameObject. Яблоко отображается в случайных
    клетках игрового поля и отрисовывается красным цветом.
    """

    def __init__(self):
        """Инициализация яблока с красным цветом и случайной позицией."""
        self.body_color = APPLE_COLOR
        self.position = None
        self.randomize_position()

    def randomize_position(self):
        """Установить случайное положение яблока на игровом поле.

        Координаты выбираются так, чтобы яблоко оказалось в пределах
        игрового поля, выровненное по сетке.
        """
        grid_x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
        grid_y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (grid_x, grid_y)

    def draw(self, screen):
        """Отрисовать яблоко на игровой поверхности.

        Рисует заполненный квадрат цвета яблока с цветной границей.

        Args:
            screen: Surface Pygame для отрисовки.
        """
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, описывающий змейку и её поведение.

    Наследуется от GameObject. Управляет движением, отрисовкой,
    а также обрабатывает действия пользователя.
    """

    def __init__(self):
        """Инициализация начального состояния змейки.

        Змейка начинается с одного сегмента в центре экрана,
        движется вправо.
        """
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        super().__init__(
            position=(center_x, center_y), body_color=SNAKE_COLOR
        )

        self.length = 1
        self.positions = [(center_x, center_y)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Обновить направление движения змейки.

        Применяет следующее направление (next_direction) к текущему
        (direction) и сбрасывает next_direction в None.
        """
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновить позицию змейки.

        Вычисляет новую позицию головы на основе текущего направления,
        вставляет её в начало списка позиций. Если длина змейки не
        увеличилась, удаляет последний сегмент (имитация движения).
        Сохраняет позицию стираемого сегмента в self.last.
        """
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
        """Отрисовать змейку на экране.

        Рисует все сегменты тела и голову змейки. Затем затирает
        последний сегмент цветом фона, чтобы имитировать движение.

        Args:
            screen: Surface Pygame для отрисовки.
        """
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(
            screen, BORDER_COLOR, head_rect, 1
        )

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвратить позицию головы змейки.

        Returns:
            Кортеж (x, y) координат головы змейки.
        """
        return self.positions[0]

    def reset(self):
        """Сбросить змейку в начальное состояние.

        Сбрасывает длину до 1, позицию в центр экрана,
        направление на случайное из четырёх возможных.
        """
        self.length = 1
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        self.positions = [(center_x, center_y)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.last = None


def handle_keys(game_object):
    """Обработать события клавиатуры.

    Обрабатывает нажатие стрелок для изменения направления змейки.
    Запрещает разворот на 180 градусов. При закрытии окна завершает игру.

    Args:
        game_object: Объект змейки для обновления направления.
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
            elif (
                event.key == pygame.K_LEFT
                and game_object.direction != RIGHT
            ):
                game_object.next_direction = LEFT
            elif (
                event.key == pygame.K_RIGHT
                and game_object.direction != LEFT
            ):
                game_object.next_direction = RIGHT


def main():
    """Основной цикл игры.

    Создаёт объекты змейки и яблока, затем в бесконечном цикле
    обрабатывает ввод, обновляет состояние, проверяет столкновения
    и отрисовывает игровое поле.
    """
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # Проверка: съела ли змейка яблоко
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        # Проверка: столкновение змейки с собой
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        # Отрисовка
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw(screen)
        snake.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()
