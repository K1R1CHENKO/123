class Inventory:
    def __init__(self, slots: int = 36):
        self.slots = slots
        self.items: dict[str, int] = {}

    def add(self, item: str, count: int = 1) -> None:
        self.items[item] = self.items.get(item, 0) + count

    def remove(self, item: str, count: int = 1) -> bool:
        current = self.items.get(item, 0)
        if current < count:
            return False
        new = current - count
        if new == 0:
            self.items.pop(item, None)
        else:
            self.items[item] = new
        return True

    def has(self, item: str, count: int = 1) -> bool:
        return self.items.get(item, 0) >= count
