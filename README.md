# Compact Cherenkov detectors for space radiation

PhD research at the Surrey Space Centre (University of Surrey, from October 2026) on compact detectors for high-energy charged particles in space, read out with silicon photomultipliers (SiPMs).

Cherenkov radiators only light up above a speed threshold (beta > 1/n), so choosing the radiator material sets an energy threshold for each particle type. Combined with simulation (Geant4 and ESA's GRAS), lab tests and a high-altitude prototype, the aim is a small, low-power instrument for measuring energetic protons and their direction.

## What's here
| Path | What it is |
|---|---|
| `tools/cherenkov_threshold.py` | Threshold kinetic energies and emission angles for electrons, muons, pions and protons in fused silica, PbF2 and water (or any refractive index). |
| `docs/gras7-geant4-11-install.md` | Step-by-step build of Geant4 11.3 + GRAS 7 from source on Linux without root access. |

```
$ python tools/cherenkov_threshold.py
fused silica (n = 1.47): max angle 47.1 deg
  proton   threshold    341.842 MeV
  ...
```

More code (simulation benchmarks, analysis) will be added as results are published.

## Related
- [MicroBooNE_DarkTrident_CNN](https://github.com/paul-fl/MicroBooNE_DarkTrident_CNN), [LYSOSimulation](https://github.com/paul-fl/LYSOSimulation)
- Website: [paul-fl.github.io](https://paul-fl.github.io)
