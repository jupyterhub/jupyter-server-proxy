from jupyter_server_proxy import utils


def test_call_with_asked_args():
    def _test_func(a, b):
        c = a * b
        return c

    assert utils.call_with_asked_args(_test_func, {
        'a': 5,
        'b': 4,
        'c': 8
    }) == 20
