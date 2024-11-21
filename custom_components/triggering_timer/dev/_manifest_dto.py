from dataclasses import dataclass, field
from typing import List

from config import Config, __version__


@dataclass
class ManifestDTO:
    domain: str = field(default = Config.INTEGRATION_NAME.value)
    name: str = field(default = Config.NAME.value)
    version: str = field(default = __version__)

    codeowners: List[str] = field(default_factory = lambda: ["@flaszlo2000"])
    documentation: str = field(default = "https://github.com/flaszlo2000/triggering_timer")

    iot_class: str = field(default = "local_push")

    dependencies: List[str] = field(default_factory = list)
    requirements: List[str] = field(default_factory = list)
