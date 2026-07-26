# EcoLoop

EcoLoop is an AI building energy optimization platform developed for the Honeywell Hackathon.
It combines EnergyPlus simulations with AI to analyze building performance and provide actionable recommendations for improving energy efficiency.

## Features

- AI-powered building energy analysis
- EnergyPlus simulation integration
- Interactive dashboard
- AI Assistant for simulation insights
- Energy consumption reports
- Recommendation engine
- Flask-based backend
- PostgreSQL database

## Tech Stack

- Python
- Flask
- PostgreSQL
- SQLAlchemy
- EnergyPlus
- HTML
- CSS
- JavaScript

## Project Structure

```
EcoLoop/
├── AI/
├── api/
├── database/
├── EnergyPlus/
├── MCP/
├── services/
├── static/
├── templates/
├── migrations/
├── app.py
├── config.py
└── requirements.txt
```

## Installation

Clone the repository:

```bash
git clone https://github.com/AryanMishra1789/Eco-Loop.git
cd Eco-Loop
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment:

Windows

```bash
venv\Scripts\activate
```

Linux/macOS

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure the `.env` file with your local settings.

Run the application:

```bash
python app.py
```

