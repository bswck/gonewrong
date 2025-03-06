import pytest

from gonewrong._compat import BaseExceptionGroup, ExceptionGroup


# YORE: BUMP 3.9: Remove block
@pytest.mark.skipif("sys.version_info < (3, 11)")
def test_correct_group_classes() -> None:
    assert not BaseExceptionGroup.__module__.startswith("exceptiongroup")
    assert not ExceptionGroup.__module__.startswith("exceptiongroup")
