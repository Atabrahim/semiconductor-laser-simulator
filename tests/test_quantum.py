import numpy as np
import pytest
from scipy.constants import elementary_charge as q
from scipy.constants import hbar, m_e
from scipy.integrate import quad
from scipy.linalg import eigh_tridiagonal

from laser_sim.materials import GaAsAlGaAs
from laser_sim.quantum import finite_well, overlap_squared


def test_gaas_reference_and_temperature():
    assert GaAsAlGaAs().bandgap_eV == pytest.approx(1.422482142857, abs=1e-12)
    assert GaAsAlGaAs(temperature_K=350).bandgap_eV < GaAsAlGaAs(temperature_K=250).bandgap_eV


def test_infinite_well_limit():
    width = 8e-9
    states = finite_well(width, 1000, 0.067, 0.067)
    exact = hbar**2 * np.pi**2 / (2 * 0.067 * m_e * width**2 * q)
    assert states[0].energy_eV < exact
    assert states[0].energy_eV / exact > 0.97


def test_wavefunctions_and_bdd_interfaces():
    states = finite_well(8e-9, 0.23, 0.067, 0.092)
    for s in states:
        a = s.half_width_m
        integral = quad(lambda y, s=s, a=a: float(s.envelope_mhalf(a * y)) ** 2 * a, -1, 1)[0]
        integral += 2 * float(s.envelope_mhalf(a)) ** 2 / (2 * s.decay_m1)
        assert integral == pytest.approx(1, abs=1e-11)
        z = s.wavevector_m1 * a
        lhs = s.wavevector_m1 * (np.tan(z) if s.parity == 1 else -1 / np.tan(z)) / 0.067
        assert lhs == pytest.approx(s.decay_m1 / 0.092, rel=1e-10)
        assert overlap_squared(s, s) == pytest.approx(1, abs=1e-11)
    assert overlap_squared(states[0], states[1]) == 0


def fd_ground(width, barrier, mw, mb, dx):
    # Independent conservative BDD operator: cell mass, series interface resistance (arithmetic mass mean).
    x = np.arange(-40e-9 + dx / 2, 40e-9, dx)
    inside = np.abs(x) < width / 2
    inv = 1 / np.where(inside, mw, mb)
    face = 2 / (1 / inv[:-1] + 1 / inv[1:])
    scale = hbar**2 / (2 * m_e * q * dx * dx)
    diag = scale * np.r_[inv[0] + face[0], face[:-1] + face[1:], face[-1] + inv[-1]]
    diag += np.where(inside, 0, barrier)
    return eigh_tridiagonal(diag, -scale * face, select="i", select_range=(0, 0))[0][0]


def test_independent_finite_difference_convergence():
    exact = finite_well(8e-9, 0.23, 0.067, 0.092)[0].energy_eV
    errors = [
        abs(fd_ground(8e-9, 0.23, 0.067, 0.092, dx) - exact)
        for dx in [0.1e-9, 0.05e-9, 0.025e-9]
    ]
    assert errors[1] < errors[0] / 3
    assert errors[2] < errors[1] / 3
    assert errors[2] < 2e-6


def test_width_and_barrier_trends():
    assert (
        finite_well(10e-9, 0.23, 0.067, 0.092)[0].energy_eV
        < finite_well(8e-9, 0.23, 0.067, 0.092)[0].energy_eV
    )
    assert (
        finite_well(8e-9, 0.4, 0.067, 0.092)[0].energy_eV
        > finite_well(8e-9, 0.23, 0.067, 0.092)[0].energy_eV
    )


def test_input_rejection():
    for bad in [0, -1, np.nan, np.inf, True]:
        with pytest.raises(ValueError):
            finite_well(bad, 0.23, 0.067, 0.092)
    with pytest.raises(ValueError):
        GaAsAlGaAs(aluminum_fraction=0.8)
    with pytest.raises(ValueError):
        GaAsAlGaAs(temperature_K=0)
