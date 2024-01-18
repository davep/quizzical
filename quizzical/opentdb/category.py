"""Provides a class that holds details of a quiz category."""

##############################################################################
# Python imports.
from dataclasses import dataclass


##############################################################################
@dataclass
class Category:
    """Class that holds the details of a quiz category."""

    id: int
    """The ID of the category"""

    name: str
    """The name of the category."""


### category.py ends here
