from datetime import datetime
from pathlib import Path
import shutil

from EnergyPlus.config import EnergyPlusConfig


class EnergyPlusWorkspace:
    """
    Manages the EnergyPlus workspace.

    Responsibilities
    ----------------
    - Create simulation run directories
    - Clean output folders
    - Locate simulation files
    - Manage workspace lifecycle
    """

    def __init__(self):

        EnergyPlusConfig.ensure_workspace()

    # ---------------------------------------------------------

    def create_run_directory(self):
        """
        Create a unique run directory.

        Example
        -------
        D:\\EnergyPlus_Workspace\\Runs\\run_20260726_153205
        """

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        run_dir = (
            EnergyPlusConfig.RUNS_DIR /
            f"run_{timestamp}"
        )

        run_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        return run_dir

    # ---------------------------------------------------------

    def prepare_simulation(
        self,
        idf_file=None,
        weather_file=None
    ):
        """
        Prepare a simulation workspace.
        """

        run_dir = self.create_run_directory()

        if idf_file is None:
            idf_path = EnergyPlusConfig.DEFAULT_IDF
        else:
            idf_path = Path(idf_file)

        if weather_file is None:
            weather_path = EnergyPlusConfig.DEFAULT_WEATHER
        else:
            weather_path = Path(weather_file)

        return {

            "run_directory": run_dir,

            "idf_file": idf_path,

            "weather_file": weather_path,

            "output_csv":
                run_dir /
                EnergyPlusConfig.OUTPUT_CSV,

            "output_error":
                run_dir /
                EnergyPlusConfig.OUTPUT_ERROR,

            "output_table":
                run_dir /
                EnergyPlusConfig.OUTPUT_TABLE,

            "output_html":
                run_dir /
                EnergyPlusConfig.OUTPUT_HTML,

            "output_sql":
                run_dir /
                EnergyPlusConfig.OUTPUT_SQL

        }

    # ---------------------------------------------------------

    def clean_directory(
        self,
        directory
    ):
        """
        Delete all files inside a directory.
        """

        directory = Path(directory)

        if not directory.exists():
            return

        for item in directory.iterdir():

            if item.is_file():
                item.unlink()

            elif item.is_dir():
                shutil.rmtree(item)

    # ---------------------------------------------------------

    def remove_run(
        self,
        run_directory
    ):
        """
        Delete a simulation run.
        """

        run_directory = Path(run_directory)

        if run_directory.exists():
            shutil.rmtree(run_directory)

    # ---------------------------------------------------------

    def list_runs(self):
        """
        Return all simulation runs.
        """

        if not EnergyPlusConfig.RUNS_DIR.exists():
            return []

        runs = []

        for folder in sorted(
            EnergyPlusConfig.RUNS_DIR.iterdir()
        ):

            if folder.is_dir():

                runs.append({

                    "name": folder.name,

                    "path": str(folder),

                    "created":
                        datetime.fromtimestamp(
                            folder.stat().st_ctime
                        ).strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )

                })

        return runs

    # ---------------------------------------------------------

    def latest_run(self):
        """
        Return the latest simulation directory.
        """

        runs = self.list_runs()

        if not runs:
            return None

        return runs[-1]

    # ---------------------------------------------------------

    def workspace_info(self):
        """
        Return workspace information.
        """

        return {

            "workspace":
                str(
                    EnergyPlusConfig.WORKSPACE
                ),

            "runs_directory":
                str(
                    EnergyPlusConfig.RUNS_DIR
                ),

            "total_runs":
                len(
                    self.list_runs()
                )

        }