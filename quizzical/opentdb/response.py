"""Base class for responses from the API."""

##############################################################################
# Python imports.
from dataclasses import dataclass
from enum import Enum
from typing import Any
from typing_extensions import Self


##############################################################################
@dataclass
class Response:
    """Base class for responses from the API."""

    class Code(Enum):
        """The response codes that the trivia API can send back."""

        UNKNOWN = -1
        """The response code is so far unknown."""

        SUCCESS = 0
        """Returned results successfully."""

        NO_RESULTS = 1
        """Could not return results.

        The API doesn't have enough questions for your query. (Ex. Asking
        for 50 Questions in a Category that only has 20.)
        """

        INVALID_PARAMETER = 2
        """Contains an invalid parameter.

        Arguements passed in aren't valid. (Ex. Amount = Five)
        """

        TOKEN_NOT_FOUND = 3
        """Session Token does not exist."""

        TOKEN_EMPTY = 4
        """Session Token has returned all possible questions for the specified query.

        Resetting the Token is necessary.
        """

        RATE_LIMIT = 5
        """Too many requests have occurred.

        Each IP can only access the API once every 5 seconds.
        """

    response_code: Code = Code.UNKNOWN
    """The response code from the API."""

    def populate_with(self, data: dict[str, Any]) -> Self:
        """Populate the response with values from the given data.

        Args:
            data: The data to populate from.

        Returns:
            Self.
        """
        self.response_code = self.Code(data.get("response_code", self.Code.UNKNOWN))
        return self


### response.py ends here
