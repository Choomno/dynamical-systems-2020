"""Scientific checks for modern companions; historical code remains untouched."""

import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "reconstructed"))
from bifurcation_lyapunov import iterate_parameter, sample, superstable
from newton_basins import basins, classify


def test_parameter_derivative_matches_difference():
    mu, h = 3.55, 1e-7
    _x, derivative = iterate_parameter(mu, 8)
    numerical = (iterate_parameter(mu + h, 8)[0] - iterate_parameter(mu - h, 8)[0]) / (
        2 * h
    )
    assert derivative == pytest.approx(numerical, rel=1e-6)


@pytest.mark.parametrize(
    "period,guess,expected",
    [
        (2, 3.24, 1 + np.sqrt(5)),
        (4, 3.50, 3.4985616993),
        (8, 3.555, 3.5546408628),
        (16, 3.5667, 3.5666673799),
        (32, 3.5692, 3.5692435316),
    ],
)
def test_primitive_superstable(period, guess, expected):
    mu = superstable(guess, period)
    assert mu == pytest.approx(expected, abs=1e-9)
    assert abs(iterate_parameter(mu, period)[0] - 0.5) < 1e-12


def test_lower_period_is_rejected():
    with pytest.raises(ValueError, match="lower-period"):
        superstable(2.0, 4)


def test_lyapunov_fixed_point_and_zero_derivative():
    _, exponent = sample(np.array([2.8, 2.0]), transient=1000, kept=400, x0=0.1)
    assert exponent[0] == pytest.approx(np.log(0.8), abs=1e-10)
    assert exponent[1] == -np.inf


def test_newton_classification_and_unresolved():
    roots = np.exp(2j * np.pi * np.arange(4) / 4)
    np.testing.assert_array_equal(classify(roots + 0.001), np.arange(4))
    assert classify(np.array([0j, complex("nan")])).tolist() == [-1, -1]
    assert classify(np.array([0.1 + 0.2j]), iterations=1).item() == -1


def test_rowwise_matches_direct():
    axis, labels = basins(17)
    direct = classify(axis[None, :] + 1j * axis[:, None])
    np.testing.assert_array_equal(labels, direct)
