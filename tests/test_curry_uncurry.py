import pytest
from project.curry_uncurry import curry_explicit, uncurry_explicit


@pytest.mark.parametrize(
    "x, y, z, expected",
    [
        (17, 28, 42, "<17, 28, 42>"),
        (5, 92, 11, "<5, 92, 11>"),
        (9, 12, 7, "<9, 12, 7>"),
        (21, 33, 10, "<21, 33, 10>"),
        (8, 14, 25, "<8, 14, 25>"),
    ],
)
def test_curry_explicit(x, y, z, expected):
    f = curry_explicit(lambda a, b, c: f"<{a}, {b}, {c}>", 3)

    assert f(x)(y)(z) == expected

    with pytest.raises(ValueError, match="Too many arguments passed to the function."):
        f(x, y, z, 99)


@pytest.mark.parametrize(
    "x, y, z, expected",
    [
        (17, 28, 42, "<17, 28, 42>"),
        (5, 92, 11, "<5, 92, 11>"),
        (9, 12, 7, "<9, 12, 7>"),
        (21, 33, 10, "<21, 33, 10>"),
        (8, 14, 25, "<8, 14, 25>"),
    ],
)
def test_uncurry_explicit(x, y, z, expected):
    f_curried = curry_explicit(lambda a, b, c: f"<{a}, {b}, {c}>", 3)
    f_uncurried = uncurry_explicit(f_curried, 3)

    assert f_uncurried(x, y, z) == expected

    with pytest.raises(
        ValueError, match="Incorrect number of arguments passed to the function."
    ):
        f_uncurried(x, y)


@pytest.mark.parametrize(
    "x, y, z, w, expected",
    [
        (10, 5, 2, 3, 17),
        (12, 7, 3, 9, 24),
        (1, 2, 3, 4, 3),
        (100, 50, 25, 75, 1275),
        (5, 4, 3, 2, 15),
    ],
)
def test_combined_curry_uncurry(x, y, z, w, expected):
    def complex_function(a, b, c, d):
        return a + b * c - d

    f_curried = curry_explicit(complex_function, 4)

    assert f_curried(x)(y)(z)(w) == expected

    f_uncurried = uncurry_explicit(f_curried, 4)

    assert f_uncurried(x, y, z, w) == expected


@pytest.mark.parametrize("arity", [-1, 1.5])
def test_curry_explicit_exceptions(arity):
    with pytest.raises(ValueError, match="Arity must be a non-negative integer."):
        curry_explicit(lambda x: x, arity)


@pytest.mark.parametrize("arity", [-1, 1.5])
def test_uncurry_explicit_exceptions(arity):
    f = curry_explicit(lambda x, y: x + y, 2)

    with pytest.raises(ValueError, match="Arity must be a non-negative integer."):
        uncurry_explicit(f, arity)
