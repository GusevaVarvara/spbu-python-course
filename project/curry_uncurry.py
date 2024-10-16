def curry_explicit(function, arity):
    if not isinstance(arity, int) or arity < 0:
        raise ValueError("Arity must be a non-negative integer.")

    def curried_function(*args):
        if len(args) > arity:
            raise ValueError("Too many arguments passed to the function.")

        if len(args) == arity:
            return function(*args)

        return lambda *new_args: curried_function(*(args + new_args))

    return curried_function


def uncurry_explicit(function, arity):
    if not isinstance(arity, int) or arity < 0:
        raise ValueError("Arity must be a non-negative integer.")

    def uncurried_function(*args):
        if len(args) != arity:
            raise ValueError("Incorrect number of arguments passed to the function.")

        result = function
        for arg in args:
            result = result(arg)

        return result

    return uncurried_function
