"""2026 reconstruction of the lost logistic-map experiment; originals are unchanged."""

import argparse

import numpy as np
from common import save_figure


def iterate_parameter(mu, period):
    """Return f_mu^period(1/2) and its parameter derivative."""
    x, dx = 0.5, 0.0
    for _ in range(period):
        x, dx = mu * x * (1 - x), x * (1 - x) + mu * (1 - 2 * x) * dx
    return x, dx


def superstable(mu, period, iterations=50, tolerance=1e-12):
    """Find a primitive superstable orbit by Newton iteration; reject lower periods."""
    if period < 1 or period != int(period) or not 0 < mu <= 4:
        raise ValueError("period must be positive integral and mu must lie in (0, 4]")
    for _ in range(iterations):
        x, dx = iterate_parameter(mu, period)
        if abs(x - 0.5) <= tolerance:
            for divisor in range(1, period):
                if (
                    period % divisor == 0
                    and abs(iterate_parameter(mu, divisor)[0] - 0.5) <= 10 * tolerance
                ):
                    raise ValueError("Newton iteration found a lower-period orbit")
            return mu
        if not np.isfinite(dx) or abs(dx) < np.finfo(float).eps:
            raise RuntimeError("Newton derivative vanished or overflowed")
        candidate = mu - (x - 0.5) / dx
        if not np.isfinite(candidate) or not 0 < candidate <= 4:
            raise RuntimeError("Newton iteration left the logistic parameter interval")
        mu = candidate
    raise RuntimeError("Newton iteration did not converge")


def sample(mu, transient=1000, kept=400, x0=0.5):
    """Finite-time Lyapunov estimate; log(0) remains -infinity, without a floor."""
    mu = np.asarray(mu, dtype=float)
    if transient < 0 or kept < 1 or np.any((mu < 0) | (mu > 4)) or not 0 <= x0 <= 1:
        raise ValueError("invalid sampling parameters")
    x = np.full(mu.shape, x0)
    for _ in range(transient):
        x = mu * x * (1 - x)
    orbit = np.empty((kept, *mu.shape))
    lyap = np.zeros_like(mu)
    with np.errstate(divide="ignore"):
        for k in range(kept):
            lyap += np.log(np.abs(mu * (1 - 2 * x)))
            x = mu * x * (1 - x)
            orbit[k] = x
    return orbit, lyap / kept


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-mu", type=int, default=4000)
    parser.add_argument("--transient", type=int, default=1000)
    parser.add_argument("--kept", type=int, default=400)
    parser.add_argument("--output", default="generated/bifurcation_lyapunov")
    args = parser.parse_args()
    if args.n_mu < 2:
        parser.error("--n-mu must be at least 2")
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    mu = np.linspace(3.5, 3.8, args.n_mu)
    orbit, lyap = sample(mu, args.transient, args.kept)
    marks = [superstable(m, p) for m, p in [(3.555, 8), (3.5667, 16), (3.5692, 32)]]
    fig, (top, bottom) = plt.subplots(
        2, 1, figsize=(7, 7), sharex=True, layout="constrained"
    )
    top.plot(
        np.broadcast_to(mu, orbit.shape).ravel(),
        orbit.ravel(),
        ",k",
        alpha=0.2,
        rasterized=True,
    )
    top.set(ylabel="$x$", title="Logistic map: long-run orbit")
    for positive, color in [(False, "#333333"), (True, "#b44635")]:
        mask = np.isfinite(lyap) & ((lyap > 0) == positive)
        bottom.plot(mu[mask], lyap[mask], ".", color=color, ms=1, rasterized=True)
    for period, value in zip((8, 16, 32), marks):
        bottom.axvline(value, color="#326b94", lw=0.6)
    bottom.text(
        0.98,
        0.96,
        "Blue: superstable periods 8, 16, 32",
        transform=bottom.transAxes,
        ha="right",
        va="top",
        fontsize=8,
    )
    bottom.axhline(0, color=".6", lw=0.5)
    bottom.set(
        xlabel="$\\mu$",
        ylabel="finite-time Lyapunov exponent",
        ylim=(-2, 1),
        xlim=(3.5, 3.8),
    )
    save_figure(
        fig,
        args.output,
        vars(args)
        | {
            "mu_range": [3.5, 3.8],
            "x0": 0.5,
            "superstable": marks,
            "zero_derivative": "negative infinity; omitted from finite plot",
            "lyapunov_plot_limits": [-2, 1],
        },
        {"mu": mu, "orbit": orbit, "lyapunov": lyap},
    )
    plt.close(fig)
    print("superstable parameters:", ", ".join(f"{x:.10f}" for x in marks))


if __name__ == "__main__":
    main()
