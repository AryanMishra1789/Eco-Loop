from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


# ==========================================================
# User
# ==========================================================

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password_hash = db.Column(db.String(255), nullable=False)

    role = db.Column(db.String(50), default="user")

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    last_login = db.Column(
        db.DateTime
    )

    def set_password(self, password):

        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):

        return check_password_hash(
            self.password_hash,
            password
        )

    def to_dict(self):

        return {

            "id": self.id,

            "name": self.name,

            "email": self.email,

            "role": self.role,

            "created_at": self.created_at.isoformat()

        }


# ==========================================================
# Simulation
# ==========================================================

class Simulation(db.Model):

    __tablename__ = "simulations"

    id = db.Column(db.Integer, primary_key=True)

    simulation_name = db.Column(
        db.String(150),
        nullable=False
    )

    building_name = db.Column(
        db.String(150)
    )

    weather_file = db.Column(
        db.String(255)
    )

    status = db.Column(
        db.String(30),
        default="Completed"
    )

    total_energy = db.Column(
        db.Float,
        default=0
    )

    estimated_cost = db.Column(
        db.Float,
        default=0
    )

    co2_emission = db.Column(
        db.Float,
        default=0
    )

    energy_savings = db.Column(
        db.Float,
        default=0
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    analysis = db.Column(
        db.Text
    )

    recommendations = db.Column(
        db.Text
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )

    def to_dict(self):

        return {

            "id": self.id,

            "simulation_name": self.simulation_name,

            "building_name": self.building_name,

            "weather_file": self.weather_file,

            "status": self.status,

            "total_energy": self.total_energy,

            "estimated_cost": self.estimated_cost,

            "co2_emission": self.co2_emission,

            "energy_savings": self.energy_savings,

            "analysis": self.analysis,

            "recommendations": self.recommendations,

            "created_at": self.created_at.isoformat()

        }


# ==========================================================
# AI Chat History
# ==========================================================

class ChatHistory(db.Model):

    __tablename__ = "chat_history"

    id = db.Column(db.Integer, primary_key=True)

    user_message = db.Column(
        db.Text,
        nullable=False
    )

    assistant_response = db.Column(
        db.Text,
        nullable=False
    )

    model = db.Column(
        db.String(80)
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )

    def to_dict(self):

        return {

            "id": self.id,

            "user_message": self.user_message,

            "assistant_response": self.assistant_response,

            "model": self.model,

            "created_at": self.created_at.isoformat()

        }


# ==========================================================
# Reports
# ==========================================================

class Report(db.Model):

    __tablename__ = "reports"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    simulation_id = db.Column(
        db.Integer,
        db.ForeignKey("simulations.id")
    )

    report_name = db.Column(
        db.String(150)
    )

    summary = db.Column(
        db.Text
    )

    report_json = db.Column(
        db.JSON
    )

    generated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def to_dict(self):

        return {

            "id": self.id,

            "simulation_id": self.simulation_id,

            "report_name": self.report_name,

            "summary": self.summary,

            "report_json": self.report_json,

            "generated_at": self.generated_at.isoformat()

        }


# ==========================================================
# Application Settings
# ==========================================================

class AppSettings(db.Model):

    __tablename__ = "app_settings"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    organization = db.Column(
        db.String(100),
        default="Honeywell"
    )

    default_building = db.Column(
        db.String(150),
        default="Main Building"
    )

    timezone = db.Column(
        db.String(50),
        default="Asia/Kolkata"
    )

    theme = db.Column(
        db.String(20),
        default="Light"
    )

    llm_model = db.Column(
        db.String(80),
        default="phi3:mini"
    )

    temperature = db.Column(
        db.Float,
        default=0.2
    )

    timeout = db.Column(
        db.Integer,
        default=180
    )

    weather_directory = db.Column(
        db.String(255)
    )

    output_directory = db.Column(
        db.String(255)
    )

    parallel_runs = db.Column(
        db.Integer,
        default=2
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def to_dict(self):

        return {

            "organization": self.organization,

            "default_building": self.default_building,

            "timezone": self.timezone,

            "theme": self.theme,

            "llm_model": self.llm_model,

            "temperature": self.temperature,

            "timeout": self.timeout,

            "weather_directory": self.weather_directory,

            "output_directory": self.output_directory,

            "parallel_runs": self.parallel_runs

        }