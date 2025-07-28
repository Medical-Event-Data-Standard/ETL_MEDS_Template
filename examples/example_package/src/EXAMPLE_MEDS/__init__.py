from importlib.metadata import PackageNotFoundError, version
from importlib.resources import files

from omegaconf import OmegaConf

__package_name__ = "EXAMPLE_MEDS"
try:
    __version__ = version(__package_name__)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"

MAIN_CFG = files(__package_name__).joinpath("configs/main.yaml")
EVENT_CFG = files(__package_name__).joinpath("configs/event_configs.yaml")
ETL_CFG = files(__package_name__).joinpath("configs/ETL.yaml")
DATASET_CFG = files(__package_name__).joinpath("dataset.yaml")

dataset_info = OmegaConf.load(DATASET_CFG)

__all__ = [
    "EVENT_CFG",
    "ETL_CFG",
    "MAIN_CFG",
    "DATASET_CFG",
    "dataset_info",
    "__package_name__",
    "__version__",
]
