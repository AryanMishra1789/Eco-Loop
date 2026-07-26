from AI.llm import LLMClient
from EnergyPlus.controller import EnergyPlusController


class EnergyOptimizer:
    """
    Coordinates the complete optimization workflow.
    Workflow:
        1. Run EnergyPlus simulation.
        2. Analyze simulation output.
        3. Generate AI recommendations.
    """

    def __init__(self):
        self.controller = EnergyPlusController()
        self.llm = LLMClient()

    def optimize(
        self,
        building_name: str,
        weather_file: str = None,
        idf_file: str = None,
    ):
        """
        Run a complete optimization cycle.
        """

        simulation_result = self.controller.simulate(
            building_name=building_name,
            weather_file=weather_file,
            idf_file=idf_file,
        )

        recommendation = self.llm.generate(
            simulation_result
        )

        return {
            "building": simulation_result["building"],
            "simulation": simulation_result,
            "recommendation": recommendation,
            "status": "Optimization Completed"
        }

    def optimize_multiple(
        self,
        building_name: str,
        runs: int = 5,
    ):
        """
        Execute multiple simulations and return
        AI recommendations for each run.
        """

        recommendations = []

        for _ in range(runs):

            simulation = self.controller.simulate(
                building_name=building_name
            )

            ai_response = self.llm.generate(
                simulation
            )

            recommendations.append(
                {
                    "simulation": simulation,
                    "recommendation": ai_response
                }
            )

        return {
            "building": building_name,
            "runs": runs,
            "results": recommendations
        }