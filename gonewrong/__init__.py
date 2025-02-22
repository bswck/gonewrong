from __future__ import annotations

from collections.abc import Generator, Iterable, MutableSequence
from contextlib import _GeneratorContextManager, contextmanager

from gonewrong._compat import BaseExceptionGroup

__all__ = ("catch_group",)

DEFAULT_MESSAGE = "Got some errors"

TYPE_CHECKING = False

if TYPE_CHECKING:
    from gonewrong._compat import TypeVar

    _ExcT_contra = TypeVar(
        "_ExcT_contra",
        bound=BaseException,
        default=Exception,
        contravariant=True,
    )


@contextmanager
def collect(
    what: tuple[type[_ExcT_contra], ...],
    into: MutableSequence[_ExcT_contra],
) -> Generator[None]:
    try:
        yield
    except what as exception:
        into.append(exception)


@contextmanager
def catch_group(
    to_catch: Iterable[type[_ExcT_contra]] = (Exception,),  # type: ignore[assignment]
    *,
    message: str = DEFAULT_MESSAGE,
    group_class: type[BaseExceptionGroup[_ExcT_contra]] = BaseExceptionGroup,
) -> Generator[_GeneratorContextManager[None]]:
    caught: list[_ExcT_contra] = []
    # Normalize arbitrary iterables
    to_catch = (*to_catch,)

    try:
        yield collect(to_catch, caught)
    except to_catch as exception:
        caught.append(exception)

    if caught:
        try:
            raise group_class(message, caught.copy())
        finally:
            caught.clear()
