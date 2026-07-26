from database.db import db


class SensorCatalog(db.Model):
    """
    Master catalog of supported sensor definitions.
    """

    __tablename__ = "sensor_catalog"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    metric_key = db.Column(
        db.String(100),
        unique=True,
        nullable=False
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

    description = db.Column(
        db.Text
    )