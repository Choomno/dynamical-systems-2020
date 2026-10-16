"""A bounded-memory companion to the historical Newton basin experiment."""
import argparse
import numpy as np
from common import save_figure


def classify(z0, degree=4, iterations=50, tolerance=1e-8):
    """Root indices 0..degree-1, or -1 when no residual-checked root is found."""
    if degree < 2 or iterations < 1 or tolerance <= 0:
        raise ValueError('invalid Newton iteration parameters')
    z = np.asarray(z0, dtype=complex).copy()
    labels = np.full(z.shape, -1, dtype=np.int16)
    active = np.isfinite(z)
    for _ in range(iterations + 1):
        with np.errstate(over='ignore', invalid='ignore'):
            residual = np.abs(z**degree - 1)
        converged = active & (residual <= tolerance)
        angle = np.mod(np.angle(z[converged]), 2*np.pi)
        labels[converged] = np.rint(angle*degree/(2*np.pi)).astype(int) % degree
        active &= ~converged
        if _ == iterations:
            break
        active &= np.isfinite(z) & (np.abs(z) > 1e-14)
        if not active.any():
            break
        with np.errstate(over='ignore', invalid='ignore', divide='ignore'):
            z[active] -= (z[active]**degree - 1)/(degree*z[active]**(degree-1))
    return labels


def basins(resolution=800, degree=4, iterations=50):
    """Process one image row at a time, avoiding multiple full complex grids."""
    if not 2 <= resolution <= 4096 or not 2 <= degree <= 12:
        raise ValueError('resolution must lie in [2,4096] and degree in [2,12]')
    axis = np.linspace(-1, 1, resolution)
    labels = np.empty((resolution, resolution), dtype=np.int16)
    for row, y in enumerate(axis):
        labels[row] = classify(axis + 1j*y, degree, iterations)
    return axis, labels


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--resolution', type=int, default=800)
    parser.add_argument('--degree', type=int, default=4)
    parser.add_argument('--iterations', type=int, default=50)
    parser.add_argument('--output', default='generated/newton_basins')
    args = parser.parse_args()
    axis, labels = basins(args.resolution, args.degree, args.iterations)
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap, BoundaryNorm
    from matplotlib.patches import Patch
    palette = ['#2878b5', '#e87524', '#369959', '#9756a6', '#ca4a4a', '#8c564b',
               '#cf6a9f', '#a58a12', '#24a5a5', '#305a80', '#9acb72', '#f4b85b']
    colors = ['#eeeeee'] + palette[:args.degree]
    cmap = ListedColormap(colors)
    fig, ax = plt.subplots(figsize=(6.5,6), layout='constrained')
    # Pixel centers agree with the sampled domain, including its endpoints.
    half = (axis[1]-axis[0])/2
    ax.imshow(labels, origin='lower', extent=(-1-half,1+half,-1-half,1+half),
              cmap=cmap, norm=BoundaryNorm(np.arange(-1.5,args.degree+.5), cmap.N), interpolation='nearest')
    ax.set(xlabel='Re $z_0$', ylabel='Im $z_0$', title=f'Newton basins for $z^{args.degree}-1$')
    handles = [Patch(color=colors[0], label='not converged / singular')]
    handles += [Patch(color=colors[k+1], label=rf'$e^{{2\pi i\,{k}/{args.degree}}}$') for k in range(args.degree)]
    ax.legend(handles=handles, loc='upper center', bbox_to_anchor=(.5,-.12), ncol=3, fontsize=8)
    save_figure(fig, args.output, vars(args) | {'residual_tolerance':1e-8, 'domain':[-1,1,-1,1],
                'unclassified':int((labels < 0).sum())}, dict(axis=axis, root_index=labels))
    plt.close(fig)


if __name__ == '__main__':
    main()
