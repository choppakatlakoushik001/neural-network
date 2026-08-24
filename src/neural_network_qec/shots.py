from neural_network_qec.circuit import circuit_info

c = circuit_info(3,3,0.04,0.01)

#sampler = c.compile_detector_sampler()
print(c.sample_detectors(5))
