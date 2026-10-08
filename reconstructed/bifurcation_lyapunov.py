# Bifurcation diagram and Lyapunov exponent of the logistic map x -> mu x (1 - x).
# 2026 reconstruction of a lost 2020 program; see figures/bifurcation.pdf for the original output.

import os
import numpy as np
import matplotlib.pyplot as plt

mu_min, mu_max = 3.5, 3.8
n_mu = 4000          # number of parameter values
transient = 1000     # iterations discarded before recording
kept = 400           # iterations plotted and averaged

mu = np.linspace(mu_min, mu_max, n_mu)
x = np.full(n_mu, 0.5)

for _ in range(transient):
    x = mu * x * (1 - x)

orbit = np.empty((kept, n_mu))
lyap = np.zeros(n_mu)
for k in range(kept):
    x = mu * x * (1 - x)
    orbit[k] = x
    # lambda = lim (1/N) sum log|f'(x_n)|, with f'(x) = mu (1 - 2x)
    lyap += np.log(np.abs(mu * (1 - 2 * x)) + 1e-300)
lyap /= kept


def superstable(mu, N, iterations=50):
    """Newton's method in mu for f^N(1/2) = 1/2, carrying d x / d mu along the orbit."""
    for _ in range(iterations):
        x, dx = 0.5, 0.0
        for _ in range(N):
            x, dx = mu * x * (1 - x), x * (1 - x) + mu * (1 - 2 * x) * dx
        mu = mu - (x - 0.5) / dx
    return mu


# superstable parameters of period 8, 16, 32 (starting guesses read off the plot)
marks = [superstable(m0, N) for m0, N in [(3.555, 8), (3.5667, 16), (3.5692, 32)]]

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 9), sharex=True)

ax1.plot(np.broadcast_to(mu, orbit.shape).ravel(), orbit.ravel(), ",k", alpha=0.25)
ax1.set_title("Bifurcation diagram")
ax1.set_ylabel("x")

chaotic = lyap > 0
ax2.plot(mu[~chaotic], lyap[~chaotic], ".k", ms=0.8)
ax2.plot(mu[chaotic], lyap[chaotic], ".", color="red", ms=0.8)
ax2.axhline(0, color="gray", lw=0.5)
for m in marks:
    ax2.axvline(m, color="tab:blue", lw=0.8)
ax2.set_ylim(-2, 1)
ax2.set_xlim(mu_min, mu_max)
ax2.set_title("Lyapunov exponent")
ax2.set_xlabel(r"$\mu$")

fig.tight_layout()
fig.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), "bifurcation_lyapunov.png"), dpi=150)
print("superstable parameters (periods 8, 16, 32):", ", ".join(f"{m:.7f}" for m in marks))
