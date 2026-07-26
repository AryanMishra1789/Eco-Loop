from flask import Blueprint, jsonify, request

from AI.agent import EcoLoopAgent

agent_bp = Blueprint(
    "agent",
    __name__,
    url_prefix="/api/agent"
)

agent = EcoLoopAgent()


# ---------------------------------------------------------
# Chat
# ---------------------------------------------------------

@agent_bp.route(
    "/chat",
    methods=["POST"]
)
def chat():

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "error": "JSON body required."
            }), 400

        message = data.get("message")

        if not message:
            return jsonify({
                "success": False,
                "error": "message field is required."
            }), 400

        response = agent.run(message)

        return jsonify(response)

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ---------------------------------------------------------
# Available Tools
# ---------------------------------------------------------

@agent_bp.route(
    "/tools",
    methods=["GET"]
)
def tools():

    try:

        return jsonify({

            "success": True,

            "tools": agent.available_tools()

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500


# ---------------------------------------------------------
# Health
# ---------------------------------------------------------

@agent_bp.route(
    "/health",
    methods=["GET"]
)
def health():

    return jsonify({

        "success": True,

        "agent": "EcoLoop AI Agent",

        "status": "Running",

        "architecture": "Metadata Driven",

        "dispatcher": "Enabled"

    })