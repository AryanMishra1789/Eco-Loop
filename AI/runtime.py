from Generic_API_Caller.dispatcher import Dispatcher


class EcoLoopRuntime:

    def __init__(self):

        self.dispatcher = Dispatcher()

    # ---------------------------------------------------------
    # Runtime Entry Point
    # ---------------------------------------------------------

    def execute(self, intent, **kwargs):

        if intent == "energyplus.simulate":

            return self.simulate_building(
                building_name=kwargs.get(
                    "building_name",
                    "Honeywell Office"
                ),
                idf_file=kwargs.get("idf_file"),
                weather_file=kwargs.get("weather_file")
            )

        elif intent == "database.save_run":

            return self.save_run(
                kwargs.get("metrics")
            )

        elif intent == "ai.analyze":

            return self.analyze_metrics(
                kwargs.get("metrics")
            )

        return {
            "success": False,
            "error": f"Unsupported workflow '{intent}'."
        }

    # ---------------------------------------------------------
    # Complete Simulation Workflow
    # ---------------------------------------------------------

    def simulate_building(
        self,
        building_name="Honeywell Office",
        idf_file=None,
        weather_file=None
    ):

        simulation_response = self.dispatcher.dispatch(
            "energyplus.simulate",
            building_name=building_name,
            idf_file=idf_file,
            weather_file=weather_file
        )

        if not simulation_response["success"]:
            return simulation_response

        metrics = simulation_response["result"]

        if metrics.get("status") == "Completed":

            save_response = self.save_run(metrics)

            if save_response["success"]:

                run = save_response["result"]

                metrics["run_id"] = run.id

        return self.analyze_metrics(metrics)

    # ---------------------------------------------------------
    # Save Simulation
    # ---------------------------------------------------------

    def save_run(self, metrics):

        return self.dispatcher.dispatch(
            "database.save_run",
            metrics
        )

    # ---------------------------------------------------------
    # Analyze Metrics
    # ---------------------------------------------------------

    def analyze_metrics(self, metrics):

        return self.dispatcher.dispatch(
            "ai.analyze",
            metrics
        )