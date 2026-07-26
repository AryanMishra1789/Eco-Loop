from Generic_API_Caller.api_config import APIConfig
from Generic_API_Caller.registry import registry
from Generic_API_Caller.executor import Executor


class Dispatcher:
    """
    Central communication bus.

    Receives requests and dispatches them
    to the appropriate registered service.
    """

    def __init__(self):

        self.config = APIConfig()

        self.registry = registry

        self.executor = Executor()

    def register_service(
        self,
        service_name: str,
        handler
    ):

        if self.config.get(service_name) is None:
            raise ValueError(
                f"'{service_name}' is not defined in APIConfig."
            )

        self.registry.register(
            service_name,
            handler
        )

    def dispatch(
        self,
        service_name: str,
        *args,
        **kwargs
    ):

        service = self.config.get(service_name)

        if service is None:

            return {
                "success": False,
                "service": service_name,
                "result": None,
                "error": "Unknown service."
            }

        if not service.enabled:

            return {
                "success": False,
                "service": service_name,
                "result": None,
                "error": "Service is disabled."
            }

        try:

            handler = self.registry.get(
                service_name
            )

        except ValueError as error:

            return {
                "success": False,
                "service": service_name,
                "result": None,
                "error": str(error)
            }

        return self.executor.execute(
            service_name,
            handler,
            *args,
            **kwargs
        )

    def available_services(self):

        return [
            service.name
            for service in self.config.list_services()
        ]