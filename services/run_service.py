from database.db import db

from database.models.run import Run
from database.models.building import Building
from database.models.zone import Zone
from database.models.sensor import Sensor
from database.models.sensor_reading import SensorReading
from database.models.occupancy import Occupancy


class RunService:

    SENSOR_MAPPING = {
        "energy_consumption": ("Energy Consumption", "ENERGY", "J"),
        "indoor_temperature": ("Indoor Temperature", "TEMPERATURE", "°C"),
        "hvac_load": ("HVAC Load", "HVAC_LOAD", "J"),
        "lighting_load": ("Lighting Load", "LIGHTING_LOAD", "J"),
        "cooling_load": ("Cooling Load", "COOLING_LOAD", "J"),
        "heating_load": ("Heating Load", "HEATING_LOAD", "J"),
        "co2_emissions": ("CO₂ Emissions", "CO2", "kg"),
    }

    @staticmethod
    def save_run(parsed_data):

        building = Building.query.filter_by(
            name=parsed_data["building_name"]
        ).first()

        if building is None:

            building = Building(
                name=parsed_data["building_name"],
                location="Unknown"
            )

            db.session.add(building)
            db.session.flush()

        zone = Zone.query.filter_by(
            building_id=building.id,
            name="Whole Building"
        ).first()

        if zone is None:

            zone = Zone(
                name="Whole Building",
                floor=0,
                building_id=building.id
            )

            db.session.add(zone)
            db.session.flush()

        run = Run(
            building_id=building.id,
            run_name="EnergyPlus Simulation",
            source="ENERGYPLUS",
            execution_time=parsed_data.get("simulation_time"),
            metadata_json={
                "run_directory": parsed_data.get("run_directory")
            }
        )

        db.session.add(run)
        db.session.flush()

        for metric, config in RunService.SENSOR_MAPPING.items():

            if metric not in parsed_data:
                continue

            sensor_name, sensor_type, unit = config

            sensor = Sensor.query.filter_by(
                zone_id=zone.id,
                sensor_name=sensor_name
            ).first()

            if sensor is None:

                sensor = Sensor(
                    sensor_name=sensor_name,
                    sensor_type=sensor_type,
                    unit=unit,
                    zone_id=zone.id
                )

                db.session.add(sensor)
                db.session.flush()

            reading = SensorReading(
                sensor_id=sensor.id,
                run_id=run.id,
                value=float(parsed_data[metric])
            )

            db.session.add(reading)

        occupancy = Occupancy(
            zone_id=zone.id,
            run_id=run.id,
            people_count=parsed_data.get("occupancy", 0)
        )

        db.session.add(occupancy)

        db.session.commit()

        return run