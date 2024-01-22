"""Functions for getting the locations of data."""

##############################################################################
# Python imports.
from pathlib import Path

##############################################################################
# XDG imports.
from xdg_base_dirs import xdg_data_home


##############################################################################
def _quizzical_dir(root: Path) -> Path:
    """Given a root, ensure and return the Quizzical directory within it."""
    (save_to := root / "quizzical").mkdir(parents=True, exist_ok=True)
    return save_to


##############################################################################
def data_dir() -> Path:
    """The path to the data directory for the application.

    Returns:
        The path to the data directory for the application.

    Note:
        If the directory doesn't exist, it will be created as a side-effect
        of calling this function.
    """
    return _quizzical_dir(xdg_data_home())


### locations.py ends here
