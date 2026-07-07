"""Executor abstractions for concurrent workflow demonstrations.

The assignment asks each group to support concurrent execution through an
Executor/Future contract. This module keeps the implementation lightweight and
standard-library only, using concurrent.futures for the threaded adapter.
"""

from __future__ import annotations

from concurrent.futures import Future as ConcurrentFuture, ThreadPoolExecutor
from typing import Callable, Protocol, TypeVar, Generic

T = TypeVar("T")


class FutureLike(Protocol[T]):
    """Minimal Future contract used by the workflow engine tests/demo."""

    def result(self, timeout: float | None = None) -> T: ...

    def cancel(self) -> bool: ...

    def done(self) -> bool: ...


class Executor(Protocol):
    """Minimal executor contract compatible with ThreadPoolExecutor/asyncio adapters."""

    def submit(self, fn: Callable[..., T], *args, **kwargs) -> FutureLike[T]: ...


class ImmediateFuture(Generic[T]):
    """Synchronous Future used for deterministic tests and local demos."""

    def __init__(self, value: T | None = None, exception: BaseException | None = None) -> None:
        self._value = value
        self._exception = exception
        self._cancelled = False

    def result(self, timeout: float | None = None) -> T:
        if self._exception:
            raise self._exception
        return self._value  # type: ignore[return-value]

    def cancel(self) -> bool:
        self._cancelled = True
        return self._cancelled

    def done(self) -> bool:
        return True


class SequentialExecutor:
    """Executor that runs work immediately while preserving the Future contract."""

    def submit(self, fn: Callable[..., T], *args, **kwargs) -> FutureLike[T]:
        try:
            return ImmediateFuture(fn(*args, **kwargs))
        except BaseException as exc:  # pragma: no cover - defensive path
            return ImmediateFuture(exception=exc)


class ThreadedExecutor:
    """Thread-based executor used to prove parallel task execution.

    It intentionally wraps the standard ThreadPoolExecutor so the project does
    not need external dependencies. The adapter can be closed explicitly or used
    as a context manager.
    """

    def __init__(self, max_workers: int = 4) -> None:
        self._pool = ThreadPoolExecutor(max_workers=max_workers)

    def submit(self, fn: Callable[..., T], *args, **kwargs) -> ConcurrentFuture[T]:
        return self._pool.submit(fn, *args, **kwargs)

    def shutdown(self, wait: bool = True) -> None:
        self._pool.shutdown(wait=wait)

    def __enter__(self) -> "ThreadedExecutor":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.shutdown(wait=True)
