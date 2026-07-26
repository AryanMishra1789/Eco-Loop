import importlib

from database import db
from database.models.service_registry import ServiceRegistry


class ServiceRegistryLoader:

    def __init__(self, dispatcher):
        self.dispatcher = dispatcher

    def load_services(self):

        services = (
            db.session.query(ServiceRegistry)
            .filter_by(enabled=True)
            .all()
        )

        for service in services:

            if service.execution_type == "python":

                module = importlib.import_module(
                    service.module_path
                )

                cls = getattr(
                    module,
                    service.class_name
                )

                instance = cls()

                handler = getattr(
                    instance,
                    service.method_name
                )

                self.dispatcher.register_service(
                    service.service_name,
                    handler
                )

            else:
                print(
                    f"Skipping unsupported execution type: "
                    f"{service.execution_type}"
                )