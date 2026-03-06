from dataclasses import dataclass
import random

from Game.world.world import World


@dataclass
class Mob:
    kind: str
    x: int
    y: int
    z: int
    hp: int = 10

    def tick(self, world: World, player_pos: tuple[int, int, int]):
        px, _, pz = player_pos
        dx = 1 if px > self.x else -1 if px < self.x else 0
        dz = 1 if pz > self.z else -1 if pz < self.z else 0
        if abs(px - self.x) + abs(pz - self.z) < 8:
            self._try_move(world, dx, dz)
        else:
            self._try_move(world, random.choice([-1, 0, 1]), random.choice([-1, 0, 1]))

    def _try_move(self, world: World, dx: int, dz: int):
        nx, nz = self.x + dx, self.z + dz
        if world.get_block(nx, self.y - 1, nz) != "air" and world.get_block(nx, self.y, nz) == "air":
            self.x, self.z = nx, nz


class MobSystem:
    def __init__(self):
        self.mobs: list[Mob] = []

    def spawn_near(self, world: World, center: tuple[int, int, int], count: int = 2):
        cx, cy, cz = center
        for i in range(count):
            m = Mob("slime", cx + i * 3 + 4, cy, cz + i * 2 + 3)
            self.mobs.append(m)

    def tick(self, world: World, player_pos: tuple[int, int, int]):
        for mob in self.mobs:
            mob.tick(world, player_pos)
