import numpy as np
import pandas as pd
import pymatching

from neural_network_qec.circuit import circuit_info
from neural_network_qec.viz import threshold_plot

shots = 1000000

sweep_data = []

for p in np.logspace(-3, -1.3, 9):
    error_list = []

    print(f" p={p} started......")

    print("\n")

    for d in range(3, 9, 2):
        print(f" d={d} for p={p} started......")

        c = circuit_info(d, d, p, p * 10, p, p * 10)

        dets, obs = c.sample_detectors(shots)
        # print("detector events : \n",dets.astype(int))
        # print(f"observable matrxi: \n", obs.astype(int))

        # c.circuit_diagram()

        dem = c.detector_error_model()
        # print("DEM :\n", dem)
        # print('\n')

        matcher = pymatching.Matching.from_detector_error_model(dem)
        # print(f" nodes: {m.num_nodes} and edges: {m.num_edges}")

        pred = matcher.decode_batch(dets)
        # print(pred)

        # counting the number of mistakes by comparing obs and pred
        num_errors = np.sum(np.any(pred != obs, axis=1))
        print(f"number of errors for d={d} and p={p}:", num_errors)

        # logical error rate per shot
        ler = num_errors / shots
        print(f"LER per shot for d={d} and p={p} is:", ler)

        # normalising LER per round
        # e = ler / d
        safe_ler_shot = np.clip(ler, 0.0, 0.5)
        e = 0.5 * (1 - (1 - 2 * safe_ler_shot) ** (1 / d))
        print(f"normalised to LER per round value for d={d} and p={p} :", e)

        error_list.append(e)

        run_metrics = {
            "distance": d,
            "physical_p": p,
            "LER_per_round": e,
        }

        print(f" d={d} for p={p} ended......")
        print("\n")

        sweep_data.append(run_metrics)
    # LER pershot per round list
    print(f"LER per round list for p={p}:", error_list)

    # supression factors of different "d" in order
    supression_list = []

    for i in range(0, len(error_list) - 1):
        lam = error_list[i] / error_list[i + 1]
        supression_list.append(lam)

    print(f"supression factors list for p={p}:", supression_list)

    print("\n")

    print(f" p={p} ended......")

    print("\n")


# print(sweep_data)

df = pd.DataFrame(sweep_data)

print(df)


threshold_plot(df)
