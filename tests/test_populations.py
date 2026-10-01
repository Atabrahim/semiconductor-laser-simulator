"""Independent k-space integration and exact limits for 2D carrier statistics."""

import numpy as np
import pytest
from scipy.constants import Boltzmann, electron_mass, elementary_charge, hbar
from scipy.integrate import quad
from scipy.special import expit

from laser_sim.materials import GaAsAlGaAs
from laser_sim.populations import (
    neutral_population,
    occupation,
    quasi_fermi_eV,
    sheet_density_m2,
)


def test_against_direct_radial_k_space_counting():
    # Count two spin states in d²k/(2pi)², without using the integrated DOS formula.
    levels, mass, temperature = [0.04, 0.11, 0.19], 0.067, 300
    scale_k = np.sqrt(2 * mass * electron_mass * Boltzmann * temperature) / hbar
    for mu in [-0.2, 0.08, 0.35]:
        count = 0.0
        for edge in levels:
            eta = (mu - edge) * elementary_charge / (Boltzmann * temperature)
            count += quad(lambda radius, eta=eta: radius * expit(eta - radius**2), 0, np.inf)[0]
        independent = scale_k**2 / np.pi * count
        assert sheet_density_m2(mu, levels, mass, temperature) == pytest.approx(
            independent, rel=2e-10
        )


def test_single_subband_exact_inverse_and_degenerate_limit():
    mass, temperature, edge = 0.09, 300, 0.02
    dos_J = mass * electron_mass / (np.pi * hbar**2)
    for density in [1e7, 1e14, 1e16, 1e18]:
        mu = quasi_fermi_eV(density, [edge], mass, temperature)
        assert sheet_density_m2(mu, [edge], mass, temperature) == pytest.approx(
            density, rel=2e-13
        )
    # Zero-temperature filled disk, well above kBT; no numerical inverse involved.
    density = sheet_density_m2(0.4, [edge], mass, 1)
    assert density == pytest.approx(dos_J * (0.4 - edge) * elementary_charge, rel=1e-13)


def test_boltzmann_limit_and_temperature_effect():
    thermal_eV = Boltzmann * 300 / elementary_charge
    mu, edge = -0.5, 0.03
    expected = 0.067 * electron_mass * Boltzmann * 300 / (np.pi * hbar**2)
    expected *= np.exp((mu - edge) / thermal_eV)
    assert sheet_density_m2(mu, [edge], 0.067, 300) == pytest.approx(expected, rel=1e-9)
    assert sheet_density_m2(mu, [edge], 0.067, 350) > expected


def test_multiple_subbands_neutrality_and_energy_references():
    levels = [0.03, 0.09, 0.14]
    for density in [1e9, 1e15, 2e16, 1e18]:
        mu = quasi_fermi_eV(density, levels, 0.1, 300)
        assert sheet_density_m2(mu, levels, 0.1, 300) == pytest.approx(density, rel=1e-10)
    material = GaAsAlGaAs()
    result = neutral_population(1e16, 8e-9, material)
    assert result.active_density_m3 == pytest.approx(1.25e24)
    assert result.quasi_fermi_separation_eV == pytest.approx(
        material.bandgap_eV + result.electron_mu_eV + result.hole_mu_eV
    )
    assert occupation(result.hole_mu_eV, result.hole_mu_eV, 300) == 0.5


def test_zero_and_invalid_inputs():
    assert quasi_fermi_eV(0, [0.03], 0.067, 300) == -np.inf
    assert sheet_density_m2(-np.inf, [0.03], 0.067, 300) == 0
    assert occupation([0.03, 0.1], -np.inf, 300).tolist() == [0, 0]
    for density in [-1, np.nan, np.inf, True]:
        with pytest.raises(ValueError):
            quasi_fermi_eV(density, [0.03], 0.067, 300)
    for levels in [[], [[0.03]], [np.nan]]:
        with pytest.raises(ValueError):
            sheet_density_m2(0, levels, 0.067, 300)
