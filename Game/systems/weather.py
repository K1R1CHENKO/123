import random


class WeatherSystem:
    def __init__(self):
        self.state = "clear"
        self.timer = 0.0

    def tick(self, dt: float):
        self.timer += dt
        if self.timer > 60:
            self.timer = 0
            self.state = random.choice(["clear", "rain", "storm"])
