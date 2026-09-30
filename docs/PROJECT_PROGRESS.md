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
- Repository scaffold/recovery record: IN PROGRESS
- Material and quantum-well model: NOT STARTED
- Populations and gain: NOT STARTED
- Cavity, threshold and dynamics: NOT STARTED
- Reproducible studies/figures/documentation: NOT STARTED
- Adversarial audit, package, CI, release: NOT STARTED

## Scientific validation and test status
No scientific implementation yet; no passing-test claim.
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
Publish this scaffold, then verify parameter sources and implement the finite well.

## Latest verified GitHub checkpoint
4855613e61c333811fd42bde4cc2bbee58ed3002 — repository created and verified.
