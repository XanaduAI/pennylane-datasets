from collections.abc import Callable
from contextlib import AbstractContextManager

import rich.progress


class IOProgressBarManager(AbstractContextManager):
    """Context manager for I/O progress bars using rich.

    See:
    https://rich.readthedocs.io/en/stable/progress.html
    """

    def __enter__(self) -> "IOProgressBarManager":
        self.progress = rich.progress.Progress(
            rich.progress.TextColumn("[progress.description]{task.description}"),
            rich.progress.BarColumn(),
            rich.progress.FileSizeColumn(),
            rich.progress.TransferSpeedColumn(),
            rich.progress.TimeElapsedColumn(),
            auto_refresh=False,
        )

        self.progress.__enter__()

        return self

    def __exit__(
        self,
        __exc_type,
        __exc_value,
        __traceback,
    ) -> None:
        self.progress.__exit__(None, None, None)

    def add_bar(self, total_bytes: int, description: str) -> Callable[[int], None]:
        """Add a progress bar to the context. Returns a callable to update
        progress bar with the number of bytes processed since the last
        call.

        Args:
            total_bytes: Total size of the file to be processed
            description: Description for the operation

        Returns:
            Callback function to update new progress bar.
        """
        task = self.progress.add_task(description, total=total_bytes)

        def advance_cb(chunk: int) -> None:
            """Callback function. ``chunk`` is the number
            of bytes processed since the last call."""
            self.progress.update(task, advance=chunk)
            self.progress.refresh()

        return advance_cb
