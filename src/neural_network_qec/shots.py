import numpy as np
import pymatching

from neural_network_qec.circuit import circuit_info

# error probability
p = 0.005
n = 3

error_list = []
while n <= 7:
    c = circuit_info(n, n, p, p, p, p)

    shots = 1000000
    dets, obs = c.sample_detectors(shots)
    # print("detector events : \n",dets.astype(int))
    # print(f"observable matrxi: \n", obs.astype(int))

    # c.circuit_diagram()

    print("\n")

    dem = c.detector_error_model()
    # print("DEM :\n", dem)

    # print('\n')

    matcher = pymatching.Matching.from_detector_error_model(dem)
    # print(f" nodes: {m.num_nodes} and edges: {m.num_edges}")

    pred = matcher.decode_batch(dets)
    # print(pred)

    # print('\n')

    # counting the number of mistakes by comparing obs and pred
    num_errors = np.sum(np.any(pred != obs, axis=1))
    print(f"number of errors for {n}:", num_errors)

    # logical error rate per shot
    ler = num_errors / shots
    print(f"LER per shot for distance - {n} is:", ler)

    # normalising o LER per round
    e = ler / n
    print(f"normalised to LER per round value for distance - {n} :", e)

    error_list.append(e)
    n += 2

print("\n")

# LER pershot per round list
print("LER per round list :", error_list)

print("\n")

# supression factors of different "d" in order
supression_list = []
for i in range(0, len(error_list) - 1):
    lam = error_list[i] / error_list[i + 1]
    supression_list.append(lam)

print("supression factors list :", supression_list)
