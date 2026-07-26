from database.db import db


class Sensor(db.Model):

    __tablename__ = "sensors"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    sensor_name = db.Column(
        db.String(100),
        nullable=False
    )

    sensor_type = db.Column(
        db.String(50),
        nullable=False
    )

    unit = db.Column(
        db.String(30),
        nullable=False
    )

    zone_id = db.Column(
        db.Integer,
        db.ForeignKey("zones.id"),
        nullable=False
    )

    zone = db.relationship(
        "Zone",
        back_populates="sensors"
    )

    readings = db.relationship(
        "SensorReading",
        back_populates="sensor",
        cascade="all, delete-orphan"
    )