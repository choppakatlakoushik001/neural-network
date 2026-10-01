import numpy as np
import sinter

from neural_network_qec.circuit import circuit_info

distances = [3, 5, 7]

p_sweep = np.logspace(-3, -1.7, 9)


def main():
    tasks = []

    for d in distances:
        for p in p_sweep:
            for rounds in [d, d * 2, d * 3]:
                c = circuit_info(rounds, d, p, p * 10, p, p * 10)

                task = sinter.Task(
                    circuit=c.circuit,
                    json_metadata={
                        "d": d,
                        "p": p,
                        "rounds": rounds,
                        "noise_model": "asymmetric_10x",
                    },
                )
                tasks.append(task)

    print(f"Generated {len(tasks)} simulation tasks. Handing off to Sinter.....")

    sinter.collect(
        num_workers=6,
        tasks=tasks,
        decoders=["pymatching"],
        max_shots=1000000,
        max_errors=1000,
        save_resume_filepath="data/sinter_asymmetric_10x.csv",
    )

    print("csv is ready")
    # print("Sweep complete. Saving data to disk...")


# sinter starts workers with "spawn", which re-imports this file in each worker.
if __name__ == "__main__":
    main()
