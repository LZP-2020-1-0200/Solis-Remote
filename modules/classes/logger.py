"""Contains a custom logging class"""
import logging
from datetime import datetime
from getpass import getuser
from pathlib import Path


class Logger:
    """Logs the module in a joined log file with timestamp and the module name"""
    def __init__(self, module_name:str) -> None:
        self._logger: logging.Logger = logging.getLogger(module_name)
        log_folder: Path = Path(f"C://users//{getuser()}//Desktop//solis_xy_log")
        log_folder.mkdir(parents=True, exist_ok=True)
        log_path: Path = Path(log_folder / (datetime.now().strftime("%Y.%m.%d_%H.00-.59") + ".log"))

        file_handler:logging.FileHandler = logging.FileHandler(str(log_path))
        file_handler.setLevel(logging.INFO)
        formatter: logging.Formatter= logging.Formatter(
            "%(asctime)s - %(levelname)s -"+module_name+"- %(message)s"
            )
        file_handler.setFormatter(formatter)
        self._logger.addHandler(file_handler)
        self._logger.setLevel(logging.DEBUG)

    def get_logger(self) -> logging.Logger:
        """Returns the custom modified logger."""
        return self._logger
