from typing import Final, Optional

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.automation.const import DOMAIN as AUTOMATION_DOMAIN
from homeassistant.components.binary_sensor import (BinarySensorDeviceClass,
                                                    BinarySensorEntity)
from homeassistant.components.switch import PLATFORM_SCHEMA
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from . import _APP  # FIXME: create a singleton to provide this
from .timers import Timers

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME): cv.string,
    vol.Required(AUTOMATION_DOMAIN): cv.string, #! test this
})

def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: Optional[DiscoveryInfoType] = None
) -> None:
    add_entities([
        TimerStateBinarySensor(_APP.getTimers(), config[AUTOMATION_DOMAIN])
    ])

class TimerStateBinarySensor(BinarySensorEntity):
    @property
    def is_on(self) -> bool:
        return self.__timers.hasTimerWithId(self._atuomation_id)

    @property
    def device_class(self) -> BinarySensorDeviceClass:
        return BinarySensorDeviceClass.RUNNING 

    def __init__(self, timers: Timers, automation_id: str) -> None:
        self.__timers: Final[Timers] = timers
        self._atuomation_id: Final[str] = automation_id
