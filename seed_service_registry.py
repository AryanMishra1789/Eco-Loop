from app import app
from database import db
from database.models.service_registry import ServiceRegistry


SERVICES = [
    {
        "service_name": "energyplus.simulate",
        "category": "EnergyPlus",
        "execution_type": "python",
        "module_path": "EnergyPlus.controller",
        "class_name": "EnergyPlusController",
        "method_name": "simulate",
        "description": "Run EnergyPlus Simulation"
    },
    {
        "service_name": "database.save_run",
        "category": "Database",
        "execution_type": "python",
        "module_path": "services.run_service",
        "class_name": "RunService",
        "method_name": "save_run",
        "description": "Save Simulation Run"
    },
    {
        "service_name": "ai.analyze",
        "category": "AI",
        "execution_type": "python",
        "module_path": "AI.agent",
        "class_name": "EcoLoopAgent",
        "method_name": "analyze_building",
        "description": "Generate AI Recommendations"
    }
]


with app.app_context():

    for service in SERVICES:

        exists = ServiceRegistry.query.filter_by(
            service_name=service["service_name"]
        ).first()

        if not exists:
            db.session.add(
                ServiceRegistry(**service)
            )

    db.session.commit()

print("Service Registry seeded successfully.")