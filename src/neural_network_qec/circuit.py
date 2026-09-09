from typing import Literal

import stim

DiagramKind = Literal[
    "timeline-text",
    "timeline-svg",
    "timeline-svg-html",
    "timeline-3d",
    "timeline-3d-html",
    "detslice-text",
    "detslice-svg",
    "detslice-svg-html",
    "matchgraph-svg",
    "matchgraph-svg-html",
    "matchgraph-3d",
    "matchgraph-3d-html",
    "timeslice-svg",
    "timeslice-svg-html",
    "detslice-with-ops-svg",
    "detslice-with-ops-svg-html",
    "interactive",
    "interactive-html",
]


class circuit_info:
    def __init__(
        self,
        rounds: int,
        distance: int,
        before_round_data_depolarization: float,
        before_measure_flip_probability: float,
        after_clifford_depolarization: float,
        after_reset_flip_probability: float,
    ):
        self.rounds = rounds
        self.distance = distance
        self.before_round_data_depolarization = before_round_data_depolarization
        self.before_measure_flip_probability = before_measure_flip_probability
        self.after_clifford_depolarization = after_clifford_depolarization
        self.after_reset_flip_probability = after_reset_flip_probability

        self.circuit = stim.Circuit.generated(
            "surface_code:rotated_memory_z",
            rounds=rounds,
            distance=distance,
            after_clifford_depolarization=after_clifford_depolarization,
            before_round_data_depolarization=before_round_data_depolarization,
            before_measure_flip_probability=before_measure_flip_probability,
            after_reset_flip_probability=after_reset_flip_probability,
        )

    def sample_detectors(self, shots: int):
        sampler = self.circuit.compile_detector_sampler()
        detector_events, observables = sampler.sample(
            shots=shots, separate_observables=True
        )
        return detector_events, observables

    def circuit_diagram(
        self, kind: DiagramKind = "timeline-svg", name: str = "circuit"
    ):
        """Render the diagram to a file and open it in the browser."""
        from neural_network_qec.viz import show

        return show(self.circuit.diagram(kind), name=name)

    def detector_error_model(self):
        dem = self.circuit.detector_error_model(decompose_errors=True)
        return dem
