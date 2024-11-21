import logging
from typing import Any, Dict, Final

from homeassistant.components import websocket_api
from homeassistant.core import HomeAssistant

from .app import App
from .config import Config

_LOGGER = logging.getLogger(__name__)
_APP: Final[App] = App()

async def async_setup(hass: HomeAssistant, config: Dict[str, Any]):
    _LOGGER.info("Setting up Time Automation integration")

    _APP.attachHass(hass)

    hass.services.async_register(
        Config.INTEGRATION_NAME.value,
        Config.TRIGGER_AFTER_DELAY.value,
        _APP.handleRequest
    )
   
    websocket_api.async_register_command(hass, _APP.ws_getTimers)
    websocket_api.async_register_command(hass, _APP.ws_cancelTimer)
    
    return True