from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

from Game.ai.mob import MobSystem
from Game.optimization.streaming import ChunkStreamer
from Game.player.controller import Player
from Game.save.storage import SaveSystem
from Game.systems.audio import AudioSystem
from Game.systems.crafting import craft
from Game.systems.lighting import LightingState
from Game.systems.particles import ParticleSystem
from Game.systems.physics import simulate_falling_blocks, simulate_player
from Game.systems.weather import WeatherSystem
from Game.ui.hud import render_hud
from Game.world.world import World

HELP = """
Commands:
  w/a/s/d               move player
  break x y z           break block
  place x y z           place selected block
  select <block>        select block to place
  craft <recipe>        craft item (planks, crafting_table, torch)
  save | load | quit
"""


class GameApp:
    def __init__(self, seed: int = 4242, save_root: str = "saves/world1"):
        self.world = World(seed=seed)
        self.player = Player()
        self.save = SaveSystem(root=save_root)
        self.lighting = LightingState()
        self.weather = WeatherSystem()
        self.particles = ParticleSystem()
        self.audio = AudioSystem()
        self.mobs = MobSystem()
        self.streamer = ChunkStreamer(self.world)
        self.running = True

        self.streamer.update(self.player.x, self.player.z)
        self.mobs.spawn_near(self.world, (self.player.x, self.player.y, self.player.z), count=3)

    def tick(self, dt: float = 0.1) -> str:
        self.streamer.update(self.player.x, self.player.z)
        self.mobs.tick(self.world, (self.player.x, self.player.y, self.player.z))
        simulate_player(self.player, self.world, dt=dt)
        simulate_falling_blocks(self.world)
        self.lighting.tick(dt)
        self.weather.tick(dt)
        return render_hud(self.player, self.lighting, len(self.mobs.mobs))

    def handle_command(self, command_line: str) -> str:
        command = command_line.strip().split()
        if not command:
            return ""

        c = command[0]
        if c in {"w", "a", "s", "d"}:
            dx = 1 if c == "d" else -1 if c == "a" else 0
            dz = 1 if c == "s" else -1 if c == "w" else 0
            self.player.move(dx, dz)
            return "moved"
        if c == "break" and len(command) == 4:
            x, y, z = map(int, command[1:])
            if self.player.break_block(self.world, x, y, z):
                self.particles.spawn("block_break", x, y, z)
                self.audio.play("break")
                return "broken"
            return "cannot break"
        if c == "place" and len(command) == 4:
            x, y, z = map(int, command[1:])
            if self.player.place_block(self.world, x, y, z):
                self.particles.spawn("block_place", x, y, z)
                self.audio.play("place")
                return "placed"
            return "cannot place"
        if c == "select" and len(command) == 2:
            self.player.selected_item = command[1]
            return f"selected {command[1]}"
        if c == "craft" and len(command) == 2:
            return "crafted" if craft(self.player.inventory, command[1]) else "cannot craft"
        if c == "save":
            self.save.save(self.world, self.player)
            return "saved"
        if c == "load":
            self.save.load(self.world, self.player)
            return "loaded"
        if c == "quit":
            self.save.save(self.world, self.player)
            self.running = False
            return "bye"
        return HELP.strip()


def _iter_script_commands(path: str | None) -> Iterable[str]:
    if not path:
        return []
    return [
        line.strip()
        for line in Path(path).read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]


def run_interactive(seed: int = 4242, save_root: str = "saves/world1") -> None:
    app = GameApp(seed=seed, save_root=save_root)
    print("Voxel Sandbox Prototype ready.")
    print(HELP)

    while app.running:
        hud = app.tick(dt=0.1)
        print(hud, f"Weather={app.weather.state}")
        print(app.handle_command(input("> ")))


def run_script(script_path: str, seed: int = 4242, save_root: str = "saves/world1", max_ticks: int = 120) -> int:
    app = GameApp(seed=seed, save_root=save_root)
    commands = list(_iter_script_commands(script_path))

    for i in range(max_ticks):
        hud = app.tick(dt=0.1)
        if i < len(commands):
            result = app.handle_command(commands[i])
            print(f"[{i:03}] cmd={commands[i]!r} -> {result}")
        else:
            print(f"[{i:03}] idle")
        print(hud, f"Weather={app.weather.state}")
        if not app.running:
            print("Script run finished by quit command.")
            return 0

    print("Max ticks reached.")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Educational Minecraft-style sandbox prototype")
    parser.add_argument("--script", type=str, default=None, help="Path to command script for non-interactive run")
    parser.add_argument("--max-ticks", type=int, default=120, help="Max ticks for --script mode")
    parser.add_argument("--seed", type=int, default=4242, help="World seed")
    parser.add_argument("--save-root", type=str, default="saves/world1", help="Save directory")
    return parser.parse_args()


def run() -> int:
    args = parse_args()
    if args.script:
        return run_script(args.script, seed=args.seed, save_root=args.save_root, max_ticks=args.max_ticks)
    run_interactive(seed=args.seed, save_root=args.save_root)
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
