import asyncio
from typing import Any, Dict, Final, Optional, Set, Tuple, cast
from uuid import UUID

import voluptuous as vol
from homeassistant.components import websocket_api
from homeassistant.components.automation import DOMAIN as AUTOMATION_DOMAIN
from homeassistant.core import HomeAssistant, callback

from .cancellable_timer import CancellableTimer
from .config import Config
from .timers import Timers


class App:
    def __init__(self, *, timers: Optional[Timers] = None, stop_event: Optional[asyncio.Event] = None) -> None:
        self.__hass: Optional[HomeAssistant] = None
        self._timers: Timers = timers or Timers(self.broadcastTimerUpdate)

        self.__connected_users: Set[Tuple[websocket_api.ActiveConnection, int]] = set()

    #region utils
    def attachHass(self, hass: HomeAssistant) -> None:
        assert self.__hass is None

        self.__hass = hass

    def sendMessageToConnection(self, connection: websocket_api.ActiveConnection, session_id: int, msg: Any) -> None:
        connection.send_message(
            websocket_api.messages.event_message(
                session_id, msg
            )
        )

    def broadcastUpdate(self, message: Any) -> None:
        for connection, session_id in self.__connected_users:
            self.sendMessageToConnection(connection, session_id, message)

    def broadcastTimerUpdate(self) -> None:
        self.broadcastUpdate(self._timers.getTimersInJson())

    @staticmethod
    def validateUUID(_input: str) -> UUID:
        try:
            return UUID(_input)
        except ValueError:
            raise AttributeError("Incorrect id!")
    #endregion

    #region automation handling
    async def __triggerAutomation(self, automation_id: str) -> None:
        await self.__hass.services.async_call(
            AUTOMATION_DOMAIN,
            "trigger",
            {
                "entity_id": automation_id
            }
        )

    def __requestCallback(self, timer_id: UUID, automation_id: str) -> None:
        asyncio.run_coroutine_threadsafe(
            self.__triggerAutomation(automation_id), self.__hass.loop
        ).result()

        self._timers.removeTimer(timer_id)

    async def handleRequest(self, call) -> None:
        if self.__hass is None:
            raise RuntimeError("HomeAssistant instance must be attached before handling requests!")

        automation_entity_id: str = cast(str, call.data.get(Config.INPUT_ENTITY_ID.value))
        time_delay: int = cast(int, call.data.get(Config.TRIGGER_AFTER_DELAY_PARAMETER.value))
        friendly_name: str = cast(str, call.data.get(Config.INPUT_FRIENDLY_NAME.value))


        current_timer = CancellableTimer(
            time_delay,
            automation_entity_id,
            friendly_name,
            self.__requestCallback
        )
    
        self._timers.add(current_timer)
    #endregion

    #region ws endpoints
    def disconnect(self, connection: websocket_api.ActiveConnection) -> None:
        self.__connected_users.discard(connection)

    @websocket_api.websocket_command(
        {
            vol.Required("type"): f"{Config.INTEGRATION_NAME.value}/{Config.WS_GET_TIMERS.value}",
        }
    )
    @callback
    def ws_getTimers(self, hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: Dict[str, Any]) -> None:
        session_id: Final[int] = msg["id"]
        self.__connected_users.add((connection, session_id))

        connection.subscriptions[session_id] = lambda: self.disconnect(connection)
        connection.send_result(session_id) # ack the ws connection

        self.sendMessageToConnection(connection, session_id, self._timers.getTimersInJson())

    @websocket_api.websocket_command(
        {
            vol.Required("type"): f"{Config.INTEGRATION_NAME.value}/{Config.WS_CANCEL_TIMER.value}",
            vol.Required("uuid"): str
        }
    )
    @callback
    def ws_cancelTimer(self, hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: Dict[str, Any]) -> None:
        session_id: Final[int] = msg["id"]

        self._timers.cancelTimer(self.validateUUID(msg["uuid"]))

        response: Dict[str, Any] = {
            "status": "success",
            "data": {
                "uuid": msg["uuid"],
                "message": "Timer cancelled!",
            }
        }

        connection.send_result(session_id, response)
    #endregion
