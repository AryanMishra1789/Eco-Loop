from dataclasses import dataclass
from typing import Dict


@dataclass
class ServiceConfig:
    """
    Metadata describing a callable service.
    """

    name: str

    category: str

    description: str

    enabled: bool = True


class APIConfig:
    """
    Registry of all callable platform services.
    """

    def __init__(self):

        self.services: Dict[str, ServiceConfig] = {}

        self._load_default_services()

    # ---------------------------------------------------------

    def _load_default_services(self):

        services = [

            # -------------------------
            # EnergyPlus
            # -------------------------

            ServiceConfig(
                name="energyplus.simulate",
                category="EnergyPlus",
                description="Run an EnergyPlus simulation."
            ),

            ServiceConfig(
                name="energyplus.compare",
                category="EnergyPlus",
                description="Compare two simulation results."
            ),

            ServiceConfig(
                name="energyplus.status",
                category="EnergyPlus",
                description="Return simulator status."
            ),

            ServiceConfig(
                name="energyplus.workspace",
                category="EnergyPlus",
                description="Return workspace information."
            ),

            # -------------------------
            # AI
            # -------------------------

            ServiceConfig(
                name="ai.analyze",
                category="AI",
                description="Generate AI recommendations."
            ),

            # -------------------------
            # Database
            # -------------------------

            ServiceConfig(
                name="database.save_run",
                category="Database",
                description="Persist a simulation run."
            ),

            # -------------------------
            # MCP
            # -------------------------

            ServiceConfig(
                name="mcp.execute",
                category="MCP",
                description="Execute an MCP tool."
            )
        ]

        for service in services:

            self.register(service)

    # ---------------------------------------------------------

    def register(
        self,
        service: ServiceConfig
    ):

        self.services[service.name] = service

    # ---------------------------------------------------------

    def get(
        self,
        service_name: str
    ):

        return self.services.get(service_name)

    # ---------------------------------------------------------

    def list_services(self):

        return list(self.services.values())