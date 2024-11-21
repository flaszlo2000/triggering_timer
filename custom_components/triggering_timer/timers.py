from typing import (Callable, Dict, Final, Iterable, List, Optional, Tuple,
                    Union, overload)
from uuid import UUID

from .cancellable_timer import CancellableTimer


class Timers:
    def __init__(
        self,
        timers_changed_callback: Callable[[], None],
        timers: Optional[Iterable[CancellableTimer]] = None
    ) -> None:
        self.timers_changed_callback: Final[Callable[[], None]] = timers_changed_callback
        self.__timers: List[CancellableTimer] = list()

        if timers is not None:
            self.__timers.extend(timers)

    def __getTimer(self, uuid: UUID) -> CancellableTimer:
        timer_with_id = list(filter(lambda timer: timer.id == uuid, self.__timers))

        if len(timer_with_id) != 1:
            raise AttributeError(f"{uuid} was not found!")

        return timer_with_id[0]

    @overload
    def removeTimer(self, _input: UUID) -> None:...
    @overload
    def removeTimer(self, _input: CancellableTimer) -> None:...

    def removeTimer(self, _input: Union[UUID, CancellableTimer]) -> None:
        timer_to_remove: CancellableTimer = self.__getTimer(_input) if isinstance(_input, UUID) else _input
        self.__timers.remove(timer_to_remove)

        self.timers_changed_callback()

    def getTimersInJson(self) -> Dict[UUID, Tuple[str, str]]:
        return {
            timer.id: (timer.friendly_name, str(timer.will_end_at)) for timer in self.__timers
        }

    def add(self, new_timer: CancellableTimer) -> None:
        self.__timers.append(new_timer)
        
        self.timers_changed_callback()

    def cancelTimer(self, timer_id: UUID) -> None:
        timer_to_cancel = self.__getTimer(timer_id)
        timer_to_cancel.cancel()

        self.removeTimer(timer_to_cancel)
