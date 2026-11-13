"""
ISOMORPH Corpus: Benchmark Scientific Literature Dataset
Curated cross-disciplinary datasets modeling real empirical mysteries across
Neuroscience, Fluid Dynamics, Quantum Physics, Economics, Epidemiology, and Synthetic Biology.
"""

from __future__ import annotations
from typing import List
from ..core.models import (
    ResearchArtifact,
    AbstractVariable,
    DynamicRole,
    InteractionKind,
    SystemRegime,
)


def load_benchmark_corpus() -> List[ResearchArtifact]:
    """
    Returns 6 deeply modeled empirical scientific papers representing diverse domains.
    """
    corpus: List[ResearchArtifact] = []

    # 1. NEUROIMMUNOLOGY
    p1 = ResearchArtifact(
        paper_id="NEURO-2024-88",
        title="Microglial Clearance Exhaustion in Hyper-phosphorylated Tau Microenvironments",
        authors="V. K. Vance, E. Thorne, et al.",
        year=2024,
        domain="Neuroimmunology",
        empirical_phenomenon="Sudden collapse of lymphatic interstitial debris clearance",
        unresolved_bottleneck="Non-linear transition from high clearance to permanent microglial arrest",
        regime=SystemRegime.FAR_FROM_EQUILIBRIUM,
        assumed_boundary_conditions=["viscous interstitial flow", "finite ATP pool"],
    )
    p1.add_mechanism(
        AbstractVariable("Interstitial_Debris_Flux", DynamicRole.SOURCE, conserved=False),
        AbstractVariable("Microglial_Degradation_Capacity", DynamicRole.BOTTLENECK, conserved=False),
        InteractionKind.POSITIVE_FEEDBACK,
        "dD/dt = flux - V_max * D / (K_m + D)",
        tau=0.8,
    )
    p1.add_mechanism(
        AbstractVariable("Microglial_Degradation_Capacity", DynamicRole.BOTTLENECK, conserved=False),
        AbstractVariable("Cellular_ATP_Reserve", DynamicRole.REGULATOR, conserved=True),
        InteractionKind.NEGATIVE_FEEDBACK,
        "dATP/dt = - alpha * degradation_rate",
        tau=1.2,
    )
    p1.add_mechanism(
        AbstractVariable("Cellular_ATP_Reserve", DynamicRole.REGULATOR, conserved=True),
        AbstractVariable("Microglial_Degradation_Capacity", DynamicRole.BOTTLENECK, conserved=False),
        InteractionKind.THRESHOLD_SWITCH,
        "if ATP < ATP_critical -> arrest = True",
        tau=0.2,
    )
    corpus.append(p1)

    # 2. HYDRAULIC NON-LINEAR MECHANICS
    p2 = ResearchArtifact(
        paper_id="HYDRO-1998-12",
        title="Bifurcation Dynamics of Bedload Sediment Jamming in Narrow Canal Flumes",
        authors="H. R. Bagnold, M. S. Garcia, et al.",
        year=1998,
        domain="Non-linear Hydrodynamics",
        empirical_phenomenon="Sudden canal lock jamming under steady particulate discharge",
        unresolved_bottleneck="Bagnold shear dilation bifurcation threshold",
        regime=SystemRegime.FAR_FROM_EQUILIBRIUM,
        assumed_boundary_conditions=["viscous fluid boundary", "confined granular bed"],
    )
    p2.add_mechanism(
        AbstractVariable("Sediment_Inflow_Volume", DynamicRole.SOURCE, conserved=False),
        AbstractVariable("Weir_Discharge_Throat", DynamicRole.BOTTLENECK, conserved=False),
        InteractionKind.POSITIVE_FEEDBACK,
        "dQ/dt = inflow - C_discharge * A * sqrt(2gh)",
        tau=0.75,
    )
    p2.add_mechanism(
        AbstractVariable("Weir_Discharge_Throat", DynamicRole.BOTTLENECK, conserved=False),
        AbstractVariable("Dynamic_Pore_Pressure", DynamicRole.REGULATOR, conserved=True),
        InteractionKind.NEGATIVE_FEEDBACK,
        "dP/dt = - beta * shear_strain_rate",
        tau=1.1,
    )
    p2.add_mechanism(
        AbstractVariable("Dynamic_Pore_Pressure", DynamicRole.REGULATOR, conserved=True),
        AbstractVariable("Weir_Discharge_Throat", DynamicRole.BOTTLENECK, conserved=False),
        InteractionKind.THRESHOLD_SWITCH,
        "if Pressure < P_shear_failure -> choke = True",
        tau=0.18,
    )
    corpus.append(p2)

    # 3. MACROECONOMICS / FINANCIAL NETWORKS
    p3 = ResearchArtifact(
        paper_id="FIN-2016-04",
        title="Endogenous Liquidity Freeze and Phase Transitions in Interbank Lending Networks",
        authors="A. Haldane, R. Cont, et al.",
        year=2016,
        domain="Macroeconomic Network Theory",
        empirical_phenomenon="Sudden interbank overnight credit evaporation during solvency rumors",
        unresolved_bottleneck="Spontaneous gridlock in uncollateralized credit velocity",
        regime=SystemRegime.FAR_FROM_EQUILIBRIUM,
        assumed_boundary_conditions=["clustered graph topology", "finite balance sheet capital"],
    )
    p3.add_mechanism(
        AbstractVariable("Interbank_Payment_Obligations", DynamicRole.SOURCE, conserved=False),
        AbstractVariable("Settlement_Velocity_Window", DynamicRole.BOTTLENECK, conserved=False),
        InteractionKind.POSITIVE_FEEDBACK,
        "dObligations/dt = credit_drawdown - settlement_rate",
        tau=0.5,
    )
    p3.add_mechanism(
        AbstractVariable("Settlement_Velocity_Window", DynamicRole.BOTTLENECK, conserved=False),
        AbstractVariable("Tier1_Capital_Buffer", DynamicRole.REGULATOR, conserved=True),
        InteractionKind.NEGATIVE_FEEDBACK,
        "dCapital/dt = - haircuts * exposure",
        tau=1.5,
    )
    p3.add_mechanism(
        AbstractVariable("Tier1_Capital_Buffer", DynamicRole.REGULATOR, conserved=True),
        AbstractVariable("Settlement_Velocity_Window", DynamicRole.BOTTLENECK, conserved=False),
        InteractionKind.THRESHOLD_SWITCH,
        "if Buffer < Tier1_min -> liquidity_freeze = True",
        tau=0.1,
    )
    corpus.append(p3)

    # 4. QUANTUM CAVITY OPTICS
    p4 = ResearchArtifact(
        paper_id="QPHYS-2022-77",
        title="Dicke Superradiance and Phase-Locking in Driven Dissipative Optical Cavities",
        authors="K. Baumann, C. Guerlin, et al.",
        year=2022,
        domain="Quantum Condensed Matter",
        empirical_phenomenon="Collective spontaneous emission into single cavity mode",
        unresolved_bottleneck="Photon decoherence barrier at critical coupling g_crit",
        regime=SystemRegime.CHAOTIC_TRANSITION,
        assumed_boundary_conditions=["frictionless cavity mirrors", "non-linear Kerr coupling"],
    )
    p4.add_mechanism(
        AbstractVariable("Coherent_Laser_Pump", DynamicRole.SOURCE, conserved=False),
        AbstractVariable("Intracavity_Photon_Mode", DynamicRole.BOTTLENECK, conserved=False),
        InteractionKind.POSITIVE_FEEDBACK,
        "da/dt = -i[H, a] + kappa * pump",
        tau=0.01,
    )
    p4.add_mechanism(
        AbstractVariable("Intracavity_Photon_Mode", DynamicRole.BOTTLENECK, conserved=False),
        AbstractVariable("Atomic_Inversion_Population", DynamicRole.REGULATOR, conserved=True),
        InteractionKind.NEGATIVE_FEEDBACK,
        "dSz/dt = - 2 * g * (a_dag * sm + a * sp)",
        tau=0.05,
    )
    p4.add_mechanism(
        AbstractVariable("Atomic_Inversion_Population", DynamicRole.REGULATOR, conserved=True),
        AbstractVariable("Intracavity_Photon_Mode", DynamicRole.BOTTLENECK, conserved=False),
        InteractionKind.THRESHOLD_SWITCH,
        "if g > g_crit -> superradiant_phase = True",
        tau=0.005,
    )
    corpus.append(p4)

    # 5. CLASSICAL EQUILIBRIUM THERMODYNAMICS PAPER (To trigger Axiomatic Collision!)
    p5 = ResearchArtifact(
        paper_id="THERMO-1985-01",
        title="Detailed Balance and Micro-Reversibility in Closed Biochemical Reaction Meshes",
        authors="G. Nicolis, I. Prigogine (Review Paper)",
        year=1985,
        domain="Classical Equilibrium Thermodynamics",
        empirical_phenomenon="Quasi-static steady-state maintenance in isolated cell extracts",
        unresolved_bottleneck="None: assumes strict equilibrium detailed balance",
        regime=SystemRegime.EQUILIBRIUM,
        assumed_boundary_conditions=["thermodynamic equilibrium", "infinite flux reservoir"],
    )
    p5.add_mechanism(
        AbstractVariable("Substrate_Pool", DynamicRole.SOURCE, conserved=False),
        AbstractVariable("Equilibrium_Product", DynamicRole.SINK, conserved=False),
        InteractionKind.DIFFUSION,
        "J_forward = J_reverse (Detailed Balance)",
        tau=10.0,
    )
    corpus.append(p5)

    # 6. SYNTHETIC METABOLIC ENGINEERING
    p6 = ResearchArtifact(
        paper_id="SYNBIOL-2023-33",
        title="Kinetic Bottlenecks in Synthetic Artemisinin Production via Yeast Mevalonate Pathway",
        authors="J. Keasling, Y. Zhang, et al.",
        year=2023,
        domain="Synthetic Biology",
        empirical_phenomenon="Unpredicted accumulation of toxic metabolic intermediate HMG-CoA",
        unresolved_bottleneck="Enzymatic rate mismatch and NADPH cofactor depletion",
        regime=SystemRegime.FAR_FROM_EQUILIBRIUM,
        assumed_boundary_conditions=["viscous cytoplasm", "finite NADPH pool"],
    )
    p6.add_mechanism(
        AbstractVariable("Acetyl_CoA_Flux", DynamicRole.SOURCE, conserved=False),
        AbstractVariable("HMGCR_Enzyme_Rate", DynamicRole.BOTTLENECK, conserved=False),
        InteractionKind.POSITIVE_FEEDBACK,
        "d[HMG]/dt = v_synth - v_deg",
        tau=0.9,
    )
    p6.add_mechanism(
        AbstractVariable("HMGCR_Enzyme_Rate", DynamicRole.BOTTLENECK, conserved=False),
        AbstractVariable("NADPH_Cofactor_Pool", DynamicRole.REGULATOR, conserved=True),
        InteractionKind.NEGATIVE_FEEDBACK,
        "d[NADPH]/dt = - 2 * v_deg",
        tau=1.4,
    )
    p6.add_mechanism(
        AbstractVariable("NADPH_Cofactor_Pool", DynamicRole.REGULATOR, conserved=True),
        AbstractVariable("HMGCR_Enzyme_Rate", DynamicRole.BOTTLENECK, conserved=False),
        InteractionKind.THRESHOLD_SWITCH,
        "if NADPH < NADPH_crit -> metabolic_stall = True",
        tau=0.25,
    )
    corpus.append(p6)

    return corpus
