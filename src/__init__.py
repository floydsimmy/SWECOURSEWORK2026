"""Package shim: lets bare imports (`from game.X`, `from ui.X`) resolve
when the project is run as `python -m src.main` from the repository root.
Tests do not use this path because pytest.ini sets pythonpath = src directly."""
import os as _os, sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__))
if _HERE not in _sys.path:
    _sys.path.insert(0, _HERE)
