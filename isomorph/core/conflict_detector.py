"""
ISOMORPH: Dialectic Conflict Detector
Uncovers silent axiomatic collisions, hidden premise incompatibilities,
and unstated physical constraint violations across independent papers.
"""

from __future__ import annotations
import uuid
from typing import List, Optional
from .models import ResearchArtifact, DialecticCollision, SystemRegime, DynamicRole


class DialecticConflictDetector:
    """
    Evaluates whether two papers published in different silos rely on
    mutually contradictory foundational assumptions.
    """

    @staticmethod
    def detect_collisions(
        paper_a: ResearchArtifact, paper_b: ResearchArtifact
    ) -> List[DialecticCollision]:
        collisions: List[DialecticCollision] = []

        # Check 1: Equilibrium vs. Far-from-equilibrium collision
        # If one paper assumes steady-state equilibrium while the other demonstrates
        # that the coupled mechanism drives the system into non-equilibrium dissipation.
        if (
            paper_a.regime == SystemRegime.EQUILIBRIUM
            and paper_b.regime == SystemRegime.FAR_FROM_EQUILIBRIUM
        ):
            collisions.append(
                DialecticCollision(
                    collision_id=f"COL-{uuid.uuid4().hex[:8].upper()}",
                    paper_a=paper_a,
                    paper_b=paper_b,
                    conflicting_premise="Equilibrium Assumption vs. Dissipative Non-Equilibrium",
                    mathematical_contradiction=(
                        f"{paper_a.paper_id} assumes detailed balance / quasi-static equilibrium (dEntropy/dt = 0), "
                        f"whereas {paper_b.paper_id} proves that the shared feedback architecture generates "
                        f"positive entropy production (dSigma/dt > 0), rendering equilibrium approximations invalid."
                    ),
                    epistemic_implication=(
                        f"The analytical conclusions in {paper_a.title} may collapse under real-world "
                        f"perturbations documented in {paper_b.title}."
                    ),
                )
            )

        # Check 2: Infinite Reservoir (Conservation) contradiction
        # If paper A assumes source pool is unconstrained, but paper B identifies that variable as conserved/depletable
        for name_a, var_a in paper_a.variables.items():
            for name_b, var_b in paper_b.variables.items():
                if var_a.role == DynamicRole.SOURCE and not var_a.conserved:
                    if var_b.role == DynamicRole.SOURCE and var_b.conserved:
                        # Shared role mismatch
                        collisions.append(
                            DialecticCollision(
                                collision_id=f"COL-{uuid.uuid4().hex[:8].upper()}",
                                paper_a=paper_a,
                                paper_b=paper_b,
                                conflicting_premise="Infinite Flux Reservoir vs. Strictly Conserved Source Pool",
                                mathematical_contradiction=(
                                    f"Variable '{name_a}' in {paper_a.paper_id} assumes continuous replenishment "
                                    f"without exhaustion, whereas the analogous pool '{name_b}' in {paper_b.paper_id} "
                                    f"is bounded by finite sum conservation (sum(X_i) = C)."
                                ),
                                epistemic_implication=(
                                    f"If the conservation constraint demonstrated in {paper_b.domain} applies "
                                    f"to {paper_a.domain}, the stability regime predicted by {paper_a.paper_id} "
                                    f"will undergo premature critical shutdown."
                                ),
                            )
                        )
                        break

        # Check 3: Mutually Exclusive Boundary Conditions
        for b_a in paper_a.assumed_boundary_conditions:
            for b_b in paper_b.assumed_boundary_conditions:
                b_a_l, b_b_l = b_a.lower(), b_b.lower()
                if (
                    ("frictionless" in b_a_l and "viscous" in b_b_l)
                    or ("linear" in b_a_l and "non-linear" in b_b_l)
                    or ("homogeneous" in b_a_l and "clustered" in b_b_l)
                ):
                    collisions.append(
                        DialecticCollision(
                            collision_id=f"COL-{uuid.uuid4().hex[:8].upper()}",
                            paper_a=paper_a,
                            paper_b=paper_b,
                            conflicting_premise=f"Boundary Condition Clash: '{b_a}' vs. '{b_b}'",
                            mathematical_contradiction=(
                                f"{paper_a.paper_id} fixes boundary condition to '{b_a}', whereas "
                                f"{paper_b.paper_id} establishes '{b_b}' under identical dynamical scales."
                            ),
                            epistemic_implication=(
                                f"A decisive empirical experiment is required to settle whether {paper_a.domain} "
                                f"or {paper_b.domain} boundary constraints govern the transition regime."
                            ),
                        )
                    )

        return collisions
