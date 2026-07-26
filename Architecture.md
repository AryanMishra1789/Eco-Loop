# EcoLoop Architecture Document

**Project:** EcoLoop – AI-Powered Autonomous Building Energy Management Platform

---

# Table of Contents

1. Project Overview
2. System Architecture
3. Project Structure
4. Metadata-Driven Architecture
5. Generic API Caller
6. AI Runtime & MCP Integration
7. EnergyPlus Integration
8. Request Execution Flow
9. Database Design
10. API Structure
11. Dashboard

---

# 1. Project Overview

EcoLoop is an AI-powered building energy management platform that combines EnergyPlus simulations with an open-source Large Language Model (LLM) to automate building performance analysis and generate actionable energy optimization recommendations.

Instead of manually executing simulations and interpreting EnergyPlus outputs, users can interact with EcoLoop through a dashboard or AI assistant. The platform executes simulations, analyzes the generated results, and provides structured recommendations for improving building energy efficiency.

The system is built around a modular Metadata-Driven Architecture that enables flexible workflow execution through a Generic API Caller and an AI Runtime.

---

# 2. System Architecture

> **Insert Architecture Diagram Here**

The platform is organized into multiple independent layers.

```
+----------------------------------------------------+
|                  Frontend Dashboard                |
| Dashboard | Simulation | AI Assistant              |
+-------------------------+--------------------------+
                          |
                          v
+----------------------------------------------------+
|              Flask Backend (REST APIs)             |
+-------------------------+--------------------------+
                          |
                          v
+----------------------------------------------------+
|      Metadata Engine & Workflow Dispatcher         |
+-------------------------+--------------------------+
          |                                   |
          |                                   |
          v                                   v
+----------------------+       +----------------------------+
| Generic API Caller   |       | AI Runtime (Ollama + MCP)  |
+----------------------+       +----------------------------+
               \                      /
                \                    /
                 \                  /
                  v                v
              +------------------------+
              |      EnergyPlus        |
              +------------------------+
                         |
                         v
                Simulation Output Files
                         |
                         v
                  PostgreSQL Database
                         |
                         v
                  Dashboard Analytics
```

Each layer performs a dedicated responsibility, allowing the platform to remain modular and easy to extend.

---

# 3. Project Structure

```
EcoLoop
│
├── backend
│   ├── api
│   ├── agent
│   ├── metadata
│   ├── services
│   ├── models
│   ├── database
│   └── config
│
├── frontend
│   ├── dashboard
│   ├── simulation
│   ├── assistant
│   └── assets
│
├── building-model
│   └── RefBldgMediumOfficeNew2004_Chicago.idf
│
├── architecture
│   ├── Architecture.md
│   ├── architecture.png
│   ├── workflow.png
│   └── database_schema.png
│
└── README.md
```

### Backend

Implements the REST APIs, workflow execution, AI integration, metadata engine, simulation execution, and database communication.

### Frontend

Provides the user interface including dashboard visualizations, simulation controls, and AI assistant.

### Building Model

Contains the EnergyPlus reference building model used for simulations.

### Architecture

Contains the supporting architecture documentation and diagrams.

---

# 4. Metadata-Driven Architecture

EcoLoop follows a Metadata-Driven Architecture where workflow behavior is determined through metadata rather than hardcoded application logic.

Instead of embedding execution logic inside the application, metadata defines:

- Available services
- Workflow configuration
- API routing
- Execution parameters
- Response mapping

When a user submits a request, the Metadata Engine determines which workflow should be executed based on the request context.

```
User Request
      │
      ▼
Metadata Engine
      │
      ▼
Workflow Configuration
      │
      ▼
Generic API Caller
```

## Benefits

- Dynamic workflow execution
- Reduced code duplication
- Easier maintenance
- Configurable services
- Simplified extension of new workflows

---

# 5. Generic API Caller

The Generic API Caller acts as a centralized execution layer between the Metadata Engine and backend services.

Instead of directly invoking individual services throughout the application, every execution request is routed through a single generic interface.

```
Metadata
     │
     ▼
Generic API Caller
     │
     ▼
Target Service
```

## Responsibilities

- Reads workflow metadata
- Identifies the target service
- Builds the execution request
- Executes the required backend operation
- Handles exceptions
- Returns a standardized response

This approach removes direct dependencies between components and allows new services to be integrated with minimal changes.

---

# 6. AI Runtime & MCP Integration

The AI Runtime is responsible for processing user prompts and coordinating AI-assisted workflows.

The execution flow consists of:

```
User Prompt
      │
      ▼
Intent Detection
      │
      ▼
Workflow Selection
      │
      ▼
Tool Execution
      │
      ▼
LLM Analysis
      │
      ▼
Generated Response
```

EcoLoop uses an open-source LLM through Ollama for local inference.

The Model Context Protocol (MCP) provides a standardized interface between the AI Runtime and executable tools, enabling structured tool invocation and future extensibility.

---

# 7. EnergyPlus Integration

EnergyPlus serves as the building energy simulation engine.

Current simulation assets:

### Building Model

```
RefBldgMediumOfficeNew2004_Chicago.idf
```

### Weather File

```
USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.epw
```

Simulation outputs include metrics such as:

- Electricity consumption
- Heating load
- Cooling load
- HVAC performance
- Zone temperatures
- Equipment energy
- Lighting energy

These outputs are parsed into structured data and passed to the AI Runtime for analysis.

---

# 8. Request Execution Flow

The following sequence illustrates the complete request lifecycle.

```
User
 │
 ▼
Flask API
 │
 ▼
Metadata Engine
 │
 ▼
Generic API Caller
 │
 ▼
EnergyPlus
 │
 ▼
Output Parser
 │
 ▼
AI Runtime
 │
 ▼
PostgreSQL
 │
 ▼
Dashboard
```

### Workflow Description

1. User submits a request through the dashboard or AI assistant.
2. Flask receives the request.
3. The Metadata Engine selects the appropriate workflow.
4. The Generic API Caller invokes the required backend service.
5. EnergyPlus executes the simulation.
6. Simulation outputs are parsed into structured metrics.
7. The AI Runtime analyzes the results and generates recommendations.
8. Results are stored in PostgreSQL.
9. The dashboard displays updated analytics and recommendations.

---

# 9. Database Design

> **Insert Database Schema Diagram Here**

PostgreSQL stores all application data required for historical tracking and dashboard visualization.

Primary data includes:

- Simulation records
- Parsed EnergyPlus metrics
- AI-generated recommendations
- User requests
- Execution history

The database acts as the persistent storage layer for both simulation outputs and AI analysis.

---

# 10. API Structure

The backend exposes REST APIs for interacting with the AI assistant.

## Health Check

```
GET /api/agent/health
```

Returns the service status.

---

## Available Tools

```
GET /api/agent/tools
```

Returns the list of supported AI tools.

---

## AI Assistant

```
POST /api/agent/chat
```

Processes user requests and returns:

- Intent
- Selected workflow
- AI-generated response
- Simulation analysis
- Recommendations

Example response:

```json
{
    "intent": "energy_analysis",
    "workflow": "simulation_analysis",
    "response": "...",
    "tool_result": {
        "success": true,
        "analysis": "...",
        "metrics": {},
        "recommendations": []
    }
}
```

---

# 11. Dashboard

The dashboard provides a unified interface for monitoring simulation results and AI-generated insights.

Key features include:

- Energy KPI cards
- Interactive charts
- Simulation history
- AI recommendation panel
- Natural language assistant

Users can execute simulations, review historical analyses, and interact with the AI assistant from a single interface.