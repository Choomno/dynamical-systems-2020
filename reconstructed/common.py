"""Small, local helpers for the reconstructed experiments."""

import json
import platform
from pathlib import Path

import matplotlib
import numpy as np


def save_figure(fig, output, parameters, data=None):
    """Write a preview, a publication figure, and regeneration metadata."""
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    for extension in ("png", "pdf"):
        fig.savefig(output.with_suffix("." + extension), dpi=180)
    metadata = {
        "parameters": parameters,
        "python": platform.python_version(),
        "numpy": np.__version__,
        "matplotlib": matplotlib.__version__,
    }
    output.with_suffix(".json").write_text(json.dumps(metadata, indent=2) + "\n")
    if data is not None:
        np.savez_compressed(output.with_suffix(".npz"), **data)
