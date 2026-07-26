from database.db import db


class Occupancy(db.Model):

    __tablename__ = "occupancy"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    zone_id = db.Column(
        db.Integer,
        db.ForeignKey("zones.id"),
        nullable=False
    )

    run_id = db.Column(
        db.Integer,
        db.ForeignKey("runs.id"),
        nullable=False
    )

    people_count = db.Column(
        db.Integer,
        nullable=False
    )

    timestamp = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    zone = db.relationship(
        "Zone",
        back_populates="occupancy_records"
    )

    run = db.relationship(
        "Run",
        back_populates="occupancy_records"
    )