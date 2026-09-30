"""Symmetric finite square well with BenDaniel–Duke mass interfaces."""

from dataclasses import dataclass

import numpy as np
from scipy.constants import elementary_charge as q
from scipy.constants import hbar, m_e
from scipy.integrate import quad
from scipy.optimize import brentq

from .materials import positive


@dataclass(frozen=True)
class BoundState:
    """Normalized real envelope: energy above well bottom; parity +1/-1."""

    energy_eV: float
    parity: int
    half_width_m: float
    wavevector_m1: float
    decay_m1: float

    def envelope_mhalf(self, position_m):
        """Return envelope in m**(-1/2); squared integral over all z is one."""
        x = np.asarray(position_m, dtype=float)
        a, k, kap = self.half_width_m, self.wavevector_m1, self.decay_m1
        phase = k * a
        if self.parity == 1:
            norm = a + np.sin(2 * phase) / (2 * k) + np.cos(phase) ** 2 / kap
            inside = np.cos(k * x)
            edge = np.cos(phase)
            sign = 1
        else:
            norm = a - np.sin(2 * phase) / (2 * k) + np.sin(phase) ** 2 / kap
            inside = np.sin(k * x)
            edge = np.sin(phase)
            sign = np.sign(x)
        outside = sign * edge * np.exp(-kap * np.maximum(np.abs(x) - a, 0))
        return np.where(np.abs(x) <= a, inside, outside) / np.sqrt(norm)


def finite_well(
    width_m: float, barrier_eV: float, mass_well: float, mass_barrier: float
) -> tuple[BoundState, ...]:
    """All bound levels, matched psi and (1/m)dpsi/dz, decaying at infinity.

    Bracket one root in each dimensionless half-period; never bracket a tan pole.
    Mass arguments are relative to the free electron mass.
    """
    width = positive(width_m, "width_m")
    barrier = positive(barrier_eV, "barrier_eV")
    mw = positive(mass_well, "mass_well")
    mb = positive(mass_barrier, "mass_barrier")
    a = width / 2
    z0 = a * np.sqrt(2 * mw * m_e * barrier * q) / hbar
    if z0 < 1e-5 or z0 > 500:
        raise ValueError("well strength outside supported numerical range")
    levels = []
    for j in range(int(np.ceil(2 * z0 / np.pi))):
        lo, hi = j * np.pi / 2, min((j + 1) * np.pi / 2, z0)
        if hi - lo < 1e-12:
            continue
        parity = 1 if j % 2 == 0 else -1

        def mismatch(z, parity=parity):
            left = z * np.tan(z) if parity == 1 else -z / np.tan(z)
            return left - np.sqrt(mw / mb) * np.sqrt(max(0, z0 * z0 - z * z))

        lo += 1e-13
        hi -= 1e-13
        if mismatch(lo) * mismatch(hi) >= 0:
            continue
        root = brentq(mismatch, lo, hi, xtol=1e-14)
        energy = hbar * hbar * (root / a) ** 2 / (2 * mw * m_e * q)
        kap = np.sqrt(2 * mb * m_e * q * (barrier - energy)) / hbar
        levels.append(BoundState(energy, parity, a, root / a, kap))
    if not levels:
        raise ArithmeticError("no resolved bound state")
    return tuple(levels)


def overlap_squared(first: BoundState, second: BoundState) -> float:
    """Dimensionless envelope overlap, including analytic infinite tails."""
    if first.half_width_m != second.half_width_m:
        raise ValueError("states must share the same well width")
    if first.parity != second.parity:
        return 0.0
    a = first.half_width_m
    inner = (
        2
        * quad(
            lambda y: float(first.envelope_mhalf(a * y) * second.envelope_mhalf(a * y)) * a,
            0,
            1,
            epsabs=1e-12,
        )[0]
    )
    tail = (
        2
        * float(first.envelope_mhalf(a) * second.envelope_mhalf(a))
        / (first.decay_m1 + second.decay_m1)
    )
    return (inner + tail) ** 2
