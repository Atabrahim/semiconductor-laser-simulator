"""Spin-degenerate 2D parabolic-subband populations (SI densities, eV energies)."""

from dataclasses import dataclass

import numpy as np
from scipy.constants import Boltzmann, electron_mass, elementary_charge, hbar
from scipy.optimize import brentq
from scipy.special import expit

from .materials import GaAsAlGaAs, positive
from .quantum import finite_well


def _levels(levels_eV):
    levels = np.asarray(levels_eV, dtype=float)
    if levels.ndim != 1 or not levels.size or not np.all(np.isfinite(levels)):
        raise ValueError("levels_eV must be a nonempty finite 1D sequence")
    return levels


def _density(density_m2):
    if isinstance(density_m2, (bool, np.bool_)) or not np.isscalar(density_m2):
        raise ValueError("sheet density must be a finite nonnegative scalar")
    density = float(density_m2)
    if not np.isfinite(density) or density < 0:
        raise ValueError("sheet density must be finite and nonnegative")
    return density


def occupation(energy_eV, quasi_fermi_eV: float, temperature_K: float):
    """Electron OR hole occupation; each energy increases from its own band edge.

    A hole quasi-Fermi energy is Ev - Fp, not Fp - Ev. Minus infinity is the
    zero-population limit. No extra spin factor belongs in this probability.
    """
    thermal_eV = Boltzmann * positive(temperature_K, "temperature_K") / elementary_charge
    energies = np.asarray(energy_eV, dtype=float)
    if not np.all(np.isfinite(energies)):
        raise ValueError("energy_eV must be finite")
    if np.isnan(quasi_fermi_eV) or quasi_fermi_eV == np.inf:
        raise ValueError("quasi_fermi_eV must be finite or minus infinity")
    return expit((quasi_fermi_eV - energies) / thermal_eV)


def sheet_density_m2(
    quasi_fermi_eV: float, levels_eV, mass_parallel: float, temperature_K: float
) -> float:
    """Sum occupied subbands; DOS m/(pi*hbar**2) includes spin degeneracy two.

    mass_parallel is m/m0. No valley degeneracy, continuum, or light-hole states
    are implicitly added. Each confined subband is extended parabolically.
    """
    levels = _levels(levels_eV)
    mass = positive(mass_parallel, "mass_parallel") * electron_mass
    thermal_J = Boltzmann * positive(temperature_K, "temperature_K")
    if np.isnan(quasi_fermi_eV) or quasi_fermi_eV == np.inf:
        raise ValueError("quasi_fermi_eV must be finite or minus infinity")
    reduced = (quasi_fermi_eV - levels) * elementary_charge / thermal_J
    return float(mass * thermal_J / (np.pi * hbar**2) * np.logaddexp(0, reduced).sum())


def quasi_fermi_eV(
    density_m2: float, levels_eV, mass_parallel: float, temperature_K: float
) -> float:
    """Invert sheet density monotonically without a starting-guess dependence."""
    levels = _levels(levels_eV)
    mass = positive(mass_parallel, "mass_parallel") * electron_mass
    thermal_J = Boltzmann * positive(temperature_K, "temperature_K")
    density = _density(density_m2)
    if density == 0:
        return -np.inf
    reduced_density = density * np.pi * hbar**2 / (mass * thermal_J * levels.size)
    # Stable inverse softplus: log(exp(y)-1), including large degeneracy.
    inverse = reduced_density + np.log(-np.expm1(-reduced_density))
    offset = thermal_J / elementary_charge * inverse
    lower, upper = float(levels.min() + offset), float(levels.max() + offset)
    if upper == lower:
        return lower
    thermal_eV = thermal_J / elementary_charge
    return float(
        brentq(
            lambda mu: sheet_density_m2(mu, levels, mass_parallel, temperature_K) / density - 1,
            lower - thermal_eV,
            upper + thermal_eV,
            xtol=1e-13,
        )
    )


@dataclass(frozen=True)
class NeutralPopulation:
    """Equal electron/hole sheet populations per well; no background doping."""

    sheet_density_m2: float
    active_density_m3: float
    electron_mu_eV: float
    hole_mu_eV: float
    quasi_fermi_separation_eV: float


def neutral_population(
    sheet_density: float, width_m: float, material: GaAsAlGaAs
) -> NeutralPopulation:
    """Compute Fn-Fp = Eg + mu_e + mu_h and N_active = n_sheet/Lw.

    N_active is an equivalent density per geometric well volume, NOT a bulk
    DOS calculation or the spatially resolved density including envelope tails.
    """
    density = _density(sheet_density)
    width = positive(width_m, "width_m")
    electrons = finite_well(
        width,
        material.electron_barrier_eV,
        material.electron_mass,
        material.electron_barrier_mass,
    )
    holes = finite_well(
        width, material.hole_barrier_eV, material.hole_mass_z, material.hole_barrier_mass_z
    )
    electron_mu = quasi_fermi_eV(
        density,
        [s.energy_eV for s in electrons],
        material.electron_mass,
        material.temperature_K,
    )
    hole_mu = quasi_fermi_eV(
        density,
        [s.energy_eV for s in holes],
        material.hole_mass_parallel,
        material.temperature_K,
    )
    return NeutralPopulation(
        density,
        density / width,
        electron_mu,
        hole_mu,
        material.bandgap_eV + electron_mu + hole_mu,
    )
