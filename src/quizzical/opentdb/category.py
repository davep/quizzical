"""Provides a class that holds details of a quiz category."""

##############################################################################
# Python imports.
from dataclasses import dataclass
from html import unescape


##############################################################################
@dataclass
class Category:
    """Class that holds the details of a quiz category."""

    id: int
    """The ID of the category"""

    name: str
    """The name of the category."""

    def __post_init__(self) -> None:
        """Tidy up the question data once it's been loaded up."""
        self.name = unescape(self.name)


### category.py ends here
