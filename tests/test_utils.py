from jupyter_server_proxy import utils


def test_call_with_asked_args():
    def _test_func(a, b):
        c = a * b
        return c

    assert utils.call_with_asked_args(_test_func, {"a": 5, "b": 4, "c": 8}) == 20


def test_mime_types_match():
    # Exact match
    assert utils.mime_types_match("text/plain", "text/plain")
    assert not utils.mime_types_match("text/plain", "text/html")

    # With optional parameters
    assert utils.mime_types_match("text/plain", "text/plain;charset=UTF-8")
    assert not utils.mime_types_match("text/plain", "text/html;charset=UTF-8")

    # With a single widcard
    assert utils.mime_types_match("*", "text/plain")
    assert utils.mime_types_match("*", "text/plain;charset=UTF-8")

    # With both components wildcard
    assert utils.mime_types_match("*/*", "text/plain")
    assert utils.mime_types_match("*/*", "text/plain;charset=UTF-8")

    # With a subtype wildcard
    assert utils.mime_types_match("text/*", "text/plain")
    assert not utils.mime_types_match("image/*", "text/plain")

    assert utils.mime_types_match("text/*", "text/plain;charset=UTF-8")
    assert not utils.mime_types_match("image/*", "text/plain;charset=UTF-8")
