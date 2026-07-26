from pathlib import Path


class EnergyPlusConfig:
    """
    Central configuration for the EnergyPlus module.

    This class stores all file paths and default settings used
    by the simulator, parser, and controller.
    """

    # ==========================================================
    # EnergyPlus Installation
    # ==========================================================

    ENERGYPLUS_HOME = Path(r"C:\EnergyPlusV26-1-0")

    EXECUTABLE = "energyplus"

    # ==========================================================
    # Workspace
    # ==========================================================

    WORKSPACE = Path(r"D:\EnergyPlus_Workspace")

    EXAMPLE_DIR = WORKSPACE / "ExampleFiles"

    WEATHER_DIR = WORKSPACE / "WeatherData"

    RUNS_DIR = WORKSPACE / "Runs"

    OUTPUT_DIR = WORKSPACE / "Output"

    TEMP_DIR = WORKSPACE / "Temp"

    # ==========================================================
    # Default Simulation Files
    # ==========================================================

    DEFAULT_IDF = EXAMPLE_DIR / "RefBldgMediumOfficeNew2004_Chicago.idf"

    DEFAULT_WEATHER = (
        WEATHER_DIR
        / "USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.epw"
    )

    # ==========================================================
    # EnergyPlus Output Files
    # ==========================================================

    OUTPUT_CSV = "eplusout.csv"

    OUTPUT_ERROR = "eplusout.err"

    OUTPUT_TABLE = "eplustbl.csv"

    OUTPUT_HTML = "eplustbl.htm"

    OUTPUT_SQL = "eplusout.sql"

    OUTPUT_MTR = "eplusout.mtr"

    OUTPUT_AUDIT = "eplusout.audit"

    OUTPUT_EIO = "eplusout.eio"

    # ==========================================================
    # Simulation Settings
    # ==========================================================

    KEEP_PREVIOUS_RUNS = True

    CLEAN_TEMP_FILES = False

    SIMULATION_TIMEOUT = 300

    # ==========================================================
    # Utility Methods
    # ==========================================================

    @classmethod
    def ensure_workspace(cls):
        """
        Create the required workspace directories if they do not exist.
        """

        directories = [
            cls.WORKSPACE,
            cls.EXAMPLE_DIR,
            cls.WEATHER_DIR,
            cls.RUNS_DIR,
            cls.OUTPUT_DIR,
            cls.TEMP_DIR,
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

    @classmethod
    def validate(cls):
        """
        Validate the EnergyPlus installation and workspace.

        Returns
        -------
        dict
        """

        return {
            "energyplus_home": cls.ENERGYPLUS_HOME.exists(),
            "workspace": cls.WORKSPACE.exists(),
            "example_dir": cls.EXAMPLE_DIR.exists(),
            "weather_dir": cls.WEATHER_DIR.exists(),
            "runs_dir": cls.RUNS_DIR.exists(),
            "default_idf": cls.DEFAULT_IDF.exists(),
            "default_weather": cls.DEFAULT_WEATHER.exists(),
        }

    @classmethod
    def info(cls):
        """
        Return configuration details.
        """

        return {
            "energyplus_home": str(cls.ENERGYPLUS_HOME),
            "workspace": str(cls.WORKSPACE),
            "default_idf": str(cls.DEFAULT_IDF),
            "default_weather": str(cls.DEFAULT_WEATHER),
            "timeout": cls.SIMULATION_TIMEOUT,
        }