from traitlets import TraitType
import six

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
    asked_arg_names = callback.__code__.co_varnames[:callback.__code__.co_argcount]
    asked_arg_values = []
    missing_args = []
    for asked_arg_name in asked_arg_names:
        if asked_arg_name in args:
            asked_arg_values.append(args[asked_arg_name])
        else:
            missing_args.append(asked_arg_name)
    if missing_args:
        raise TypeError(
            '{}() missing required positional argument: {}'.format(
                callback.__code__.co_name,
                ', '.join(missing_args)
            )
        )
    return callback(*asked_arg_values)

# copy-pasted from the master of Traitlets source
class Callable(TraitType):
    """A trait which is callable.
    Notes
    -----
    Classes are callable, as are instances
    with a __call__() method."""

    info_text = 'a callable'

    def validate(self, obj, value):
        if six.callable(value):
            return value
        else:
            self.error(obj, value)
