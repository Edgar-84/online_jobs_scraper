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
                logger.debug(f'Finished {func.__name__!r} after time: {round(end_time - start_time, 5)} seconds')

                if func.__name__ == 'main':
                    time_search = end_time - start_time
                    if time_search > 60:
                        message = f'Finished work after: {round((time_search / 60), 2)} minutes'
                    else:
                        message = f'Finished work after: {round(time_search, 2)} seconds'
                    print(message)

                return func_result

            else:
                return func(*args, **kwargs)

        return wrapper
    return actual_decorator
