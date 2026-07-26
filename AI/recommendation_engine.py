class RecommendationEngine:
    """
    Generates energy optimization recommendations
    based on EnergyPlus simulation metrics.
    """

    def __init__(self):
        pass

    def generate(self, metrics):

        recommendations = []

        # -----------------------------
        # Temperature
        # -----------------------------
        temp = metrics.get("indoor_temperature", 0)

        if temp > 26:
            recommendations.append({
                "category": "Cooling",
                "priority": "High",
                "recommendation": "Indoor temperature is high. Reduce cooling setpoint or improve insulation."
            })

        elif temp < 20:
            recommendations.append({
                "category": "Heating",
                "priority": "Medium",
                "recommendation": "Indoor temperature is low. Consider optimizing heating schedules."
            })

        # -----------------------------
        # HVAC
        # -----------------------------
        hvac = metrics.get("hvac_load", 0)

        if hvac > 1e9:
            recommendations.append({
                "category": "HVAC",
                "priority": "High",
                "recommendation": "HVAC energy usage is high. Check fan schedules and airflow rates."
            })

        # -----------------------------
        # Cooling
        # -----------------------------
        cooling = metrics.get("cooling_load", 0)

        if cooling > 1e9:
            recommendations.append({
                "category": "Cooling",
                "priority": "Medium",
                "recommendation": "Cooling demand is high. Consider shading, glazing improvements, or raising cooling setpoint."
            })

        # -----------------------------
        # Heating
        # -----------------------------
        heating = metrics.get("heating_load", 0)

        if heating > 1e9:
            recommendations.append({
                "category": "Heating",
                "priority": "Medium",
                "recommendation": "Heating demand is high. Improve insulation and reduce infiltration."
            })

        # -----------------------------
        # Lighting
        # -----------------------------
        lighting = metrics.get("lighting_load", 0)

        if lighting > 5e8:
            recommendations.append({
                "category": "Lighting",
                "priority": "Low",
                "recommendation": "Lighting energy is significant. Replace fixtures with LED lighting and install occupancy sensors."
            })

        # -----------------------------
        # CO2
        # -----------------------------
        co2 = metrics.get("co2_emissions", 0)

        if co2 > 1000:
            recommendations.append({
                "category": "Sustainability",
                "priority": "High",
                "recommendation": "Carbon emissions are high. Reduce electricity demand and increase renewable energy usage."
            })

        # -----------------------------
        # Energy Consumption
        # -----------------------------
        energy = metrics.get("energy_consumption", 0)

        if energy > 1e11:
            recommendations.append({
                "category": "Energy",
                "priority": "High",
                "recommendation": "Overall energy consumption is very high. Perform a detailed energy audit."
            })

        if not recommendations:

            recommendations.append({
                "category": "General",
                "priority": "Low",
                "recommendation": "Building performance is within acceptable limits."
            })

        return recommendations