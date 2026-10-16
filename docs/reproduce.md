# Reproduce the modern experiments

Run from the repository root with Python 3.10 or later:

```sh
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
python reconstructed/bifurcation_lyapunov.py
python reconstructed/cobweb.py
python reconstructed/newton_basins.py --resolution 800
```

For the exact direct dependency versions used in the reconstruction checks,
install `requirements-tested.txt` instead.

To check the maintained reconstruction and tests:

```sh
python -m pip install -r requirements-dev.txt
python -m ruff check .
python -m ruff format --check .
python -m pytest -q
```

`ruff.toml` limits linting and formatting to `reconstructed/` and `tests/`.
The historical `code/`, `figures/`, and `writeup/` are preserved artifacts;
they are excluded from modern style checks and automatic fixes. There is no
package build: run the three scripts above to check figure regeneration.

Each command writes a PNG preview, PDF, and JSON parameters/version record in
`generated/`. The basin and bifurcation commands also save numerical arrays in
NPZ files. Use `--output PATH` to choose a different basename. These outputs are
modern reconstructions; the 2020 sources and figures remain in `code/`,
`figures/`, and `writeup/`.

For the logistic map, the defaults discard 1000 iterates and retain 400 at 4000
parameters in [3.5, 3.8]. Assess finite-time sensitivity by increasing
`--transient`, `--kept`, and `--n-mu`, for example to 2000, 800, and 8000.
The Lyapunov estimate uses the orbit derivative before each update. An exactly
zero derivative gives negative infinity; no numerical floor is added. Such values
are preserved in the NPZ file and omitted from the finite plot, whose vertical
range is [-2, 1]. A positive finite-time estimate alone is not a proof of chaos.
The superstable solver rejects lower periods, vanished derivatives, departures
from (0, 4], and failure to meet its residual tolerance.

Newton basins use one complex row at a time, with resolution bounded by 4096.
The displayed square is [-1, 1]^2. A root receives a color only when
|z^d - 1| <= 10^-8 within the iteration budget. Gray marks singular starts and
unresolved points, including nonfinite iterates. Try `--degree 3` for the other
historical picture or `--iterations 100` to assess iteration sensitivity.

The old write-up cannot yet be rebuilt: its personal `preamble.sty` is absent,
its file paths assume a flat directory, and its preamble needs repair. Its
historical PDF is the authoritative preserved output. A reconstructed edition
would need its own mathematical and layout review.
