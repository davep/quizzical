"""The Open Trivia DB client."""

##############################################################################
# Backward compatibility.
from __future__ import annotations

##############################################################################
# Python imports.
from json import loads
from typing_extensions import Final

##############################################################################
# HTTPX imports.
from httpx import AsyncClient, RequestError, HTTPStatusError

##############################################################################
# Local imports.
from .category import Category
from .question import Difficulty, Question, Type


##############################################################################
class OpenTriviaDB:
    """Client for the Open Trivia DB API."""

    AGENT: Final[str] = "Quizzical (https://github.com/davep/quizzical)"
    """The agent string to use when talking to the API."""

    _BASE: Final[str] = "https://opentdb.com/"
    """The base of the URL for the API."""

    class RequestError(Exception):
        """Exception raised if there was a problem making an API request."""

    def __init__(self) -> None:
        """Initialise the API client object."""
        self._client_: AsyncClient | None = None
        """The HTTPX client."""
        self._categories: list[Category] = []
        """The list of categories."""

    @property
    def _client(self) -> AsyncClient:
        """The API client."""
        if self._client_ is None:
            self._client_ = AsyncClient()
        return self._client_

    async def _call(self, module: str, **params: str) -> str:
        """Call on the OpenTDB API.

        Args:
            path: The path for the API call.
            params: The parameters for the call.

        Returns:
            The text returned from the call.
        """
        try:
            response = await self._client.get(
                f"{self._BASE}/{module}.php",
                params=params,
                headers={"user-agent": self.AGENT},
            )
        except RequestError as error:
            raise self.RequestError(str(error))

        try:
            response.raise_for_status()
        except HTTPStatusError as error:
            raise self.RequestError(str(error))

        return response.text

    async def categories(self) -> list[Category]:
        """Get the list of quiz categories.

        Returns:
            The list of quiz categories.
        """
        if self._categories:
            return self._categories
        self._categories = [
            Category(**category)
            for category in loads(await self._call("api_category"))["trivia_categories"]
        ]
        return self._categories

    async def questions(
        self,
        amount: int = 10,
        category: int | Category | None = None,
        difficulty: Difficulty | None = None,
        type: Type | None = None,
    ) -> list[Question]:
        """Get a collection of questions from the API.

        Args:
            amount: The amount of questions to get.
            category: The category of questions to get.
            difficulty: The difficulty of questions to get.
            type: The type of question to get.

        Returns:
            The questions.
        """

        if isinstance(category, Category):
            category = category.id

        params = {"amount": str(amount)}
        if category is not None:
            params["category"] = str(category)
        if difficulty is not None:
            params["difficulty"] = difficulty
        if type is not None:
            params["type"] = type

        response = loads(await self._call("api", **params))

        if response["response_code"] != 0:  # TODO: Use proper value.
            raise Exception(f"Response not good")  # TODO: Proper exceptions

        return [Question(**question) for question in response["results"]]


### client.py ends here
