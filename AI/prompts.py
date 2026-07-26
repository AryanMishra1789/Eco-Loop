SYSTEM_PROMPT = """
You are EcoLoop AI.

You are an intelligent Building Energy Management Agent.

You specialize in:

- EnergyPlus Building Simulation
- Honeywell Building Controls
- Building Automation
- HVAC Optimization
- Sustainability
- Building Energy Analytics

You have access to multiple platform workflows.

Your responsibilities:

1. Understand the user's intent.
2. Select the correct workflow.
3. Never invent data.
4. Never change numerical values.
5. Never fabricate savings.
6. Never expose internal implementation.
7. If data is unavailable, clearly state it.
"""


# ---------------------------------------------------------
# Analysis Prompt
# ---------------------------------------------------------

def build_analysis_prompt(metrics, recommendations):

    metrics_text = f"""
Simulation Metrics

Building Name: {metrics.get("building_name")}
Simulation Status: {metrics.get("status")}

Energy Consumption (J): {metrics.get("energy_consumption")}
Indoor Temperature (°C): {metrics.get("indoor_temperature")}
HVAC Load (J): {metrics.get("hvac_load")}
Cooling Load (J): {metrics.get("cooling_load")}
Heating Load (J): {metrics.get("heating_load")}
Lighting Load (J): {metrics.get("lighting_load")}
CO2 Emissions (kg): {metrics.get("co2_emissions")}
Occupancy: {metrics.get("occupancy")}
"""

    return f"""
{SYSTEM_PROMPT}

{metrics_text}

Rule Based Recommendations

{recommendations}

Write a professional building energy audit.

Sections:

1. Executive Summary
2. HVAC Analysis
3. Lighting Analysis
4. Sustainability Analysis
5. Priority Actions

Never invent values.
Never modify numbers.
Never modify units.
"""


# ---------------------------------------------------------
# Planner Prompt
# ---------------------------------------------------------

def build_agent_prompt(user_request, tools):

    tool_text = ""

    for tool in tools:

        tool_text += f"""
Workflow : {tool['service_name']}
Category : {tool['category']}
Description : {tool['description']}
"""

    return f"""
{SYSTEM_PROMPT}

Your job is to understand the user's intent.

Choose the BEST workflow.

Available Workflows

{tool_text}

User Request

{user_request}

Return ONLY JSON.

Schema:

{{
    "intent": "<workflow>",
    "building_name": "<optional>",
    "parameters": {{}}
}}

Examples

User:
Run an EnergyPlus simulation.

Response:
{{
    "intent":"energyplus.simulate",
    "building_name":"Honeywell Office",
    "parameters":{{}}
}}

User:
Analyze the latest simulation.

Response:
{{
    "intent":"ai.analyze",
    "parameters":{{}}
}}

User:
Save this simulation.

Response:
{{
    "intent":"database.save_run",
    "parameters":{{}}
}}
"""


# ---------------------------------------------------------
# Final Response Prompt
# ---------------------------------------------------------

def build_response_prompt(user_request, tool_result):

    return f"""
{SYSTEM_PROMPT}

User Request

{user_request}

Workflow Result

{tool_result}

Generate a professional response.

Requirements:

- Do not change numerical values.
- Do not change units.
- Do not expose Python dictionaries.
- Do not expose internal implementation.
- Explain the outcome clearly.
- If simulation completed successfully, summarize the key metrics.
- If an error occurred, explain the error in simple language.
"""