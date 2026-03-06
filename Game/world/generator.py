from __future__ import annotations
import random

from Game.engine.constants import CHUNK_HEIGHT, CHUNK_SIZE, ORE_TABLE
from Game.engine.noise import fractal_noise_2d
from Game.world.blocks import BLOCKS
from Game.world.chunk import Chunk


class WorldGenerator:
    def __init__(self, seed: int = 1337):
        self.seed = seed

    def biome_at(self, wx: int, wz: int) -> str:
        n = fractal_noise_2d(wx / 128.0, wz / 128.0, seed=self.seed + 77)
        if n < -0.25:
            return "desert"
        if n > 0.35:
            return "mountains"
        return "plains"

    def surface_height(self, wx: int, wz: int, biome: str) -> int:
        base = 26
        if biome == "mountains":
            amp = 22
        elif biome == "desert":
            amp = 8
        else:
            amp = 12
        h = base + int((fractal_noise_2d(wx / 52.0, wz / 52.0, seed=self.seed) + 1) * 0.5 * amp)
        return max(4, min(CHUNK_HEIGHT - 2, h))

    def generate_chunk(self, cx: int, cz: int) -> Chunk:
        ch = Chunk(cx, cz)
        rng = random.Random((cx * 92821) ^ (cz * 31847) ^ self.seed)

        for lx in range(CHUNK_SIZE):
            for lz in range(CHUNK_SIZE):
                wx = cx * CHUNK_SIZE + lx
                wz = cz * CHUNK_SIZE + lz
                biome = self.biome_at(wx, wz)
                h = self.surface_height(wx, wz, biome)

                for y in range(0, h + 1):
                    cave = fractal_noise_2d(wx / 26.0, (wz + y) / 26.0, seed=self.seed + y)
                    if y > 5 and cave > 0.62:
                        continue

                    if y == h:
                        top = "sand" if biome == "desert" else "grass"
                        ch.set_block(lx, y, lz, top)
                    elif y > h - 4:
                        ch.set_block(lx, y, lz, "sand" if biome == "desert" else "dirt")
                    else:
                        ch.set_block(lx, y, lz, self._ore_or_stone(y, rng))

                if biome != "desert" and rng.random() < 0.03:
                    self._place_tree(ch, lx, h + 1, lz)

                if rng.random() < 0.004:
                    self._place_ruin(ch, lx, h + 1, lz)
        return ch

    def _ore_or_stone(self, y: int, rng: random.Random) -> str:
        for ore, rules in ORE_TABLE.items():
            if rules["min_y"] <= y <= rules["max_y"] and rng.random() < rules["chance"]:
                return ore
        return "stone"

    def _place_tree(self, ch: Chunk, x: int, y: int, z: int) -> None:
        height = 4
        for i in range(height):
            ch.set_block(x, y + i, z, "log")
        for dx in range(-2, 3):
            for dz in range(-2, 3):
                for dy in range(2, 5):
                    if abs(dx) + abs(dz) < 4:
                        ch.set_block(x + dx, y + dy, z + dz, "leaves")

    def _place_ruin(self, ch: Chunk, x: int, y: int, z: int) -> None:
        for dx in range(0, 3):
            for dz in range(0, 3):
                ch.set_block(x + dx, y, z + dz, "stone")
        ch.set_block(x + 1, y + 1, z + 1, "torch")
