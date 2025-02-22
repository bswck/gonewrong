from __future__ import annotations

from collections.abc import Generator
from contextlib import contextmanager
from functools import partial

import pytest

from gonewrong import DEFAULT_MESSAGE, catch_group
from gonewrong._compat import BaseExceptionGroup


@contextmanager
def raises_group(like: BaseExceptionGroup[BaseException]) -> Generator[None]:
    try:
        with pytest.raises(type(like)) as raises_context:
            yield
        if excinfo := raises_context._excinfo:  # noqa: SLF001
            _, exc, _ = excinfo
            raise exc from None
    except BaseExceptionGroup as g:
        to_types = partial(map, type)
        assert list(to_types(g.exceptions)) == list(to_types(like.exceptions))  # noqa: PT017


group = partial(BaseExceptionGroup, DEFAULT_MESSAGE)


@pytest.mark.parametrize(
    ("which", "sample_error", "expected"),
    [
        ([Exception], ValueError, group([ValueError()])),
        ([BaseException], ValueError, group([ValueError()])),
        ([BaseException], SystemExit, group([SystemExit()])),
    ],
)
def test_happy_path_integration(
    which: list[type[BaseException]],
    sample_error: Exception | type[Exception],
    expected: BaseExceptionGroup[BaseException],
) -> None:
    with raises_group(expected), catch_group(which) as maybe, maybe:
        raise sample_error


def test_no_swallow() -> None:
    with raises_group(group([AttributeError()])), catch_group():
        raise AttributeError
