import pytest
from api.routes.v1_experiments import _calculate_significance

def test_statistical_significance_calculation():
    # Clear significant difference (e.g. 5% vs 10% on large sample)
    sig, p_val = _calculate_significance(n_a=2000, c_a=100, n_b=2000, c_b=200)
    assert sig is True
    assert p_val is not None
    assert p_val < 0.05

    # Insignificant difference (e.g. 5.1% vs 5.2%)
    sig_no, p_val_no = _calculate_significance(n_a=1000, c_a=51, n_b=1000, c_b=52)
    assert sig_no is False
    assert p_val_no is not None
    assert p_val_no > 0.05

    # Small sample size (not enough data)
    sig_small, p_val_small = _calculate_significance(n_a=10, c_a=1, n_b=10, c_b=2)
    assert sig_small is False
    assert p_val_small is None
