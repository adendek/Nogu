from functools import partial
from typing import Any, Callable, List

import numpy as np
from parameterized import parameterized

from nogu.tests import BaseTestCase
from nogu.utils import chain


def evaluate_functions(function_list: List[Callable], function_input: Any) -> Any:
    """Evaluate iteratively the function composition.

    Args:
    function_list : List[Callable]  a list of functions to be evaluated
    function_input : Any
        a function parameter to be passed to the first function in the evaluation list

    Example:
        function_list [f,g,h]
        result  = h(g(f(x)))
    """
    if len(function_list) == 0:
        return None
    result = function_list[0](function_input)
    if len(function_list) == 1:
        return result
    for function in function_list[1:]:
        result = function(result)
    return result


class NonCallableClass:
    """An example of a non-callable class.

    This class does not provide an implementation for the __call__ method,
    and thus calling an instance of this class directly will raise an exception.

    Example:
        a = NonCallableClass(2)
        a()  # This will raise an exception.
    """

    def __init__(self, val):
        self.a = val

    def a(self):
        """Dummy method to return the stored value.

        Returns:
            The stored value.
        """
        return self.a


class TestChain(BaseTestCase):
    """Test cases for the `chain` function.

    These tests verify the behavior of the `chain` function with various types of.
    """

    @parameterized.expand(
        [
            [[lambda x: x + 1, lambda x: x**2, lambda x: x - 1], 1],
            [[lambda x: x + 1], 1],
        ]
    )
    def test_chain_scalar_input(
        self, function_lists: List[Callable], function_input: Any
    ):
        """Test the `chain` function with scalar input.

        Args:
            function_lists (List[Callable]): A list of functions to be chained.
            function_input (Any): The input value to be passed through the chain of functions.
        """
        expected_result = evaluate_functions(function_lists, function_input)
        chain_to_test = chain(*function_lists)
        self.assertEqual(chain_to_test(function_input), expected_result)

    @parameterized.expand(
        [
            [
                [np.sin, partial(np.sum, axis=1)],
                np.random.randint(1, 100, size=(100, 2, 3)),
            ],
            [
                [np.sin, lambda x: x[:, np.newaxis]],
                np.random.randint(0, 100, size=(100, 2, 3)),
            ],
        ]
    )
    def test_chain_scalar_np_array_input(
        self, function_lists: List[Callable], function_input: Any
    ):
        """Test the `chain` function with NumPy array input.

        Args:
            function_lists (List[Callable]): A list of functions to be chained.
            function_input (Any): The input NumPy array to be passed through the chain of functions.
        """
        expected_result = evaluate_functions(function_lists, function_input)
        chain_to_test = chain(*function_lists)
        self.assert_almost_equal(chain_to_test(function_input), expected_result)

    @parameterized.expand(
        [
            [[lambda x: x + 1, lambda x: x**2, lambda x: x - 1, 1], 1],
            [[lambda x: x + 1, "1"], 1],
            [[lambda x: x + 1, NonCallableClass(2)], 1],
        ]
    )
    def test_chain_raise_exception_when_none_callable_function_provided(
        self, function_lists: List[Any], function_input: Any
    ):
        """Test the `chain` function to ensure it raises an exception when a non-callable function is provided.

        Args:
            function_lists (List[Any]): A list of functions and/or non-callable objects to be chained.
            function_input (Any): The input value to be passed through the chain of functions.

        """
        with self.assertRaises(ValueError):
            chain(*function_lists)(function_input)
