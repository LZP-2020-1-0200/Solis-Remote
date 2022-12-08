import logging
from datetime import datetime
from getpass import getuser
from pathlib import Path


class Logger:
    def __init__(self, module_name:str) -> None:
        self.logger: logging.Logger = logging.getLogger(module_name)

        log_folder: Path = Path(f"C://users//{getuser()}//Desktop//solis_xy_log")
        log_folder.mkdir(parents=True, exist_ok=True)
        log_path: Path = Path(log_folder / (datetime.now().strftime("%Y%m%d_%H%M") + ".log"))

        fh:logging.FileHandler = logging.FileHandler(str(log_path))
        fh.setLevel(logging.INFO)
        formatter: logging.Formatter= logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

    def get_logger(self) -> logging.Logger:
        return self.logger