from dataclasses import dataclass
from datetime import datetime, time
import re
from typing import List, Tuple

@dataclass
class Scheduler:
    """A class representing the workers schedule"""

    SHIFT_START = "__SHIFT_START__"

    def __init__(
        self,
        schedule: List[Tuple[float, str]],
        number_of_hours_per_day: int,
        shift_schedule: float,
        round_display_time: bool,
    ) -> None:
        """The schedule is a dictionary of task duration and task name.
        The duration as no unit, is just a proportion.
        The duration will be determined so that the list of task is over one hour."""

        self._number_of_hours_per_day = number_of_hours_per_day
        self._max_total = self._number_of_hours_per_day * 60

        self._stretch_factor = self._get_stretch_factor(schedule)
        marked_schedule = self._add_shift_start_marker(schedule, shift_schedule)
        self._marked_schedule = self._convert_durations_into_minutes(marked_schedule, round_display_time)

    def _add_shift_start_marker(
        self, schedule: List[Tuple[float, str]], shift_schedule: float
    ) -> List[Tuple[float, str]]:
        """Add a marker to the start of the shift for cases when the shift starts at a different time than the day"""

        if shift_schedule < 0 or shift_schedule >= schedule[-1][0]:
            raise ValueError("shift_schedule must be between 0 and the last task duration")

        schedule.insert(0, (shift_schedule, self.SHIFT_START))

        return schedule


    def _get_stretch_factor(self, schedule: List[Tuple[float, str]]) -> float:
        """Convert the durations into minutes"""
        
        durations = list(zip(*schedule))[0]
        total_duration = sum(durations)

        return self._max_total / total_duration

    @staticmethod
    def _round_to_five_minutes(minutes: int) -> int:
        """Round to the nearest five minutes"""
        return int(minutes / 5) * 5

    def _convert_durations_into_minutes(
        self, schedule: List[Tuple[float, str]], round_display_time: bool
    ) -> List[Tuple[float, str, str]]:
        """Convert the durations into minutes"""

        out = []
        acc_duration = 0
        for duration, task in schedule:

            if round_display_time:
                display_duration = self._round_to_five_minutes(acc_duration * self._stretch_factor)
            else:
                display_duration = acc_duration * self._stretch_factor

            out.append((
                duration * self._stretch_factor,
                task,
                self._get_corrected_time_text(display_duration),
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
        
        idx = None
        for i in range(len(self._marked_schedule)):
            if minutes <= acc + self._marked_schedule[i][0] - 1:                
                idx = i
                break
            acc += self._marked_schedule[i][0]

        # If we are before the shift start, we return the last index
        idx = idx if idx != 0 else len(self._marked_schedule) - 1

        assert idx is not None
        return idx

    def get_list_of_tasks(self, current_time: datetime) -> List[Tuple[str, str, bool]]:
        """Get a list of tasks and their status
        Returns a list of tuples of the form (time_text, task_text, is_done)"""
        current_index = self._get_task_index_for_minute(current_time)

        marked_list = [
            (time_text, task, i == current_index)
            for i, (_, task, time_text) in enumerate(self._marked_schedule)
        ]

        # Remove the shift start marker
        return marked_list[1:]