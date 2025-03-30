def call_with_asked_args(callback, args):
    """
    Call callback with only the args it wants from args

    Example
    >>> def cb(a):
    ...    return a * 5

    >>> print(call_with_asked_args(cb, {'a': 4, 'b': 8}))
    20
    """
    # FIXME: support default args
    # FIXME: support kwargs
    # co_varnames contains both args and local variables, in order.
    # We only pick the local variables
    asked_arg_names = callback.__code__.co_varnames[: callback.__code__.co_argcount]
    asked_arg_values = []
    missing_args = []
    for asked_arg_name in asked_arg_names:
        if asked_arg_name in args:
            asked_arg_values.append(args[asked_arg_name])
        else:
            missing_args.append(asked_arg_name)
    if missing_args:
        raise TypeError(
            "{}() missing required positional argument: {}".format(
                callback.__code__.co_name, ", ".join(missing_args)
            )
        )
    return callback(*asked_arg_values)


def mime_types_match(pattern: str, value: str) -> bool:
    """
    Compare a MIME type pattern, possibly with wildcards, and a value
    """
    value = value.split(";")[0]  # Remove optional details
    if pattern == value:
        return True

    type, subtype = value.split("/")
    pattern = pattern.split("/")

    if pattern[0] == "*" or (pattern[0] == type and pattern[1] == "*"):
        return True

    return False
