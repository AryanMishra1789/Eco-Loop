from datetime import datetime

from database import db


class ServiceRegistry(db.Model):

    __tablename__ = "service_registry"

    id = db.Column(db.Integer, primary_key=True)

    service_name = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    category = db.Column(
        db.String(100),
        nullable=False
    )

    execution_type = db.Column(
        db.String(30),
        nullable=False,
        default="python"
    )

    module_path = db.Column(db.String(255))

    class_name = db.Column(db.String(100))

    method_name = db.Column(db.String(100))

    endpoint = db.Column(db.String(500))

    http_method = db.Column(
        db.String(20),
        default="POST"
    )

    description = db.Column(db.Text)

    timeout_seconds = db.Column(
        db.Integer,
        default=30
    )

    retry_count = db.Column(
        db.Integer,
        default=0
    )

    version = db.Column(
        db.String(20),
        default="1.0"
    )

    enabled = db.Column(
        db.Boolean,
        default=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def __repr__(self):

        return (
            f"<ServiceRegistry "
            f"{self.service_name}>"
        )