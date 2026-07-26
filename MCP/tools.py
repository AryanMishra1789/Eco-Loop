from EnergyPlus.controller import EnergyPlusController
from AI.recommendation_engine import RecommendationEngine


class MCPTools:
    """
    MCP Tool Implementations.

    These methods are exposed to the AI Agent
    through the MCP Server.
    """

    def __init__(self):

        self.energy_controller = EnergyPlusController()

        self.recommendation_engine = RecommendationEngine()

    # ---------------------------------------------------------

    def simulate_building(
        self,
        building_name,
        weather_file=None,
        idf_file=None
    ):
        """
        Run a building simulation.
        """

        simulation = self.energy_controller.simulate(
            building_name=building_name,
            weather_file=weather_file,
            idf_file=idf_file
        )

        return simulation

    # ---------------------------------------------------------

    def optimize_building(
        self,
        building_name,
        weather_file=None,
        idf_file=None
    ):
        """
        Run a simulation and generate optimization
        recommendations.
        """

        simulation = self.energy_controller.simulate(
            building_name=building_name,
            weather_file=weather_file,
            idf_file=idf_file
        )

        recommendations = self.recommendation_engine.generate(
            simulation
        )

        summary = self.recommendation_engine.summarize(
            recommendations
        )

        return {

            "building": building_name,

            "simulation": simulation,

            "recommendations": recommendations,

            "summary": summary

        }

    # ---------------------------------------------------------

    def health_check(self):
        """
        Return MCP server health status.
        """

        return {

            "status": "healthy",

            "service": "EcoLoop MCP Server"

        }