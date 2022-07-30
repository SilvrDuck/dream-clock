from dataclasses import dataclass
from datetime import datetime
from typing import List, Tuple

@dataclass
class Scheduler:
    """A class representing the workers schedule"""

    def __init__(self, schedule: List[Tuple[float, str]]) -> None:
        """The schedule is a dictionary of task duration and task name.
        The duration as no unit, is just a proportion.
        The duration will be determined so that the list of task is over one hour."""

        self._schedule = self._convert_durations_into_datetimes(schedule)

    def _convert_durations_into_datetimes(self, schedule: List[Tuple[float, str]]) -> List[Tuple[float, str]]:
        """Convert the durations into minutes"""
        
        durations = list(zip(*schedule))[0]
        total_duration = sum(durations)

        stretch_factor = 60 / total_duration

        return [(duration * stretch_factor, task) for duration, task in schedule]

    def _get_task_index_for_minute(self, minute: int) -> int:
        """Get the index of the task that should be done at a given minute"""
        acc = 0
        for i in range(len(self._schedule)):
            if minute <= acc + self._schedule[i][0]:
                return i
            acc += self._schedule[i][0]


    def get_list_of_tasks(self, current_time: datetime) -> List[Tuple[str, bool]]:
        """Get a list of tasks and their status"""
        current_index = self._get_task_index_for_minute(current_time.minute)
        return [
            (task, i == current_index)
            for i, (_, task) in enumerate(self._schedule)
        ]