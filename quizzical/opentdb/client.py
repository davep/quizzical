"""The Open Trivia DB client."""

##############################################################################
# Backward compatibility.
from __future__ import annotations

##############################################################################
# Python imports.
from json import loads
from typing import Final

##############################################################################
# HTTPX imports.
from httpx import AsyncClient, HTTPStatusError, RequestError

##############################################################################
# Local imports.
from .category import Category
from .counts import Counts
from .question import Difficulty, Question, Type
from .response import Code


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
        self._overall_counts: Counts | None = None
        """The overall counts of questions in the backend."""
        self._category_counts: dict[int, Counts] = {}
        """The question counts per category."""

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

    async def category(self, category_id: int) -> Category:
        """Get a category based on its ID.

        Args:
            category_id: The ID of the category to get.

        Returns:
            The category data.
        """
        return next(
            category
            for category in await self.categories()
            if category.id == category_id
        )

    async def questions(
        self,
        amount: int = 10,
        category: int | Category | None = None,
        difficulty: Difficulty | None = None,
        of_type: Type | None = None,
    ) -> list[Question]:
        """Get a collection of questions from the API.

        Args:
            amount: The amount of questions to get.
            category: The category of questions to get.
            difficulty: The difficulty of questions to get.
            of_type: The type of question to get.

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
        if of_type is not None:
            params["type"] = of_type

        response = loads(await self._call("api", **params))

        # TODO: for things like invalid or exhausted tokens, or a rate
        # limit, bounce back around, perhaps. For now though just do a
        # simple sanity check.
        Code(response.get("response_code", Code.UNKNOWN)).maybe_raise()

        return [Question(**question) for question in response["results"]]

    async def _counts(self) -> None:
        """Get the low-level counts data."""
        if self._overall_counts is not None:
            return
        counts = loads(await self._call("api_count_global"))
        self._overall_counts = Counts(
            counts["overall"]["total_num_of_questions"],
            counts["overall"]["total_num_of_pending_questions"],
            counts["overall"]["total_num_of_verified_questions"],
            counts["overall"]["total_num_of_rejected_questions"],
        )
        self._category_counts = {
            int(category): Counts(
                category_counts["total_num_of_questions"],
                category_counts["total_num_of_pending_questions"],
                category_counts["total_num_of_verified_questions"],
                category_counts["total_num_of_rejected_questions"],
            )
            for category, category_counts in counts["categories"].items()
        }

    async def overall_counts(self) -> Counts:
        """Gets the overall question counts.

        Returns:
            The overall counts from the backend.

        Note:
            Because this is a low-importance value that won't change very
            often, the value is cached for the lifetime of the client
            object.
        """
        await self._counts()
        assert self._overall_counts is not None
        return self._overall_counts

    async def category_counts(self) -> dict[int, Counts]:
        """Gets the question counts per category.

        Returns:
            The question counts per category.

        Note:
            Because this is a low-importance value that won't change very
            often, the value is cached for the lifetime of the client
            object.
        """
        await self._counts()
        return self._category_counts


### client.py ends here
