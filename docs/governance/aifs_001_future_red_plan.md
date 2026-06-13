# AIFS-001 Future RED Plan

## Trigger

Only if ADR-015 is accepted in a future release.

## Future First Module

Not authorized now.

Possible future isolated namespace:

experiments/ai_for_science/aifs_001_poisson_1d/

No directory is created in this release.

## Candidate RED Tests

1. test_aifs_module_absent_until_adr_acceptance
2. test_no_ml_dependencies_in_pyproject
3. test_no_ml_imports_in_src_scripts_tests
4. test_benchmark_domain_is_explicit
5. test_operator_sign_convention_is_explicit
6. test_exact_solution_defined
7. test_source_term_matches_exact_solution
8. test_boundary_conditions_defined
9. test_l2_error_metric_required
10. test_linf_error_metric_required
11. test_residual_metric_required
12. test_boundary_error_metric_required
13. test_reproducibility_seed_required_if_stochastic
14. test_no_c1_imports
15. test_no_c2_imports
16. test_no_c3_imports
17. test_no_project_poisson_solver_import
18. test_no_physical_phi_claim
19. test_no_calibration_claim
20. test_no_device_prediction_claim

## Non-goals

* no implementation now;
* no PINN now;
* no surrogate now;
* no dependency now;
* no project physics coupling.
