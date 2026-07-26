from flask import Flask, render_template, jsonify
from flask_migrate import Migrate
from sqlalchemy import inspect

from api.agent_routes import agent_bp
from bootstrap import initialize
from config import Config
from database import db


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    # =====================================================
    # Database
    # =====================================================

    db.init_app(app)

    Migrate(app, db)

    # =====================================================
    # API Blueprints
    # =====================================================

    app.register_blueprint(agent_bp)

    # =====================================================
    # Initialize Dynamic Services
    # =====================================================

    with app.app_context():

        try:

            inspector = inspect(db.engine)

            if inspector.has_table("service_registry"):
                initialize()
            else:
                print("service_registry table not found. Skipping initialization.")

        except Exception as e:

            print(f"Service initialization skipped: {e}")

    # =====================================================
    # Frontend Pages
    # =====================================================

    @app.route("/")
    def home():
        return render_template("login.html")

    @app.route("/dashboard")
    def dashboard():
        return render_template("dashboard.html")

    @app.route("/simulation")
    def simulation():
        return render_template("simulation.html")

    @app.route("/assistant")
    def assistant():
        return render_template("assistant.html")

    @app.route("/history")
    def history():
        return render_template("history.html")

    @app.route("/reports")
    def reports():
        return render_template("reports.html")

    @app.route("/settings")
    def settings():
        return render_template("settings.html")

    # =====================================================
    # Global Error Handlers
    # =====================================================

    @app.errorhandler(404)
    def page_not_found(error):
        return jsonify({
            "success": False,
            "error": "Endpoint not found."
        }), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": "Internal server error."
        }), 500

    return app


app = create_app()


if __name__ == "__main__":

    print("\n" + "=" * 80)
    print("REGISTERED ROUTES")
    print("=" * 80)

    for rule in sorted(app.url_map.iter_rules(), key=lambda x: str(x)):
        methods = ", ".join(sorted(rule.methods - {"HEAD", "OPTIONS"}))
        print(f"{methods:<20} {rule}")

    print("=" * 80)

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )