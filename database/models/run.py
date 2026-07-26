from database.db import db


class Run(db.Model):
    """
    Generic execution/data collection run.

    Examples:
    - EnergyPlus simulation
    - Live IoT snapshot
    - AI optimization
    - Digital Twin replay
    """

    __tablename__ = "runs"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    building_id = db.Column(
        db.Integer,
        db.ForeignKey("buildings.id"),
        nullable=False
    )

    run_name = db.Column(
        db.String(150),
        nullable=False
    )

    source = db.Column(
        db.String(50),
        nullable=False
    )

    status = db.Column(
        db.String(30),
        default="Completed"
    )

    execution_time = db.Column(
        db.Float
    )

    metadata_json = db.Column(
        db.JSON
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    sensor_readings = db.relationship(
        "SensorReading",
        back_populates="run",
        cascade="all, delete-orphan"
    )

    occupancy_records = db.relationship(
        "Occupancy",
        back_populates="run",
        cascade="all, delete-orphan"
    )

    recommendations = db.relationship(
    "AIRecommendation",
    back_populates="run",
    cascade="all, delete-orphan"
    )