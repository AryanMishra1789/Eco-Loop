from EnergyPlus.simulator import EnergyPlusSimulator
from EnergyPlus.parser import EnergyPlusParser


class EnergyPlusController:
    """
    EnergyPlus Controller

    Responsibilities
    ----------------
    - Execute EnergyPlus simulations
    - Parse simulation results
    - Batch simulations
    - Compare simulations
    """

    def __init__(self):

        self.simulator = EnergyPlusSimulator()

        self.parser = EnergyPlusParser()

    # ---------------------------------------------------------

    def simulate(self, building_name="Building", idf_file=None, weather_file=None):
        simulation_result = self.simulator.run_simulation(
            building_name=building_name,
            idf_file=idf_file,
            weather_file=weather_file
        )

        parsed_result = self.parser.parse(simulation_result)

        simulation_result.update(parsed_result)

        return simulation_result

    # ---------------------------------------------------------

    def batch_simulation(
        self,
        buildings
    ):
        """
        Run simulations for multiple buildings.
        """

        results = []

        for building in buildings:

            result = self.simulate(

                building_name=building

            )

            results.append(result)

        return {

            "total_buildings": len(results),

            "results": results,

            "summary": self.parser.summarize(results)

        }

    # ---------------------------------------------------------

    def compare_simulations(
        self,
        first_result,
        second_result
    ):
        """
        Compare two EnergyPlus simulations.
        """

        return {

            "energy_difference":

                second_result.get(
                    "energy_consumption",
                    0
                )

                -

                first_result.get(
                    "energy_consumption",
                    0
                ),

            "temperature_difference":

                second_result.get(
                    "indoor_temperature",
                    0
                )

                -

                first_result.get(
                    "indoor_temperature",
                    0
                ),

            "occupancy_difference":

                second_result.get(
                    "occupancy",
                    0
                )

                -

                first_result.get(
                    "occupancy",
                    0
                ),

            "cooling_difference":

                second_result.get(
                    "cooling_load",
                    0
                )

                -

                first_result.get(
                    "cooling_load",
                    0
                ),

            "heating_difference":

                second_result.get(
                    "heating_load",
                    0
                )

                -

                first_result.get(
                    "heating_load",
                    0
                )

        }

    # ---------------------------------------------------------

    def get_status(self):
        """
        Return simulator status.
        """

        return self.simulator.get_status()

    # ---------------------------------------------------------

    def workspace_info(self):
        """
        Return workspace information.
        """

        return self.simulator.workspace.workspace_info()

    # ---------------------------------------------------------

    def latest_run(self):
        """
        Return latest simulation directory.
        """

        return self.simulator.workspace.latest_run()