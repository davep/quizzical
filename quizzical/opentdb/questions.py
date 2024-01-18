"""Provides a class that holds questions pulled from the API."""

##############################################################################
# Python imports.
from dataclasses import dataclass, field
from typing import Any
from typing_extensions import Self

##############################################################################
# Local imports.
from .response import Response


##############################################################################
@dataclass
class Questions(Response):
    results: list[dict[str, str]] = field(default_factory=list)
    """The results."""

    def populate_with(self, data: dict[str, Any]) -> Self:
        """Populate the response with values from the given data.

        Args:
            data: The data to populate from.

        Returns:
            Self.
        """
        # TODO: Turn into actual question objects.
        self.results = data["results"]
        return super().populate_with(data)


### questions.py ends here
