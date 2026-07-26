# EcoLoop Architecture Document

## 1. Project Overview

EcoLoop is an AI-powered building energy optimization platform developed for the Honeywell Hackathon. The system integrates EnergyPlus simulations, an AI Agent powered by an open-source LLM, Model Context Protocol (MCP), and a Metadata-Driven Architecture to automate building analysis and generate energy optimization recommendations.

The platform allows users to run building simulations, analyze energy consumption, generate AI-based recommendations, and visualize results through an interactive dashboard.

---

# 2. System Architecture

The system consists of the following major components:

- Frontend Dashboard
- Flask REST API
- AI Runtime
- Metadata-Driven Generic API Caller
- MCP Server
- EnergyPlus Simulation Engine
- PostgreSQL Database

The frontend communicates with the Flask backend through REST APIs. The AI Runtime interprets user requests and selects the required workflow. The Generic API Caller executes services dynamically using metadata stored in the registry. MCP provides standardized tool access, while EnergyPlus performs building simulations. Results and recommendations are stored in PostgreSQL and displayed on the dashboard.

---

# 3. Project Structure

```
EcoLoop
│
├── AI
├── api
├── database
├── EnergyPlus
├── Generic_API_Caller
├── MCP
├── services
├── static
├── templates
├── building-model
├── migrations
│
├── app.py
├── config.py
├── bootstrap.py
├── requirements.txt
└── README.md
```

---

# 4. Metadata-Driven Architecture

The project follows a metadata-driven architecture where workflows are executed dynamically instead of being hardcoded.

Each service is registered with metadata including:

- Workflow name
- Service category
- Description
- Execution handler

When a request is received:

1. AI identifies the required workflow.
2. Dispatcher searches the service registry.
3. Executor invokes the corresponding service.
4. Results are returned to the AI Runtime.

This architecture makes the platform modular and allows new services to be added without modifying the execution logic.

---

# 5. Generic API Caller

The Generic API Caller is responsible for executing services dynamically.

Main components:

- APIConfig
- Registry
- Dispatcher
- Executor

Responsibilities:

- Register available services
- Discover workflows
- Route requests
- Execute services
- Return standardized responses

This removes tight coupling between modules and provides a reusable execution framework.

---

# 6. AI Runtime

The AI Runtime manages the complete AI execution pipeline.

Components include:

- Agent Runtime
- Agent Executor
- Agent Memory
- Recommendation Engine
- LLM Client

Responsibilities:

- Understand user prompts
- Select the correct workflow
- Execute required tools
- Maintain execution context
- Generate natural language responses

The project uses an open-source LLM through Ollama.

---

# 7. Model Context Protocol (MCP)

MCP provides a standardized interface between the AI Agent and backend tools.

Available tools include:

- EnergyPlus Simulation
- Database Access
- Weather Information
- Health Check

The MCP Server validates tool requests, executes the appropriate handler, and returns structured results to the AI Runtime.

---

# 8. EnergyPlus Integration

EnergyPlus is used as the simulation engine for building performance analysis.

Simulation workflow:

1. Select building model
2. Execute EnergyPlus simulation
3. Parse simulation outputs
4. Extract performance metrics
5. Generate optimization recommendations

Key outputs include:

- Energy Consumption
- HVAC Load
- Cooling Load
- Heating Load
- Lighting Load
- Indoor Temperature
- CO₂ Emissions

---

# 9. Database

PostgreSQL is used for storing application data and simulation history.

The database stores:

- Buildings
- Zones
- Sensors
- Sensor Readings
- Occupancy
- AI Recommendations

SQLAlchemy ORM is used for database operations, while Flask-Migrate manages schema migrations.

---

# 10. API Layer

The Flask backend exposes REST APIs for communication with the frontend.

Major endpoints include:

- Health Check
- AI Chat
- Available Tools
- Simulation
- Dashboard Data
- Optimization

These APIs act as the communication layer between the user interface and backend services.

---

# 11. Execution Flow

```
User

↓

Frontend Dashboard

↓

Flask API

↓

AI Runtime

↓

Generic API Caller

↓

Dispatcher

↓

Executor

↓

MCP Server

↓

EnergyPlus / Database

↓

Simulation Results

↓

Recommendation Engine

↓

Dashboard
```

---

# 12. Technologies Used

| Component | Technology |
|-----------|------------|
| Backend | Flask |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Migration | Flask-Migrate |
| AI Model | Ollama (Open Source LLM) |
| Simulation | EnergyPlus |
| Protocol | Model Context Protocol (MCP) |
| Architecture | Metadata-Driven Architecture |
| API Framework | Generic API Caller |
| Frontend | HTML, CSS, JavaScript |

---

# 13. Conclusion

EcoLoop combines AI, EnergyPlus, MCP, and a Metadata-Driven Architecture to provide an intelligent and modular building energy optimization platform. The Generic API Caller enables dynamic service execution, while the AI Runtime automates analysis and recommendation generation. The modular design allows the system to be easily extended with additional tools and workflows.