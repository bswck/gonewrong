from __future__ import annotations

import sys

TYPE_CHECKING = False

# YORE: BUMP 3.10: Replace block with lines 9-10
if sys.version_info >= (3, 11):
    BaseExceptionGroup: TypeAlias = BaseExceptionGroup  # noqa: PLW0127, F821
    ExceptionGroup: TypeAlias = ExceptionGroup  # noqa: PLW0127, F821
else:
    from exceptiongroup import BaseExceptionGroup, ExceptionGroup

# YORE: BUMP 3.12: Remove block
if TYPE_CHECKING:
    # YORE: BUMP 3.9: Replace block with line 20
    if sys.version_info >= (3, 10):
        from typing import TypeAlias
    else:
        from typing_extensions import TypeAlias

    if sys.version_info >= (3, 13):
        from typing import TypeVar
    else:
        from typing_extensions import TypeVar

__all__ = (
    "BaseExceptionGroup",
    "ExceptionGroup",
    "TypeAlias",
    "TypeVar",
)
