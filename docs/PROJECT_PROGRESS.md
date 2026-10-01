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
- Material and quantum-well source: VERIFIED, PUBLISHED; supporting tests/docs publication in progress
- Populations and gain: NOT STARTED
- Cavity, threshold and dynamics: NOT STARTED
- Reproducible studies/figures/documentation: NOT STARTED
- Adversarial audit, package, CI, release: NOT STARTED

## Scientific validation and test status
Six scientific tests pass: GaAs reference gap, mass-interface matching, normalization, infinite-barrier limit, width/barrier trends and an independent conservative finite-difference refinement.
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
Publish material/finite-well milestone; next implement quasi-Fermi populations and gain.

## Latest verified GitHub checkpoint
0d322a924d6294f4f6ba2daebf489bfb687eb712 — material and quantum-well source;
remote source compared byte-for-byte with local files on 1 October 2026.
Publication gate rerun: 6 passed in 0.37 s; no solver changes.

## Resolved validation findings
The independent finite-difference benchmark initially used the wrong average at
a mass interface. Series resistance requires arithmetic mass (harmonic inverse
mass), not arithmetic inverse mass. Correcting the independent discretization
restored second-order convergence. Refining to 0.025 nm meets the original 2 µeV
error gate. The infinite-barrier test uses a deliberately nonphysical 1000 eV
barrier to approach the mathematical limit; not a material parameter.
