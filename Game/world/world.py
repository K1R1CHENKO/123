from __future__ import annotations
from typing import Dict, Tuple

from Game.engine.constants import CHUNK_SIZE
from Game.world.chunk import Chunk
from Game.world.generator import WorldGenerator


class World:
    def __init__(self, seed: int = 1337):
        self.seed = seed
        self.generator = WorldGenerator(seed)
        self.chunks: Dict[Tuple[int, int], Chunk] = {}

    def _chunk_coords(self, wx: int, wz: int) -> Tuple[int, int, int, int]:
        cx = wx // CHUNK_SIZE
        cz = wz // CHUNK_SIZE
        lx = wx % CHUNK_SIZE
        lz = wz % CHUNK_SIZE
        return cx, cz, lx, lz

    def ensure_chunk(self, cx: int, cz: int) -> Chunk:
        if (cx, cz) not in self.chunks:
            self.chunks[(cx, cz)] = self.generator.generate_chunk(cx, cz)
        return self.chunks[(cx, cz)]

    def get_block(self, wx: int, y: int, wz: int) -> str:
        cx, cz, lx, lz = self._chunk_coords(wx, wz)
        ch = self.ensure_chunk(cx, cz)
        return ch.get_block(lx, y, lz)

    def set_block(self, wx: int, y: int, wz: int, block_id: str) -> None:
        cx, cz, lx, lz = self._chunk_coords(wx, wz)
        ch = self.ensure_chunk(cx, cz)
        ch.set_block(lx, y, lz, block_id)

    def chunk_positions(self):
        return list(self.chunks.keys())
