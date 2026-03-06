from dataclasses import dataclass

from Game.engine.constants import PLAYER_REACH
from Game.systems.inventory import Inventory
from Game.world.blocks import BLOCKS
from Game.world.world import World


@dataclass
class Player:
    x: int = 0
    y: int = 40
    z: int = 0
    vy: float = 0.0

    def __post_init__(self):
        self.inventory = Inventory()
        self.selected_item = "dirt"

    def move(self, dx: int, dz: int):
        self.x += dx
        self.z += dz

    def break_block(self, world: World, tx: int, ty: int, tz: int):
        if abs(tx - self.x) + abs(ty - self.y) + abs(tz - self.z) > PLAYER_REACH:
            return False
        block = world.get_block(tx, ty, tz)
        if block == "air":
            return False
        world.set_block(tx, ty, tz, "air")
        self.inventory.add(block, 1)
        return True

    def place_block(self, world: World, tx: int, ty: int, tz: int):
        block = self.selected_item
        if block not in BLOCKS:
            return False
        if not self.inventory.has(block):
            return False
        if world.get_block(tx, ty, tz) != "air":
            return False
        world.set_block(tx, ty, tz, block)
        self.inventory.remove(block, 1)
        return True
