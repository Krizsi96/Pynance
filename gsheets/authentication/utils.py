from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError


def run_with_timeout(func, timeout, *args, **kwargs):
    executor = ThreadPoolExecutor(max_workers=1)
    future = executor.submit(func, *args, **kwargs)
    try:
        return future.result(timeout=timeout)
    except FutureTimeoutError:
        print(f"TimeoutError for func: {func.__name__}, timeout: {timeout}")
        return None
    finally:
        executor.shutdown(wait=False)
