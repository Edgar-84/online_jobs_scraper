import time
import functools

from src.config.logger_config import logger


def working_time(active: bool = True):
    """
    Get the runtime of the decorated function
    """
    def actual_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if active:
                start_time = time.time()
                func_result = func(*args, **kwargs)
                end_time = time.time()
                message_info = f'Finished {func.__name__!r} after time: {round(end_time - start_time, 5)} seconds'
                logger.debug(message_info)
                if func.__name__ == 'main':
                    print(message_info)

                return func_result

            else:
                return func(*args, **kwargs)

        return wrapper
    return actual_decorator
