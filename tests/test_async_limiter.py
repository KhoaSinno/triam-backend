import asyncio

from app.services.async_limiter import get_loop_semaphore


async def _semaphore_for_current_loop():
    semaphore = get_loop_semaphore("test", 1)
    async with semaphore:
        return id(asyncio.get_running_loop()), id(semaphore)


def _run_on_new_loop():
    loop = asyncio.new_event_loop()
    try:
        return loop, loop.run_until_complete(_semaphore_for_current_loop())
    finally:
        loop.close()


def test_loop_semaphore_is_scoped_to_each_event_loop():
    first_loop, (first_loop_id, first_semaphore_id) = _run_on_new_loop()
    second_loop, (second_loop_id, second_semaphore_id) = _run_on_new_loop()

    assert first_loop is not second_loop
    assert first_loop_id != second_loop_id
    assert first_semaphore_id != second_semaphore_id
