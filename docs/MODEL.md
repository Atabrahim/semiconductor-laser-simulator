# Physical model and conventions

## Material and confinement

An unstrained (001) GaAs well is surrounded by Al_xGa_(1-x)As, 0.1 <= x <= 0.35.
The empirical direct-gap increment is 1.155 x + 0.37 x² eV; 60% is assigned to
conduction and 40% to valence confinement. Offsets are held constant over the
restricted prescribed-temperature range 250–350 K. This is an approximate
band-offset model, not a fit to a particular grown heterostructure.

GaAs gap: Eg(T) = 1.519 - 5.405e-4 T²/(T+204) eV, T in kelvin.
Electron mass: 0.067 m0 in the well, (0.067 + 0.083 x)m0 in the barrier.
For uncoupled heavy holes, m_z/m0 = 1/(gamma1-2 gamma2) and
m_parallel/m0 = 1/(gamma1+gamma2). GaAs gamma1=6.98, gamma2=2.06;
AlAs gamma1=3.76, gamma2=0.82, linearly interpolated in the barrier.
Valence mixing, strain, nonparabolicity and temperature-dependent masses are absent.

Solve H psi = E psi with H = -(hbar²/2) d/dz [(1/m(z)) d/dz] + V(z).
The well bottom is zero, V outside is the respective positive band offset, and
psi decays at infinity. Both psi and (1/m)dpsi/dz are continuous at an interface.
Set a=Lw/2, k=sqrt(2 mw E)/hbar, kappa=sqrt(2 mb (V-E))/hbar.
Even states obey k tan(ka)/mw = kappa/mb; odd states obey
-k cot(ka)/mw = kappa/mb. Brent roots are bracketed between successive poles.
The code solves in dimensionless ka and includes analytic tail normalization.
Energies are returned in eV; widths/positions in m; masses supplied as m/m0;
normalized envelopes have units m^(-1/2). Overlap squared is dimensionless.

The independent test constructs the differential operator on a cell grid, with
series interface resistance and remote zero envelope boundaries. Its convergence
checks the transcendental solution rather than reusing the same root formula.

## Sources and parameter status

- I. Vurgaftman, J. R. Meyer and L. R. Ram-Mohan, J. Appl. Phys. 89, 5815 (2001),
  https://doi.org/10.1063/1.1368156 — standard band parameter compilation.
- *Optical gain spectra of unstrained
  graded GaAs/AlxGa1-xAs quantum well laser*, Physics Letters A 377 (2013) 582–586,
  https://www.sciencedirect.com/science/article/pii/S0375960112013084 — empirical
  alloy electron mass and gap increment; the model here does not reproduce its
  graded well or full hole treatment.
- *The Combined Influence of Hydrostatic Pressure and Temperature on Nonlinear
  Optical Properties of GaAs/Ga0.7Al0.3As Morse Quantum Well in the Presence of an
  Applied Magnetic Field*, https://pmc.ncbi.nlm.nih.gov/articles/PMC5978045/ —
  example 60% conduction offset convention. Offset ratios vary between models.
- F. Rana, Cornell ECE533, Chapter 11, *Basics of Semiconductor Lasers*,
  https://courses.cit.cornell.edu/ece533/Lectures/handout11.pdf — cavity and
  rate-equation normalization reference for the next milestone.

All outputs are ANALYTICAL MODEL or NUMERICAL MODEL results. Literature material
parameters are REFERENCE DATA. No EXPERIMENTAL DATA or calibrated device claims.
Further gain and dynamics equations will be documented as implemented and tested.
