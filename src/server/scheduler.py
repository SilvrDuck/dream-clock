from dataclasses import dataclass
from datetime import datetime, time
from typing import List, Tuple

@dataclass
class Scheduler:
    """A class representing the workers schedule"""

    def __init__(
        self,
        schedule: List[Tuple[float, str]],
        number_of_hours_per_day: int,
    ) -> None:
        """The schedule is a dictionary of task duration and task name.
        The duration as no unit, is just a proportion.
        The duration will be determined so that the list of task is over one hour."""

        self._number_of_hours_per_day = number_of_hours_per_day
        self._max_total = self._number_of_hours_per_day * 60
        self._stretch_factor = self._get_stretch_factor(schedule)
        self._schedule = self._convert_durations_into_minutes(schedule)

    def _get_stretch_factor(self, schedule: List[Tuple[float, str]]) -> float:
        """Convert the durations into minutes"""
        
        durations = list(zip(*schedule))[0]
        total_duration = sum(durations)

        return self._max_total / total_duration

    def _convert_durations_into_minutes(self, schedule: List[Tuple[float, str]]) -> List[Tuple[float, str, str]]:
        """Convert the durations into minutes"""

        out = []
        acc_duration = 0
        for duration, task in schedule:
            out.append((
                duration * self._stretch_factor,
                task,
                self._get_corrected_time_text(acc_duration * self._stretch_factor),
            ))
            acc_duration += duration

        return out

    def _get_corrected_time_text(self, minutes_after_start: float) -> str:
        """Add the start time to the task text"""
        hours_after_start = int(minutes_after_start / 60)
        minutes_after_hour = int(minutes_after_start % 60)

        if self._number_of_hours_per_day <= 1:
            strftime = "min %M"
        else:
            strftime = "%H:%M"

        return time(hours_after_start, minutes_after_hour).strftime(strftime)

    def _get_task_index_for_minute(self, current_time: datetime) -> int:
        """Get the index of the task that should be done at a given minute"""
        minutes = (current_time.hour * 60 + current_time.minute) % self._max_total
        acc = 0
        
        for i in range(len(self._schedule)):
            if minutes <= acc + self._schedule[i][0] - 1:                
                return i
            acc += self._schedule[i][0]

    def get_list_of_tasks(self, current_time: datetime) -> List[Tuple[str, str, bool]]:
        """Get a list of tasks and their status
        Returns a list of tuples of the form (time_text, task_text, is_done)"""
        current_index = self._get_task_index_for_minute(current_time)
        return [
            (time_text, task, i == current_index)
            for i, (_, task, time_text) in enumerate(self._schedule)
        ]