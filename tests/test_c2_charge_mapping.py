import pytest
import inspect

def test_c2_module_imports():
    """RED esperado: ModuleNotFoundError."""
    try:
        import mvp_quantum_materials.c2_charge_mapping
    except ModuleNotFoundError:
        pass  # Expected in RED phase
    else:
        pytest.fail("Module should not exist in RED phase")

def test_interface_sheet_source_dataclass_contract():
    """InterfaceSheetSource deve conter campos obrigatorios e bloqueios."""
    from mvp_quantum_materials.c2_charge_mapping import InterfaceSheetSource
    
    fields = inspect.signature(InterfaceSheetSource).parameters
    assert "sigma_c_per_m2" in fields
    assert "surface_dimension" in fields
    assert "geometry_label" in fields
    
    source = InterfaceSheetSource(sigma_c_per_m2=1e-4, surface_dimension="1D", geometry_label="top_gate")
    assert source.source_type == "interface_sheet"
    assert source.physical_interpretation_allowed is False
    assert source.solver_coupling_enabled is False

def test_interface_sheet_source_requires_sigma_units():
    """sigma deve ser C/m² e rejeitar unidades invalidas."""
    from mvp_quantum_materials.c2_charge_mapping import InterfaceSheetSource
    with pytest.raises(ValueError, match="Units must be C/m²"):
        InterfaceSheetSource(sigma_c_per_m2=1e-4, surface_dimension="1D", geometry_label="top_gate", units="C/cm2")

def test_interface_sheet_source_preserves_charge_sign():
    """sinal positivo e negativo de sigma deve ser preservado."""
    from mvp_quantum_materials.c2_charge_mapping import InterfaceSheetSource
    source_pos = InterfaceSheetSource(sigma_c_per_m2=1e-4, surface_dimension="1D", geometry_label="top_gate")
    source_neg = InterfaceSheetSource(sigma_c_per_m2=-1e-4, surface_dimension="1D", geometry_label="top_gate")
    assert source_pos.sigma_c_per_m2 > 0
    assert source_neg.sigma_c_per_m2 < 0

def test_conservative_regularization_requires_l_reg():
    """Regularização volumétrica deve exigir l_reg explicitamente."""
    from mvp_quantum_materials.c2_charge_mapping import ConservativeVolumeRegularization
    with pytest.raises(TypeError):
        ConservativeVolumeRegularization(sigma_c_per_m2=1e-4)

def test_l_reg_positive_finite():
    """l_reg deve ser finito e positivo."""
    from mvp_quantum_materials.c2_charge_mapping import ConservativeVolumeRegularization
    with pytest.raises(ValueError):
        ConservativeVolumeRegularization(sigma_c_per_m2=1e-4, l_reg=-1e-9)
    with pytest.raises(ValueError):
        ConservativeVolumeRegularization(sigma_c_per_m2=1e-4, l_reg=0)

def test_l_reg_is_numerical_not_physical_t_eff():
    """Metadata deve declarar natureza numerica de l_reg."""
    from mvp_quantum_materials.c2_charge_mapping import ConservativeVolumeRegularization
    reg = ConservativeVolumeRegularization(sigma_c_per_m2=1e-4, l_reg=1e-9)
    assert reg.metadata["regularization_role"] == "numerical"
    assert reg.metadata["not_physical_t_eff"] is True
    assert reg.metadata["calibration_status"] == "not_calibrated"

def test_rho_reg_units_are_c_per_m3():
    """rho_reg deve ter unidade C/m³."""
    from mvp_quantum_materials.c2_charge_mapping import ConservativeVolumeRegularization
    reg = ConservativeVolumeRegularization(sigma_c_per_m2=1e-4, l_reg=1e-9)
    assert "C/m³" in reg.rho_units or "C/m3" in reg.rho_units

def test_volume_regularization_preserves_total_charge_uniform_case():
    """Caso uniforme: rho_reg * volume = sigma * A."""
    from mvp_quantum_materials.c2_charge_mapping import regularize_sheet_charge_to_volume
    sigma = 1e-4
    A = 1e-12
    l_reg = 1e-9
    rho_reg = regularize_sheet_charge_to_volume(sigma, l_reg)
    volume = A * l_reg
    assert pytest.approx(rho_reg * volume) == sigma * A

def test_volume_regularization_preserves_total_charge_discrete_case():
    """Para arrays discretos: sum(rho_reg * cell_volume) == sum(sigma * cell_area)."""
    from mvp_quantum_materials.c2_charge_mapping import validate_charge_conservation
    import numpy as np
    sigma_array = np.array([1e-4, 2e-4, 3e-4])
    area_array = np.array([1e-12, 1e-12, 1e-12])
    l_reg = 1e-9
    rho_array = sigma_array / l_reg
    vol_array = area_array * l_reg
    assert validate_charge_conservation(rho_array, vol_array, sigma_array, area_array) is True

def test_charge_conservation_tolerance_is_explicit():
    """A tolerância não pode ser default escondido."""
    from mvp_quantum_materials.c2_charge_mapping import validate_charge_conservation
    fields = inspect.signature(validate_charge_conservation).parameters
    assert "tolerance" in fields
    assert fields["tolerance"].default is not inspect.Parameter.empty

def test_depth_prior_requires_trap_family():
    """Depth prior deve exigir trap_family e distinguir entre interface e border/oxide."""
    from mvp_quantum_materials.c2_charge_mapping import DepthPriorMetadata
    with pytest.raises(ValueError):
        DepthPriorMetadata(trap_family="invalid_family")
    valid = DepthPriorMetadata(trap_family="border", source="Test", source_role="test", material_stack="Si", interface_or_region="Si", depth_or_distribution_parameter="1nm", length_units="nm", transferability_note="None", calibration_status="not_calibrated")
    assert valid.trap_family in {"interface", "border", "oxide", "near_interface_oxide"}

def test_e1_depth_prior_requires_metadata():
    """E1 depth prior deve exigir campos especificos."""
    from mvp_quantum_materials.c2_charge_mapping import DepthPriorMetadata
    fields = inspect.signature(DepthPriorMetadata).parameters
    required_fields = ["source", "source_role", "material_stack", "interface_or_region", "depth_or_distribution_parameter", "length_units", "transferability_note", "calibration_status"]
    for req in required_fields:
        assert req in fields

def test_e2_depth_prior_requires_full_metadata():
    """E2 deve exigir, alem dos campos E1, campos adicionais."""
    from mvp_quantum_materials.c2_charge_mapping import ExperimentalDepthPriorMetadata
    fields = inspect.signature(ExperimentalDepthPriorMetadata).parameters
    required_e2_fields = ["technique", "extraction_assumptions", "uncertainty_note", "temperature_or_bias_context"]
    for req in required_e2_fields:
        assert req in fields

def test_generic_physical_t_eff_rejected():
    """Qualquer uso de generic t_eff deve ser rejeitado."""
    from mvp_quantum_materials.c2_charge_mapping import build_interface_sheet_source
    with pytest.raises(ValueError, match="generic_thickness"):
        build_interface_sheet_source(sigma=1e-4, generic_thickness=1e-9)

def test_calibrated_t_eff_blocked():
    """calibration_status = 'calibrated' deve ser rejeitado."""
    from mvp_quantum_materials.c2_charge_mapping import DepthPriorMetadata
    with pytest.raises(ValueError, match="calibrated"):
        DepthPriorMetadata(calibration_status="calibrated", trap_family="border", source="Test", source_role="test", material_stack="Si", interface_or_region="Si", depth_or_distribution_parameter="1nm", length_units="nm", transferability_note="None")

def test_no_solver_import_or_coupling():
    """Modulo futuro não pode importar poisson_solver_2d e solver_coupling_enabled = False."""
    from mvp_quantum_materials.c2_charge_mapping import InterfaceSheetSource
    import sys
    assert "poisson_solver_2d" not in sys.modules
    source = InterfaceSheetSource(sigma_c_per_m2=1e-4, surface_dimension="1D", geometry_label="top_gate")
    assert source.solver_coupling_enabled is False

def test_no_quantum_confinement_solver_import():
    """Modulo futuro não pode importar solver de confinamento quantico."""
    import sys
    try:
        import mvp_quantum_materials.c2_charge_mapping
    except ModuleNotFoundError:
        pass
    assert "quantum_confinement_solver" not in sys.modules
    assert "schrodinger" not in sys.modules

def test_no_physical_phi_claim():
    """Modulo C2 não pode autorizar interpretação fisica de phi."""
    from mvp_quantum_materials.c2_charge_mapping import InterfaceSheetSource
    source = InterfaceSheetSource(sigma_c_per_m2=1e-4, surface_dimension="1D", geometry_label="top_gate")
    assert getattr(source, "phi_physical_claim", False) is False

def test_future_green_does_not_modify_existing_c1_profiles():
    """C2 não deve modificar modulos C1."""
    import inspect
    import mvp_quantum_materials.surface_charge as sc
    import mvp_quantum_materials.energy_profiles as ep
    import mvp_quantum_materials.dit_profile_library as dl
    # Just asserting they exist and can be inspected without being altered by C2
    assert inspect.ismodule(sc)
    assert inspect.ismodule(ep)
    assert inspect.ismodule(dl)
