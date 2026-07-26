from database.db import db


class Zone(db.Model):

    __tablename__ = "zones"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    floor = db.Column(
        db.Integer,
        nullable=False
    )

    building_id = db.Column(
        db.Integer,
        db.ForeignKey("buildings.id"),
        nullable=False
    )

    building = db.relationship(
        "Building",
        back_populates="zones"
    )

    sensors = db.relationship(
        "Sensor",
        back_populates="zone",
        cascade="all, delete-orphan"
    )

    occupancy_records = db.relationship(
        "Occupancy",
        back_populates="zone",
        cascade="all, delete-orphan"
    )