# Cobweb (web) diagrams for the logistic map x -> mu x (1 - x).
# 2026 reconstruction of a lost 2020 program.

import os
import numpy as np
import matplotlib.pyplot as plt


def logistic(mu, x):
    return mu * x * (1 - x)


def cobweb(ax, f, x0, n, title=""):
    """Draw y = f(x), the diagonal y = x, and the staircase of n iterates starting at x0."""
    t = np.linspace(0, 1, 500)
    ax.plot(t, f(t), color="#2a78d6", lw=2)
    ax.plot(t, t, color="#898781", lw=1)

    x = x0
    path_x, path_y = [x], [0]
    for _ in range(n):
        y = f(x)
        path_x += [x, y]          # vertical step to the graph, then horizontal to the diagonal
        path_y += [y, y]
        x = y
    ax.plot(path_x, path_y, color="#eb6834", lw=1)
    ax.plot(path_x[0], path_y[0], "o", color="#eb6834", ms=5)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.set_title(title)


if __name__ == "__main__":
    cases = [(2.8, "fixed point"), (3.3, "period 2"), (3.5, "period 4"), (3.9, "chaos")]
    fig, axes = plt.subplots(2, 2, figsize=(8, 8))
    for ax, (mu, label) in zip(axes.ravel(), cases):
        cobweb(ax, lambda x, mu=mu: logistic(mu, x), x0=0.1, n=60 if mu < 3.8 else 40,
               title=rf"$\mu = {mu}$ ({label})")
    fig.tight_layout()
    fig.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), "cobweb.png"), dpi=150)
