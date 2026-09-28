# Анализ задания «Изгиб Питона» (Змейка)

## Источник
`info/Змейка.html` — страница урока Яндекс Практикум.

## Что необходимо реализовать

### 1. Класс `GameObject`
**Атрибуты:**
- `position` — позиция на игровом поле (центр экрана)
- `body_color` — цвет объекта (RGB), определяется в дочерних классах

**Методы:**
- `__init__(self, position=None, body_color=None)` — инициализация атрибутов
- `draw(self, screen)` — абстрактный метод, `pass` по умолчанию

### 2. Класс `Apple` (наследуется от `GameObject`)
**Атрибуты:**
- `body_color` — `(255, 0, 0)` (красный)
- `position` — случайная позиция на поле

**Методы:**
- `__init__(self)` — задаёт цвет, вызывает `randomize_position()`
- `randomize_position(self)` — случайная позиция в пределах сетки
- `draw(self, screen)` — рисует красный квадрат с цветной границей

### 3. Класс `Snake` (наследуется от `GameObject`)
**Атрибуты:**
- `length` — начальная длина = 1
- `positions` — список координат сегментов, начальная — центр экрана
- `direction` — начальное направление = вправо `(1, 0)`
- `next_direction` — следующее направление = `None`
- `body_color` — `(0, 255, 0)` (зелёный)
- `last` — позиция последнего сегмента для стирания = `None`

**Методы:**
- `__init__(self)` — инициализация начального состояния
- `update_direction(self)` — применяет `next_direction` к `direction`
- `move(self)` — вычисляет новую голову, insert/pop, обновляет `last`
- `draw(self, screen)` — рисует все сегменты + голову, затирает `last`
- `get_head_position(self)` — возвращает `positions[0]`
- `reset(self)` — сброс: длина=1, позиция центр, направление случайное

### 4. Функция `handle_keys(game_object)`
- Обработка `pygame.QUIT` → `pygame.quit()`, `raise SystemExit`
- Обработка стрелок с запретом разворота на 180°

### 5. Функция `main()`
```
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

## Дополнительные требования
- Все классы и методы должны содержать docstrings
- Код должен соответствовать PEP 8
- Игра должна запускаться и работать без ошибок

## Дополнительные опции (не проверяются)
- Настройка цветов и скорости
- «Неправильная» еда (уменьшает длину)
- Препятствия в виде «камней»
