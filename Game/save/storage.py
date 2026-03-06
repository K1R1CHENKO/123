import json
from pathlib import Path

from Game.player.controller import Player
from Game.world.chunk import Chunk
from Game.world.world import World


class SaveSystem:
    def __init__(self, root: str = "saves/world1"):
        self.root = Path(root)
        self.chunks_dir = self.root / "chunks"
        self.chunks_dir.mkdir(parents=True, exist_ok=True)

    def _player_payload(self, player: Player) -> dict:
        return {
            "x": player.x,
            "y": player.y,
            "z": player.z,
            "vy": player.vy,
            "selected_item": player.selected_item,
            "inventory": dict(player.inventory.items),
        }

    def save(self, world: World, player: Player):
        (self.root / "player.json").write_text(
            json.dumps(self._player_payload(player), indent=2), encoding="utf-8"
        )
        for (cx, cz), chunk in world.chunks.items():
            path = self.chunks_dir / f"{cx}_{cz}.json"
            path.write_text(json.dumps(chunk.serialize()), encoding="utf-8")

    def load(self, world: World, player: Player):
        p = self.root / "player.json"
        if p.exists():
            data = json.loads(p.read_text(encoding="utf-8"))
            player.x, player.y, player.z = data["x"], data["y"], data["z"]
            player.vy = data.get("vy", 0.0)
            player.selected_item = data.get("selected_item", "dirt")
            player.inventory.items = dict(data.get("inventory", {}))
        for file in self.chunks_dir.glob("*.json"):
            chunk = Chunk.deserialize(json.loads(file.read_text(encoding="utf-8")))
            world.chunks[(chunk.cx, chunk.cz)] = chunk
