# Minecraft-style Sandbox (Educational Prototype)

## Quick start

```bash
python -m Game.main
```

## Non-interactive test run (recommended)

```bash
python -m Game.main --script scripts/smoke_commands.txt --max-ticks 20 --save-root /tmp/voxel_save
```

This mode is made for CI/local smoke checks: it executes commands from a file and exits automatically.

## Run tests

```bash
python -m unittest discover -s tests -p 'test_*.py'
```

## Notes

- Prototype is fully Python-stdlib and demonstrates modular architecture.
- See `Game/docs/DEVELOPMENT_STAGES.md` for stage-by-stage mapping.
