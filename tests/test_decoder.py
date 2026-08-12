from neural_network_qec.decoder import syndrome_weight


def test_empty_syndrome_has_zero_weight():
    assert syndrome_weight([0, 0, 0]) == 0


def test_counts_triggered_stabilizers():
    assert syndrome_weight([1, 0, 1, 1]) == 3
