from Generic_API_Caller.dispatcher import Dispatcher
from services.service_registry_loader import ServiceRegistryLoader

dispatcher = Dispatcher()


def initialize():

    loader = ServiceRegistryLoader(dispatcher)

    loader.load_services()

    return dispatcher