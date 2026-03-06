import math
import random


def _hash(x: int, z: int, seed: int) -> float:
    r = random.Random((x * 92837111) ^ (z * 689287499) ^ seed)
    return r.uniform(-1.0, 1.0)


def value_noise_2d(x: float, z: float, seed: int = 1337) -> float:
    x0, z0 = math.floor(x), math.floor(z)
    x1, z1 = x0 + 1, z0 + 1
    sx, sz = x - x0, z - z0

    n00 = _hash(x0, z0, seed)
    n10 = _hash(x1, z0, seed)
    n01 = _hash(x0, z1, seed)
    n11 = _hash(x1, z1, seed)

    ix0 = n00 + (n10 - n00) * _smoothstep(sx)
    ix1 = n01 + (n11 - n01) * _smoothstep(sx)
    return ix0 + (ix1 - ix0) * _smoothstep(sz)


def fractal_noise_2d(x: float, z: float, octaves: int = 4, persistence: float = 0.5, lacunarity: float = 2.0, seed: int = 1337) -> float:
    total, amplitude, frequency = 0.0, 1.0, 1.0
    max_amp = 0.0
    for i in range(octaves):
        total += value_noise_2d(x * frequency, z * frequency, seed + i * 113) * amplitude
        max_amp += amplitude
        amplitude *= persistence
        frequency *= lacunarity
    return total / max_amp if max_amp else 0.0


def _smoothstep(t: float) -> float:
    return t * t * (3 - 2 * t)
