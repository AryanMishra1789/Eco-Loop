from database.models import (
    Building,
    Zone,
    Sensor,
    SensorReading
)


class DatabaseTool:
    """
    Database Tool

    Provides building metadata to the agent.
    """

    def get_buildings(self):

        buildings = Building.query.all()

        return [
            {
                "id": b.id,
                "name": b.name,
                "location": b.location
            }
            for b in buildings
        ]

    # ---------------------------------------------------------

    def get_building(self, building_name):

        building = Building.query.filter_by(
            name=building_name
        ).first()

        if building is None:

            raise ValueError(
                f"Building '{building_name}' not found."
            )

        return {
            "id": building.id,
            "name": building.name,
            "location": building.location
        }

    # ---------------------------------------------------------

    def get_zones(
        self,
        building_name
    ):

        building = Building.query.filter_by(
            name=building_name
        ).first()

        if building is None:

            return []

        return [

            {
                "id": zone.id,
                "name": zone.name
            }

            for zone in building.zones

        ]

    # ---------------------------------------------------------

    def latest_sensor_values(
        self,
        building_name
    ):

        building = Building.query.filter_by(
            name=building_name
        ).first()

        if building is None:

            return []

        values = []

        for zone in building.zones:

            for sensor in zone.sensors:

                reading = (

                    SensorReading.query

                    .filter_by(sensor_id=sensor.id)

                    .order_by(
                        SensorReading.timestamp.desc()
                    )

                    .first()

                )

                if reading:

                    values.append({

                        "sensor": sensor.name,

                        "zone": zone.name,

                        "value": reading.value,

                        "timestamp": str(
                            reading.timestamp
                        )

                    })

        return values