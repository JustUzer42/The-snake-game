# Задание для агента: Реализация игры «Изгиб Питона» (Змейка)

## Текущее состояние

### Реализовано (прекод в `the_snake.py`):
- **Константы:** `SCREEN_WIDTH=640`, `SCREEN_HEIGHT=480`, `GRID_SIZE=20`, `GRID_WIDTH`, `GRID_HEIGHT`
- **Направления:** `UP=(0,-1)`, `DOWN=(0,1)`, `LEFT=(-1,0)`, `RIGHT=(1,0)`
- **Цвета:** `BOARD_BACKGROUND_COLOR=(0,0,0)`, `BORDER_COLOR=(93,216,228)`, `APPLE_COLOR=(255,0,0)`, `SNAKE_COLOR=(0,255,0)`
- **Скорость:** `SPEED=20`
- **Pygame:** `screen`, `clock`, `pygame.display.set_caption('Змейка')`

### Не реализовано (заглушки `...`):
- Класс `GameObject` — отсутствует
- Класс `Apple` — отсутствует
- Класс `Snake` — отсутствует
- Функция `main()` — пустая
- Функция `handle_keys()` — отсутствует

### Тесты:
- `tests/test_code_structure.py` — 36 тестов на структуру классов и модуля
- `tests/test_main.py` — 1 тест на запуск `main()` без исключений (таймаут 1с)
- `tests/conftest.py` — фикстуры и защита от бесконечных циклов

---

## Что нужно сделать

### Заменить заглушки `...` на полную реализацию:

### 1. Класс `GameObject`
```python
class GameObject:
    """Базовый класс игрового объекта."""

    def __init__(self, position=None, body_color=None):
        self.position = position
        self.body_color = body_color

    def draw(self, screen):
        pass
```

### 2. Класс `Apple`
```python
class Apple(GameObject):
    """Яблоко на игровом поле."""

    def __init__(self):
        self.body_color = APPLE_COLOR
        self.position = None
        self.randomize_position()

    def randomize_position(self):
        grid_x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        grid_y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (grid_x, grid_y)

    def draw(self, screen):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
```

### 3. Класс `Snake`
```python
class Snake(GameObject):
    """Змейка — управляемый игроком объект."""

    def __init__(self):
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        super().__init__(position=(center_x, center_y), body_color=SNAKE_COLOR)
        self.length = 1
        self.positions = [(center_x, center_y)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
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
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        return self.positions[0]

    def reset(self):
        self.length = 1
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        self.positions = [(center_x, center_y)]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.last = None
```

### 4. Функция `handle_keys`
```python
def handle_keys(game_object):
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
```

### 5. Функция `main`
```python
def main():
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw(screen)
        snake.draw(screen)
        pygame.display.update()
```

---

## Требования к коду
1. **Docstrings** — все классы и публичные методы должны содержать docstrings
2. **PEP 8** — код должен проходить `flake8` без ошибок
3. **Тесты** — все 37 тестов должны проходить

---

## Файл для модификации
- `the_snake.py` — полный ребейд (замена заглушек `...` на реализацию)

## Файлы для чтения (не изменять)
- `tests/test_code_structure.py` — структура тестов
- `tests/test_main.py` — тест main
- `tests/conftest.py` — фикстуры

---

## Команды для верификации
```powershell
python -m flake8 "D:/GIGA projects/snake/the_snake.py"
python -m pytest "D:/GIGA projects/snake/tests/" -v
```

Ожидаемый результат: flake8 — 0 ошибок, pytest — 37 passed.
