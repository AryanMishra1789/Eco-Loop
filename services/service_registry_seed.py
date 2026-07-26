from database import db
from database.models.service_registry import ServiceRegistry


class ServiceRegistrySeeder:

    @staticmethod
    def seed():

        services = [

            {
                "service_name": "energyplus.simulate",
                "category": "EnergyPlus",
                "module_path": "EnergyPlus.controller",
                "class_name": "EnergyPlusController",
                "method_name": "simulate",
                "description": "Run EnergyPlus simulation"
            },

            {
                "service_name": "database.save_run",
                "category": "Database",
                "module_path": "services.run_service",
                "class_name": "RunService",
                "method_name": "save_run",
                "description": "Persist simulation results"
            },

            {
                "service_name": "ai.analyze",
                "category": "AI",
                "module_path": "AI.agent",
                "class_name": "EcoLoopAgent",
                "method_name": "analyze_building",
                "description": "Generate AI recommendations"
            }

        ]

        for service in services:

            exists = ServiceRegistry.query.filter_by(
                service_name=service["service_name"]
            ).first()

            if exists:
                continue

            db.session.add(
                ServiceRegistry(**service)
            )

        db.session.commit()