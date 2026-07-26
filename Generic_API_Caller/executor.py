import time
from typing import Any, Callable


class Executor:
    """
    Executes registered services and returns
    a standardized response.
    """

    def execute(self, service_name: str, handler: Callable, *args, **kwargs) -> dict:
        """
        Execute a registered service.

        Parameters
        ----------
        service_name : str
            Name of the registered service.
        handler : Callable
            Function to execute.

        Returns
        -------
        dict
            Standardized execution response.
        """

        start_time = time.perf_counter()

        try:
            result = handler(*args, **kwargs)

            execution_time = round(
                (time.perf_counter() - start_time) * 1000,
                2
            )

            return {
                "success": True,
                "service": service_name,
                "result": result,
                "execution_time_ms": execution_time,
                "error": None
            }

        except Exception as error:

            execution_time = round(
                (time.perf_counter() - start_time) * 1000,
                2
            )

            return {
                "success": False,
                "service": service_name,
                "result": None,
                "execution_time_ms": execution_time,
                "error": str(error)
            }