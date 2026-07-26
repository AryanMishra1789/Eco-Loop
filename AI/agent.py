from AI.llm import OllamaLLM
from AI.prompts import (build_analysis_prompt, build_agent_prompt, build_response_prompt)
from AI.recommendation_engine import RecommendationEngine
from AI.runtime import EcoLoopRuntime
from database.models.service_registry import ServiceRegistry


class EcoLoopAgent:

    def __init__(self):

        self.llm = OllamaLLM()

        self.runtime = EcoLoopRuntime()

        self.recommendation_engine = RecommendationEngine()

        self._history = []

    # ---------------------------------------------------------
    # Building Analysis
    # ---------------------------------------------------------

    def analyze_building(self, metrics):

        recommendations = self.recommendation_engine.generate(
            metrics
        )

        prompt = build_analysis_prompt(
            metrics,
            recommendations
        )

        analysis = self.llm.generate(prompt)

        return {
            "metrics": metrics,
            "recommendations": recommendations,
            "analysis": analysis
        }

    # ---------------------------------------------------------
    # Main Agent
    # ---------------------------------------------------------

    def run(self, user_request):

        services = ServiceRegistry.query.filter_by(
            enabled=True
        ).all()

        workflows = []

        for service in services:

            workflows.append({

                "service_name": service.service_name,

                "category": service.category,

                "description": service.description

            })

        planner_prompt = build_agent_prompt(
            user_request,
            workflows
        )

        decision = self.llm.generate_json(
            planner_prompt
        )

        if not decision.get("intent"):

            return {

                "success": False,

                "error": "Unable to determine user intent.",

                "llm_response": decision

            }

        intent = decision["intent"]

        building_name = decision.get(
            "building_name",
            "Honeywell Office"
        )

        parameters = decision.get(
            "parameters",
            {}
        )

        # -----------------------------------------------------
        # Runtime Execution
        # -----------------------------------------------------

        execution_args = {

            "building_name": building_name,

            **parameters

        }

        result = self.runtime.execute(

            intent=intent,

            **execution_args

        )

        if not result.get("success", False):

            return {

                "success": False,

                "intent": intent,

                "error": result.get(
                    "error",
                    "Workflow execution failed."
                )

            }

        # -----------------------------------------------------
        # Store Execution History
        # -----------------------------------------------------

        self._history.append({

            "intent": intent,

            "request": user_request,

            "result": result

        })

        # -----------------------------------------------------
        # Generate Final Response
        # -----------------------------------------------------

        response_prompt = build_response_prompt(

            user_request,

            result

        )

        final_response = self.llm.generate(
            response_prompt
        )

        return {

            "success": True,

            "intent": intent,

            "workflow": intent,

            "tool_result": result,

            "response": final_response

        }

    # ---------------------------------------------------------
    # Available Workflows
    # ---------------------------------------------------------

    def available_tools(self):

        services = ServiceRegistry.query.filter_by(
            enabled=True
        ).all()

        return [

            {

                "workflow": service.service_name,

                "category": service.category,

                "description": service.description

            }

            for service in services

        ]

    # ---------------------------------------------------------
    # Execution History
    # ---------------------------------------------------------

    def execution_history(self):

        return self._history

    # ---------------------------------------------------------
    # Memory
    # ---------------------------------------------------------

    def get_memory(self):

        return {

            "history_count": len(self._history),

            "last_execution": self._history[-1] if self._history else None

        }

    # ---------------------------------------------------------
    # Health
    # ---------------------------------------------------------

    def health(self):

        return {

            "success": True,

            "agent": "EcoLoop AI",

            "status": "Running",

            "registered_workflows": len(
                self.available_tools()
            )

        }