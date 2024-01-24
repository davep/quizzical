"""Provides code for dealing with response values."""

##############################################################################
# Python imports.
from enum import Enum


##############################################################################
class NoResults(Exception):
    """Exception raised if there are no results."""


##############################################################################
class InvalidParameter(Exception):
    """Exception raised if there is an invalid parameter."""


##############################################################################
class TokenNotFound(Exception):
    """Exception raised if the passed token isn't found."""


##############################################################################
class TokenEmpty(Exception):
    """Exception raised if the given token has used all possible questions."""


##############################################################################
class RateLimit(Exception):
    """Exception raised if there have been too many requests."""


##############################################################################
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

    Arguments passed in aren't valid. (Ex. Amount = Five)
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

    def maybe_raise(self) -> None:
        """Raise any appropriate exceptions based on the code."""
        if self is Code.SUCCESS:
            return
        try:
            raise {
                Code.NO_RESULTS: NoResults,
                Code.INVALID_PARAMETER: InvalidParameter,
                Code.TOKEN_NOT_FOUND: TokenNotFound,
                Code.TOKEN_EMPTY: TokenEmpty,
                Code.RATE_LIMIT: RateLimit,
            }[self]()
        except KeyError:
            raise ValueError(f"Not a valid response code: {self}") from None


### response.py ends here
