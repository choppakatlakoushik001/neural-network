import stim
#from vizshow import show

class circuit_info:

    def __init__(self,rounds:int,distance:int,before_round_data_depolarization:float,before_measure_flip_probability:float):
         self.rounds=rounds
         self.distance=distance
         self.before_round_data_depolarization=before_round_data_depolarization
         self.before_measure_flip_probability=before_measure_flip_probability


         self.circuit = stim.Circuit.generated(
                "surface_code:rotated_memory_z",
                rounds=rounds,
                distance=distance,
                before_round_data_depolarization=before_round_data_depolarization,
                before_measure_flip_probability=before_measure_flip_probability)


        #return (circuit.diagram("timeline-text"))
        #show(circuit.diagram("timeline-svg"))
        #show(circuit.diagram("timeline-3d-html"))


    def sample_detectors(self,shots:int):
        sampler = self.circuit.compile_detector_sampler()
        detector_events = sampler.sample(shots=shots)
        return detector_events
