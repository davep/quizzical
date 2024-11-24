"""Code relating to the data stored by the application."""

##############################################################################
# Local imports.
from .locations import data_dir
from .quiz_parameters import QuizParameters, QuizTimer
from .quizzes_file import quizzes_file

##############################################################################
# Exports.
__all__ = ["data_dir", "QuizParameters", "quizzes_file", "QuizTimer"]

### __init__.py ends here
