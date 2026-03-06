from dataclasses import dataclass


@dataclass(frozen=True)
class BlockDef:
    id: str
    solid: bool
    transparent: bool = False
    emits_light: int = 0
    break_time: float = 0.2


BLOCKS = {
    "air": BlockDef("air", solid=False, transparent=True),
    "grass": BlockDef("grass", solid=True),
    "dirt": BlockDef("dirt", solid=True),
    "stone": BlockDef("stone", solid=True),
    "sand": BlockDef("sand", solid=True),
    "log": BlockDef("log", solid=True),
    "leaves": BlockDef("leaves", solid=True, transparent=True),
    "water": BlockDef("water", solid=False, transparent=True),
    "coal_ore": BlockDef("coal_ore", solid=True),
    "iron_ore": BlockDef("iron_ore", solid=True),
    "gold_ore": BlockDef("gold_ore", solid=True),
    "diamond_ore": BlockDef("diamond_ore", solid=True),
    "torch": BlockDef("torch", solid=False, transparent=True, emits_light=14),
    "wood_planks": BlockDef("wood_planks", solid=True),
    "crafting_table": BlockDef("crafting_table", solid=True),
}


FALLING_BLOCKS = {"sand"}
