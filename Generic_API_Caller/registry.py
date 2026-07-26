from typing import Callable, Dict


class Registry:
    """
    Registry for all callable services/tools.
    """

    def __init__(self):
        self._services: Dict[str, Callable] = {}

    def register(self, name: str, handler: Callable):

        if not callable(handler):
            raise TypeError(f"{name} is not callable.")

        self._services[name] = handler

    def unregister(self, name: str):

        self._services.pop(name, None)

    def get(self, name: str):

        if name not in self._services:
            raise ValueError(
                f"Service '{name}' is not registered."
            )

        return self._services[name]

    def exists(self, name: str):

        return name in self._services

    def list_services(self):

        return list(self._services.keys())


# ---------------------------------------------------------
# Shared global registry
# ---------------------------------------------------------

registry = Registry()