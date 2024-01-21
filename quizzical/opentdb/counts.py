"""Provides a class that holds counts."""

##############################################################################
# Python imports.
from dataclasses import dataclass


##############################################################################
@dataclass
class Counts:
    """Class that holds the counts of questions."""

    questions: int
    """The total number of questions."""

    pending: int
    """The number of pending questions."""

    verified: int
    """The number of verified questions."""

    rejected: int
    """The number of rejected questions."""


### counts.py ends here
