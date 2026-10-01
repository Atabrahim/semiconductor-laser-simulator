# Project 6 progress — Semiconductor Laser Simulator

## Original objective and frozen V1
Add active III–V optoelectronics to the completed five-project portfolio. Model a
GaAs/AlGaAs quantum-well edge-emitting laser using explicit approximations.

Mandatory: finite effective-mass quantum-well levels and optical transitions;
carrier quasi-Fermi populations and simplified interband gain; Fabry–Perot loss,
threshold and output coupling; consistent carrier/photon normalization; static
L–I and transient turn-on; prescribed-temperature and cavity sensitivity;
independent benchmarks, API/CLI, reproducible reports/figures, scientific docs,
tests, package, clean installation, actual CI and verified release.

Future work: multiband k.p, strain, excitons and many-body corrections, transport/
capture/escape, self-consistent heating, multimode competition, calibrated device
prediction, experimental fitting, optional interactive UI. These are not V1 gates.

## Portfolio audit
Read the five published README files and inspected repository inventory on
30 September 2026. Existing coverage: equilibrium silicon carrier statistics;
PN electrostatics and compact diode diagnostics; measured Raman fitting/bootstrap;
conservative dopant diffusion with thermal budgets; passive multilayer optics,
ellipsometric inference and tolerances. No laser repository/workspace existed.
New capability: driven electron–hole populations, confined active-region states,
stimulated emission and nonlinear carrier–photon dynamics. Reuse engineering
practices, not copies of earlier solvers.

## Architecture
src/laser_sim: materials, quantum well, gain/populations, cavity/rate equations,
workflow/CLI. tests: independent scientific checks. examples: fixed study inputs.
docs: equations, parameter provenance, validation and progress. results: labelled
numerical outputs. SI internally; conversion boundaries explicitly named.

## Milestones
- Audit and scope: VERIFIED
- Repository scaffold/recovery record: VERIFIED, PUBLISHED
- Material and quantum-well source, tests and documentation: VERIFIED, PUBLISHED
- Carrier populations source and tests: VERIFIED, PUBLISHED
- Optical gain: NOT STARTED
- Cavity, threshold and dynamics: NOT STARTED
- Reproducible studies/figures/documentation: NOT STARTED
- Adversarial audit, package, CI, release: NOT STARTED

## Scientific validation and test status
11 tests pass (1 October 2026, 0.37 s). Ruff passes. Six confinement tests plus
five population tests: independent radial k-space integration, Boltzmann/degenerate
limits, single/multiple-subband inversion, neutrality conventions and invalid inputs.
Required checks: finite-well roots vs independent finite differences, infinite-well
limit, carrier-population integrals, gain sign/transparency, cavity round trip,
steady-state balance vs integration, independent integrators/tolerance refinement,
photon-number/active-volume consistency and convergence of reported outputs.

## Known limitations / parameter policy
Material references must be verified before use. Device geometry/loss/lifetime/
confinement are scenario inputs, not universal GaAs constants. Temperature is a
prescribed junction temperature; no self-heating prediction. No experimental
validation claimed. AI-assisted development and execution of validation.

## Next action
Implement and independently validate optical gain; do not repeat confinement work.

## Latest verified GitHub checkpoint
af817705087010c78f17d793797fa1b1f544621b — population tests, following
2b9f16c (population source). Source/tests compared with fetched GitHub contents.
This field records the verified preceding checkpoint, not its own future commit.

## Resolved validation findings
The independent finite-difference benchmark initially used the wrong average at
a mass interface. Series resistance requires arithmetic mass (harmonic inverse
mass), not arithmetic inverse mass. Correcting the independent discretization
restored second-order convergence. Refining to 0.025 nm meets the original 2 µeV
error gate. The infinite-barrier test uses a deliberately nonphysical 1000 eV
barrier to approach the mathematical limit; not a material parameter.
