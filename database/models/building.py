from database.db import db


class Building(db.Model):

    __tablename__ = "buildings"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    location = db.Column(
        db.String(150),
        nullable=False
    )

    status = db.Column(
        db.String(30),
        default="Active"
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    # ----------------------------
    # Relationships
    # ----------------------------

    zones = db.relationship(
        "Zone",
        back_populates="building",
        cascade="all, delete-orphan"
    )

    runs = db.relationship(
        "Run",
        backref="building",
        cascade="all, delete-orphan",
        lazy=True
    )