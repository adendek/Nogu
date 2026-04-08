from functools import reduce
from typing import Callable


def chain(*functions: callable) -> Callable:
    """Build a data processing chain by applying a list of transformations.

    Given a sequence of callable functions, this function executes their composition.
    For more details, see [1].

    Args:
        functions (Sequence[Callable]): A sequence of chainable functions.

    Raises:
        ValueError: If any argument is not a callable function.

    Returns:
        Callable: A single function that is the composition of the input functions.

    References:
        [1] https://mathieularose.com/function-composition-in-python
    """
    if any(not callable(function) for function in functions):
        raise ValueError("Every chain args must be a callable function")
    return lambda x: reduce(lambda f, g: g(f), functions, x)
