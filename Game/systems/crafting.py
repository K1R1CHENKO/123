from dataclasses import dataclass
from typing import Dict

from Game.systems.inventory import Inventory


@dataclass(frozen=True)
class Recipe:
    ingredients: Dict[str, int]
    result: str
    amount: int


RECIPES = {
    "planks": Recipe({"log": 1}, "planks", 4),
    "crafting_table": Recipe({"planks": 4}, "crafting_table", 1),
    "torch": Recipe({"planks": 1, "coal_ore": 1}, "torch", 4),
}


def craft(inventory: Inventory, recipe_id: str) -> bool:
    recipe = RECIPES.get(recipe_id)
    if not recipe:
        return False
    if not all(inventory.has(i, c) for i, c in recipe.ingredients.items()):
        return False
    for i, c in recipe.ingredients.items():
        inventory.remove(i, c)
    inventory.add(recipe.result, recipe.amount)
    return True
