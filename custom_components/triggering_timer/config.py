from enum import Enum

__version__ = "0.1.5"

class Config(str, Enum):
    INTEGRATION_NAME = "triggering_timer"

    INPUT_ENTITY_ID = "automation_entity_id"
    TRIGGER_AFTER_DELAY = "trigger_after_delay"
    TRIGGER_AFTER_DELAY_PARAMETER = "time_delay"
    INPUT_FRIENDLY_NAME = "name"

    WS_GET_TIMERS = "get_timers"
    WS_CANCEL_TIMER = "cancel_timer"

    NAME = "Triggering Timer Integration"


