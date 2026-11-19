"""Cherenkov thresholds and emission angles for common radiator materials.

A charged particle emits Cherenkov light when beta > 1/n. The threshold kinetic
energy is T = m c^2 (gamma_th - 1), with gamma_th = 1/sqrt(1 - 1/n^2).
The emission angle is cos(theta) = 1/(n beta).

Usage: python cherenkov_threshold.py [n ...]
"""
import math
import sys

MASSES_MEV = {"electron": 0.51099895, "muon": 105.6583755, "pion": 139.57039, "proton": 938.27208816}
MATERIALS = {"fused silica": 1.47, "PbF2": 1.80, "water": 1.33}


def threshold_ke(mass_mev: float, n: float) -> float:
    """Kinetic energy (MeV) at the Cherenkov threshold for refractive index n."""
    gamma = 1.0 / math.sqrt(1.0 - 1.0 / n**2)
    return mass_mev * (gamma - 1.0)


def angle_deg(n: float, beta: float = 1.0) -> float:
    """Cherenkov emission angle in degrees (0 below threshold)."""
    c = 1.0 / (n * beta)
    return math.degrees(math.acos(c)) if c <= 1 else 0.0


def main() -> None:
    materials = {f"n = {x}": float(x) for x in sys.argv[1:]} or MATERIALS
    for name, n in materials.items():
        print(f"{name} (n = {n}): max angle {angle_deg(n):.1f} deg")
        for particle, m in MASSES_MEV.items():
            print(f"  {particle:8s} threshold {threshold_ke(m, n):10.3f} MeV")


if __name__ == "__main__":
    main()
