from dataclasses import dataclass, field
from datetime import datetime, timedelta
from threading import Timer
from typing import Callable
from uuid import UUID, uuid4


@dataclass
class CancellableTimer:
    interval: float
    automation_id: str
    friendly_name: str
    callback: Callable[[UUID, str], None]

    id: UUID = field(init = False, default_factory = uuid4)
    timer: Timer = field(init = False, repr = False)
    cancelled: bool = field(init = False, default = False)

    started: datetime = field(init = False, default_factory = datetime.now)
    will_end_at: datetime = field(init = False)

    def __post_init__(self) -> None:
        self.will_end_at = (self.started + timedelta(seconds = self.interval)).replace(microsecond = 0)

        self.timer = Timer(self.interval, self.__timer_callback)
        self.timer.start()

    def __timer_callback(self) -> None:
        if self.cancelled: return

        self.callback(self.id, self.automation_id)

    def cancel(self) -> None:
        self.cancelled = True
        self.timer.cancel()
