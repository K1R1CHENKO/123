from Game.engine.constants import RENDER_DISTANCE
from Game.world.world import World


class ChunkStreamer:
    def __init__(self, world: World):
        self.world = world

    def update(self, player_x: int, player_z: int):
        pcx, pcz = player_x // 16, player_z // 16
        needed = set()
        for dx in range(-RENDER_DISTANCE, RENDER_DISTANCE + 1):
            for dz in range(-RENDER_DISTANCE, RENDER_DISTANCE + 1):
                needed.add((pcx + dx, pcz + dz))
                self.world.ensure_chunk(pcx + dx, pcz + dz)

        for key in list(self.world.chunks.keys()):
            if key not in needed:
                del self.world.chunks[key]
