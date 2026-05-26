import asyncio
import threading
import weakref

_limiters_by_loop: weakref.WeakKeyDictionary[asyncio.AbstractEventLoop, dict[str, asyncio.Semaphore]] = weakref.WeakKeyDictionary()
_limiters_lock = threading.Lock()


def get_loop_semaphore(name: str, limit: int) -> asyncio.Semaphore:
    """Return a semaphore scoped to the current event loop.

    Celery runs each async book job through ``asyncio.run()``, which creates a
    fresh event loop per task. A module-level asyncio.Semaphore can become bound
    to the first loop and fail on later tasks, so limiters must be loop-local.
    """
    loop = asyncio.get_running_loop()
    with _limiters_lock:
        loop_limiters = _limiters_by_loop.setdefault(loop, {})
        semaphore = loop_limiters.get(name)
        if semaphore is None:
            semaphore = asyncio.Semaphore(max(1, limit))
            loop_limiters[name] = semaphore
        return semaphore
