from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Tuple

from Game.engine.constants import CHUNK_HEIGHT, CHUNK_SIZE

VoxelPos = Tuple[int, int, int]


@dataclass
class Chunk:
    cx: int
    cz: int
    blocks: Dict[VoxelPos, str] = field(default_factory=dict)
    dirty: bool = True

    def _in_bounds(self, x: int, y: int, z: int) -> bool:
        return 0 <= x < CHUNK_SIZE and 0 <= z < CHUNK_SIZE and 0 <= y < CHUNK_HEIGHT

    def set_block(self, x: int, y: int, z: int, block_id: str) -> None:
        if not self._in_bounds(x, y, z):
            return
        key = (x, y, z)
        if block_id == "air":
            self.blocks.pop(key, None)
        else:
            self.blocks[key] = block_id
        self.dirty = True

    def get_block(self, x: int, y: int, z: int) -> str:
        if not self._in_bounds(x, y, z):
            return "air"
        return self.blocks.get((x, y, z), "air")

    def serialize(self) -> dict:
        return {
            "cx": self.cx,
            "cz": self.cz,
            "blocks": [[x, y, z, b] for (x, y, z), b in self.blocks.items()],
        }

    @classmethod
    def deserialize(cls, data: dict) -> "Chunk":
        c = cls(data["cx"], data["cz"])
        for x, y, z, block in data["blocks"]:
            c.blocks[(x, y, z)] = block
        return c
