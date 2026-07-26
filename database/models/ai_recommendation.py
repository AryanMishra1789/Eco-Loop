from database.db import db


class AIRecommendation(db.Model):

    __tablename__ = "ai_recommendations"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    run_id = db.Column(
        db.Integer,
        db.ForeignKey("runs.id"),
        nullable=False
    )

    recommendation = db.Column(
        db.Text,
        nullable=False
    )

    priority = db.Column(
        db.String(20),
        default="Medium"
    )

    status = db.Column(
        db.String(20),
        default="Pending"
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    run = db.relationship(
        "Run",
        back_populates="recommendations"
    )