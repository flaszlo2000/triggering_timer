from dataclasses import dataclass, field
from re import sub as re_sub
from typing import Dict

from config import Config
from yaml import dump as yaml_dump


@dataclass
class ServicesDataFieldDTO:
    description: str
    example: str


def generate_service_fields() -> Dict[str, ServicesDataFieldDTO]:
    return {
        Config.INPUT_ENTITY_ID.value: ServicesDataFieldDTO(
            "The automation to trigger",
            "automation.lights_on"
        ),
        Config.TRIGGER_AFTER_DELAY.value: ServicesDataFieldDTO(
            "The time delay before triggering the automation",
            "00:10:00"
        ),
        Config.INPUT_FRIENDLY_NAME.value: ServicesDataFieldDTO(
            "The friendly name of the automation",
            "automation"
        )
    }

@dataclass
class ServicesDataDTO:
    name: str = field(default = Config.NAME.value)
    description: str = field(default = "Triggers an automation after a specified delay.")
    fields: Dict[str, ServicesDataFieldDTO] = field(default_factory = generate_service_fields) 

def generate_domain() -> Dict[str, ServicesDataDTO]:
    return {
        Config.INTEGRATION_NAME.value: ServicesDataDTO()
    }


@dataclass
class ServicesDTO:
    domain: Dict[str, ServicesDataDTO] = field(default_factory = generate_domain)

def create_yaml() -> str:
    raw_yaml = yaml_dump(ServicesDTO().__dict__["domain"], default_flow_style = False)

    return re_sub(r"!!python/object:\S*", "", raw_yaml)

