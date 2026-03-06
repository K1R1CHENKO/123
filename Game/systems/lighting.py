from dataclasses import dataclass

from Game.engine.constants import DAY_LENGTH_SECONDS
from Game.world.blocks import BLOCKS
from Game.world.world import World


@dataclass
class LightingState:
    time_of_day: float = 0.25

    def tick(self, dt: float):
        self.time_of_day = (self.time_of_day + dt / DAY_LENGTH_SECONDS) % 1.0

    @property
    def sun_intensity(self) -> float:
        t = self.time_of_day
        return max(0.2, 1.0 - abs(t - 0.5) * 1.6)


def local_light(world: World, x: int, y: int, z: int) -> int:
    best = 0
    for dx in range(-4, 5):
        for dy in range(-4, 5):
            for dz in range(-4, 5):
                b = world.get_block(x + dx, y + dy, z + dz)
                best = max(best, BLOCKS.get(b, BLOCKS["air"]).emits_light - abs(dx) - abs(dy) - abs(dz))
    return max(0, best)
