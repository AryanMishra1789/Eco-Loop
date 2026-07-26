from database.db import db


class SensorReading(db.Model):

    __tablename__ = "sensor_readings"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    sensor_id = db.Column(
        db.Integer,
        db.ForeignKey("sensors.id"),
        nullable=False
    )

    run_id = db.Column(
        db.Integer,
        db.ForeignKey("runs.id"),
        nullable=False
    )

    value = db.Column(
        db.Float,
        nullable=False
    )

    timestamp = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    sensor = db.relationship(
        "Sensor",
        back_populates="readings"
    )

    run = db.relationship(
        "Run",
        back_populates="sensor_readings"
    )