"""Restricted GaAs/AlGaAs band-edge model; energies eV and masses / m0."""

from dataclasses import dataclass

import numpy as np


def positive(value: float, name: str) -> float:
    """Require a finite positive scalar, rejecting booleans."""
    if isinstance(value, (bool, np.bool_)) or not np.isscalar(value):
        raise ValueError(f"{name} must be a finite positive scalar")
    value = float(value)
    if not np.isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be finite and positive")
    return value


@dataclass(frozen=True)
class GaAsAlGaAs:
    """Unstrained (001), parabolic Gamma electrons and uncoupled heavy holes.

    Offsets use 60/40 of 1.155*x + 0.37*x**2 eV. Fixed band masses and
    offsets over 250–350 K are approximations, not measured device inputs.
    """

    aluminum_fraction: float = 0.3
    temperature_K: float = 300.0

    def __post_init__(self):
        if not np.isfinite(self.aluminum_fraction) or not 0.1 <= self.aluminum_fraction <= 0.35:
            raise ValueError("aluminum_fraction must be in [0.1, 0.35]")
        if not np.isfinite(self.temperature_K) or not 250 <= self.temperature_K <= 350:
            raise ValueError("temperature_K must be in [250, 350]")

    @property
    def bandgap_eV(self):
        t = self.temperature_K
        return 1.519 - 5.405e-4 * t * t / (t + 204)

    @property
    def gap_offset_eV(self):
        x = self.aluminum_fraction
        return 1.155 * x + 0.37 * x * x

    @property
    def electron_barrier_eV(self):
        return 0.6 * self.gap_offset_eV

    @property
    def hole_barrier_eV(self):
        return 0.4 * self.gap_offset_eV

    @property
    def electron_mass(self):
        return 0.067

    @property
    def electron_barrier_mass(self):
        return 0.067 + 0.083 * self.aluminum_fraction

    @property
    def hole_mass_z(self):
        return 1 / (6.98 - 2 * 2.06)

    @property
    def hole_mass_parallel(self):
        return 1 / (6.98 + 2.06)

    @property
    def hole_barrier_mass_z(self):
        x = self.aluminum_fraction
        gamma1 = 6.98 * (1 - x) + 3.76 * x
        gamma2 = 2.06 * (1 - x) + 0.82 * x
        return 1 / (gamma1 - 2 * gamma2)
