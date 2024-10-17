import pytest
from project.cache_decorator import cache_decorator


@cache_decorator(cache_limit=2)
def add_numbers(a, b):
    return a + b


@pytest.mark.parametrize(
    "args, expected",
    [
        ((1, 2), 3),
        ((5, 3), 8),
        ((10, 20), 30),
    ],
)
def test_cache_content(args, expected):
    result = add_numbers(*args)
    assert result == expected

    cache_keys = list(add_numbers.cache.keys())
    cache_values = list(add_numbers.cache.values())

    if len(cache_keys) == 3:
        assert cache_values == [8, 30]


def test_cache_decorator_exceptions():
    with pytest.raises(ValueError, match="cache_limit must be a non-negative integer."):
        cache_decorator(cache_limit=-1)

    with pytest.raises(ValueError, match="cache_limit must be a non-negative integer."):
        cache_decorator(cache_limit=1.5)


@cache_decorator(cache_limit=3)
def subtract_numbers(a, b):
    return a - b


@pytest.mark.parametrize(
    "args, kwargs, expected",
    [
        ((), {"a": 10, "b": 5}, 5),
        ((), {"a": 20, "b": 10}, 10),
        ((), {"a": 30, "b": 15}, 15),
        ((), {"a": 10, "b": 5}, 5),
    ],
)
def test_cache_decorator_named_args(args, kwargs, expected):
    assert subtract_numbers(*args, **kwargs) == expected


@pytest.mark.parametrize(
    "args, kwargs, expected",
    [
        ((1,), {"b": 2}, 3),
        ((5,), {"b": 3}, 8),
        ((), {"a": 10, "b": 5}, 15),
    ],
)
def test_cache_decorator_mixed_args(args, kwargs, expected):
    assert add_numbers(*args, **kwargs) == expected
