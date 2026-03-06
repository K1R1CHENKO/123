from Game.engine.constants import GRAVITY
from Game.player.controller import Player
from Game.world.blocks import FALLING_BLOCKS
from Game.world.world import World


def simulate_player(player: Player, world: World, dt: float) -> None:
    player.vy += GRAVITY * dt
    ny = player.y + int(player.vy * dt)
    if world.get_block(player.x, max(0, ny - 1), player.z) == "air":
        player.y = max(1, ny)
    else:
        player.vy = 0.0


def simulate_falling_blocks(world: World) -> None:
    for (cx, cz) in world.chunk_positions():
        ch = world.ensure_chunk(cx, cz)
        moved = []
        for (x, y, z), block in list(ch.blocks.items()):
            if block in FALLING_BLOCKS and y > 0 and ch.get_block(x, y - 1, z) == "air":
                moved.append((x, y, z, block))
        for x, y, z, block in moved:
            ch.set_block(x, y, z, "air")
            ch.set_block(x, y - 1, z, block)
