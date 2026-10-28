"""Test helpers for importing pure Radialight modules without Home Assistant."""

from __future__ import annotations

import importlib.util
import sys
import types
from pathlib import Path

_PACKAGE = "custom_components.radialight_cloud"
_ROOT = Path(__file__).resolve().parents[1]
_PKG_DIR = _ROOT / "custom_components" / "radialight_cloud"


def load_radialight_module(module_name: str):
    """Load a submodule of radialight_cloud without importing package __init__."""
    full_name = f"{_PACKAGE}.{module_name}"
    if full_name in sys.modules:
        return sys.modules[full_name]

    if "custom_components" not in sys.modules:
        cc = types.ModuleType("custom_components")
        cc.__path__ = [str(_ROOT / "custom_components")]
        sys.modules["custom_components"] = cc

    if _PACKAGE not in sys.modules:
        pkg = types.ModuleType(_PACKAGE)
        pkg.__path__ = [str(_PKG_DIR)]
        sys.modules[_PACKAGE] = pkg

    path = _PKG_DIR / f"{module_name}.py"
    spec = importlib.util.spec_from_file_location(full_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[full_name] = module
    spec.loader.exec_module(module)
    return module
