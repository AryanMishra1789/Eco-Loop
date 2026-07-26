import subprocess
import time
from pathlib import Path

from EnergyPlus.config import EnergyPlusConfig
from EnergyPlus.workspace import EnergyPlusWorkspace


class EnergyPlusSimulator:
    """
    Executes a real EnergyPlus simulation.
    """

    def __init__(self):

        self.status = "Idle"

        self.workspace = EnergyPlusWorkspace()

    # ---------------------------------------------------------

    def run_simulation(
        self,
        building_name,
        weather_file=None,
        idf_file=None
    ):

        self.status = "Running"

        start = time.perf_counter()

        simulation = self.workspace.prepare_simulation(
            idf_file=idf_file,
            weather_file=weather_file
        )

        run_directory = simulation["run_directory"]

        idf_path = simulation["idf_file"]

        weather_path = simulation["weather_file"]

        if not idf_path.exists():

            raise FileNotFoundError(
                f"IDF file not found:\n{idf_path}"
            )

        if not weather_path.exists():

            raise FileNotFoundError(
                f"Weather file not found:\n{weather_path}"
            )

        command = [

            EnergyPlusConfig.EXECUTABLE,

            "-w",
            str(weather_path),

            "-d",
            str(run_directory),

            "-r",

            str(idf_path)

        ]

        try:

            process = subprocess.run(

                command,

                capture_output=True,

                text=True,

                timeout=EnergyPlusConfig.SIMULATION_TIMEOUT

            )

        except subprocess.TimeoutExpired:

            self.status = "Timeout"

            return {

                "building_name": building_name,

                "status": "Timeout",

                "run_directory": str(run_directory),

                "stdout": "",

                "stderr": "Simulation timeout."

            }

        execution_time = round(

            time.perf_counter() - start,

            2

        )

        error_file = run_directory / EnergyPlusConfig.OUTPUT_ERROR

        simulation_error = ""

        if error_file.exists():

            simulation_error = error_file.read_text(
                encoding="utf-8",
                errors="ignore"
            )

        success = (

            process.returncode == 0

        )

        self.status = "Completed" if success else "Failed"

        return {

            "building_name": building_name,

            "status": self.status,

            "run_directory": str(run_directory),

            "idf_file": str(idf_path),

            "weather_file": str(weather_path),

            "stdout": process.stdout,

            "stderr": process.stderr,

            "error_log": simulation_error,

            "execution_time": execution_time,

            "csv_file": str(
                run_directory /
                EnergyPlusConfig.OUTPUT_CSV
            ),

            "table_file": str(
                run_directory /
                EnergyPlusConfig.OUTPUT_TABLE
            ),

            "html_report": str(
                run_directory /
                EnergyPlusConfig.OUTPUT_HTML
            )

        }

    # ---------------------------------------------------------

    def get_status(self):

        return {

            "status": self.status

        }

    # ---------------------------------------------------------

    def reset(self):

        self.status = "Idle"