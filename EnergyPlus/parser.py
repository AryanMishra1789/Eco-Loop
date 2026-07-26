import os
import pandas as pd


class EnergyPlusParser:
    """
    Parses EnergyPlus simulation outputs.

    Reads EnergyPlus generated files and converts them
    into a standardized format for the AI layer.
    """

    def __init__(self):
        pass

    # ---------------------------------------------------------

    def parse(self, simulation_result):

        if simulation_result["status"] != "Completed":

            return {

                "status": simulation_result["status"],

                "error": simulation_result.get("stderr", "")

            }

        csv_file = simulation_result["csv_file"]

        if not os.path.exists(csv_file):

            return {

                "status": "Failed",

                "error": "EnergyPlus output CSV not found."

            }

        try:

            df = pd.read_csv(csv_file)

        except Exception as e:

            return {

                "status": "Failed",

                "error": str(e)

            }

        metrics = self.extract_metrics(df)

        metrics["building_name"] = simulation_result["building_name"]

        metrics["simulation_time"] = simulation_result["execution_time"]

        metrics["run_directory"] = simulation_result["run_directory"]

        metrics["status"] = simulation_result["status"]

        return metrics

    # ---------------------------------------------------------

    def extract_metrics(self, df):
        metrics = {
            "energy_consumption": 0.0,
            "indoor_temperature": 0.0,
            "occupancy": 0,
            "hvac_load": 0.0,
            "lighting_load": 0.0,
            "cooling_load": 0.0,
            "heating_load": 0.0,
            "co2_emissions": 0.0
        }

        # -----------------------------
        # Total Facility Electricity
        # -----------------------------
        electricity_cols = [
            col for col in df.columns
            if "Electricity:Facility" in col
            and "[J]" in col
            and "(Hourly)" in col
        ]

        if electricity_cols:
            metrics["energy_consumption"] = (
                df[electricity_cols].sum().sum()
            )

        # -----------------------------
        # Indoor Temperature
        # -----------------------------
        temp_cols = [
            col for col in df.columns
            if "Zone Mean Air Temperature" in col
        ]

        if temp_cols:
            metrics["indoor_temperature"] = (
                df[temp_cols].mean().mean()
            )

        # -----------------------------
        # Fan Electricity
        # -----------------------------
        fan_cols = [
            col for col in df.columns
            if "Fan Electricity Energy" in col
        ]

        if fan_cols:
            metrics["hvac_load"] = (
                df[fan_cols].sum().sum()
            )

        # -----------------------------
        # Cooling
        # -----------------------------
        cooling_cols = [
            col for col in df.columns
            if "Cooling Energy" in col
            or "Cooling:Electricity" in col
        ]

        if cooling_cols:
            metrics["cooling_load"] = (
                df[cooling_cols].sum().sum()
            )

        # -----------------------------
        # Heating
        # -----------------------------
        heating_cols = [
            col for col in df.columns
            if "Heating Energy" in col
            or "Heating Coil Hot Water Energy" in col
            or "Heating:Electricity" in col
        ]

        if heating_cols:
            metrics["heating_load"] = (
                df[heating_cols].sum().sum()
            )

        # -----------------------------
        # Interior Lights
        # -----------------------------
        light_cols = [
            col for col in df.columns
            if "InteriorLights:Electricity" in col
        ]

        if light_cols:
            metrics["lighting_load"] = (
                df[light_cols].sum().sum()
            )

        # -----------------------------
        # CO2
        # -----------------------------
        co2_cols = [
            col for col in df.columns
            if "CO2:Facility" in col
        ]

        if co2_cols:
            metrics["co2_emissions"] = (
                df[co2_cols].sum().sum()
            )

        # -----------------------------
        # Occupancy
        # -----------------------------
        occ_cols = [
            col for col in df.columns
            if "People Occupant Count" in col
        ]

        if occ_cols:
            metrics["occupancy"] = int(
                df[occ_cols].max().max()
            )

        # -----------------------------
        # Round values
        # -----------------------------
        for key in metrics:
            if isinstance(metrics[key], float):
                metrics[key] = round(metrics[key], 2)

        return metrics

    # ---------------------------------------------------------

    def summarize(self, results):

        if not results:

            return {

                "total_buildings": 0,

                "average_energy": 0,

                "average_temperature": 0,

                "average_occupancy": 0

            }

        total_energy = sum(

            item.get("energy_consumption", 0)

            for item in results

        )

        total_temperature = sum(

            item.get("indoor_temperature", 0)

            for item in results

        )

        total_occupancy = sum(

            item.get("occupancy", 0)

            for item in results

        )

        count = len(results)

        return {

            "total_buildings": count,

            "average_energy": round(

                total_energy / count,

                2

            ),

            "average_temperature": round(

                total_temperature / count,

                2

            ),

            "average_occupancy": round(

                total_occupancy / count,

                2

            )

        }