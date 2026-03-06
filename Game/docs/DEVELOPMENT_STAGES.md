# Этап 1: Архитектура

1. Краткое объяснение: проект разбит на модули `engine/world/player/systems/ai/ui/save/optimization/network`.
2. Архитектура файлов:

```text
Game/
 ├── engine/
 ├── world/
 ├── player/
 ├── systems/
 ├── ai/
 ├── ui/
 ├── optimization/
 ├── save/
 ├── network/
 ├── main.py
 ├── docs/
 └── ...
scripts/
 └── smoke_commands.txt
tests/
 └── test_smoke.py
```

3. Полный код: см. файлы в репозитории.
4. Как это работает: `GameApp` в `main.py` связывает системы и запускает игровой цикл.
5. Переход к следующему этапу: Core Engine.

# Этап 2: Core Engine

- Воксельная модель: `world/chunk.py`, `world/blocks.py`.
- Chunk-система и стриминг: `world/world.py`, `optimization/streaming.py`.
- Генерация и шумы: `engine/noise.py`, `world/generator.py`.

# Этап 3: Генерация мира

- Биомы: `biome_at()`.
- Пещеры: cave-mask в `generate_chunk()`.
- Руды: `_ore_or_stone()`.
- Деревья и структуры: `_place_tree()`, `_place_ruin()`.

# Этап 4: Игровые системы

- FPS-like управление (CLI-прототип): `player/controller.py`.
- Разрушение/установка блоков: `break_block()`/`place_block()`.
- Инвентарь и крафт: `systems/inventory.py`, `systems/crafting.py`.

# Этап 5: Мобы и AI

- `ai/mob.py`: базовый моб, преследование игрока, спавн.

# Этап 6: Физика

- Гравитация игрока: `simulate_player()`.
- Падение блоков: `simulate_falling_blocks()`.

# Этап 7: Освещение

- Дневной цикл: `LightingState`.
- Блок-свет: `local_light()`.

# Этап 8: UI

- Текстовый HUD: `ui/hud.py`.

# Этап 9: Сохранение

- Save/load чанков и игрока: `save/storage.py`.

# Этап 10: Оптимизация

- Chunk streaming + выгрузка дальних чанков.

# Этап 11: Дополнительные системы

- Звук: `systems/audio.py`.
- Частицы: `systems/particles.py`.
- Погода: `systems/weather.py`.
- Мультиплеер-заглушка: `network/server.py`.

# Этап 12: Тестируемость и DX

- `--script` и `--max-ticks` в `main.py` позволяют стабильно запускать симуляцию без интерактива.
- `scripts/smoke_commands.txt` — готовый сценарий ручного и CI smoke-теста.
- `tests/test_smoke.py` проверяет запуск, выход и запись save-файлов.
