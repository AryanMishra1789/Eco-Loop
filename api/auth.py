from flask import Blueprint, request, jsonify, session
from werkzeug.security import check_password_hash

from database.models import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:

        return jsonify({

            "message": "Email and password are required."

        }), 400

    user = User.query.filter_by(email=email).first()

    if user is None:

        return jsonify({

            "message": "Invalid email or password."

        }), 401

    if not check_password_hash(user.password_hash, password):

        return jsonify({

            "message": "Invalid email or password."

        }), 401

    session["user_id"] = user.id

    return jsonify({

        "success": True,

        "user": {

            "id": user.id,

            "name": user.name,

            "email": user.email

        }

    })


@auth_bp.route("/logout", methods=["POST"])
def logout():

    session.clear()

    return jsonify({

        "success": True

    })


@auth_bp.route("/me")
def me():

    user_id = session.get("user_id")

    if not user_id:

        return jsonify({

            "authenticated": False

        }), 401

    user = User.query.get(user_id)

    if user is None:

        return jsonify({

            "authenticated": False

        }), 401

    return jsonify({

        "authenticated": True,

        "user": {

            "id": user.id,

            "name": user.name,

            "email": user.email

        }

    })