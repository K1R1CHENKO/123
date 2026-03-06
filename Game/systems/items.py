from dataclasses import dataclass


@dataclass(frozen=True)
class ItemDef:
    id: str
    place_block: str | None = None


ITEMS = {
    "dirt": ItemDef("dirt", place_block="dirt"),
    "stone": ItemDef("stone", place_block="stone"),
    "log": ItemDef("log", place_block="log"),
    "planks": ItemDef("planks", place_block="wood_planks"),
    "torch": ItemDef("torch", place_block="torch"),
    "crafting_table": ItemDef("crafting_table", place_block="crafting_table"),
}
