from contextlib import ContextDecorator
from time import perf_counter
from typing import Self


class Timer(ContextDecorator):
    def __init__(
        self,
        source_name: str,
        log_params: dict | None = None,
    ):
        """
        A context manager for measuring time and logging to logz.io

        # Usage as context manager:
        with timer(SOURCE_NAME):
            pass

        :param source_name: The identifier of the event, will be shown in the log.
        :param log_params: A dictionary of extra data to pass to the logger.
        """
        self.source_name = source_name
        self.log_params = log_params

    def __enter__(self) -> Self:
        self.start_time = perf_counter()
        return self

    def __exit__(self, *exc: Self) -> None:
        self.end_time = perf_counter()
        run_time = self.end_time - self.start_time
        self.log_run_time(run_time)

    def log_run_time(self, run_time: float) -> None:
        run_time = round(run_time, 3)
        msg = f"{self.source_name} took: {run_time} seconds"
        if self.log_params:
            msg += f" with parameters: {self.log_params}"
        print(msg)
