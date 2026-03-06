from dataclasses import dataclass


@dataclass
class ParticleEvent:
    kind: str
    x: int
    y: int
    z: int


class ParticleSystem:
    def __init__(self):
        self.events: list[ParticleEvent] = []

    def spawn(self, kind: str, x: int, y: int, z: int):
        self.events.append(ParticleEvent(kind, x, y, z))

    def flush(self):
        self.events.clear()
