from datetime import time, datetime


class StretcheableClock:
    """A clock that can be stretched so that hours are longer or shorter than 60 minutes."""

    def __init__(
        self, 
        start_time: time,
        day_duration_in_minutes: float,
        number_of_hours_per_day: int,
    ):
        """
        Args:
            start_time: The time at which the clock starts.
            hour_duration_in_minutes: The duration of an hour in minutes.
        """

        self._check_arguments(start_time, number_of_hours_per_day)

        self.utc_start = datetime.utcnow()
        self.start_time = self.utc_start.replace(hour=start_time.hour, minute=start_time.minute)

        hour_duration_in_minutes = day_duration_in_minutes / number_of_hours_per_day
        self.stretch_factor = 60 / hour_duration_in_minutes

    @staticmethod
    def _check_arguments(start_time: time, number_of_hours_per_day: int) -> None:
        """Check that the arguments are valid."""

        if number_of_hours_per_day not in [1, 12, 24]:
            raise ValueError("number_of_hours_per_day must be 1, 12 or 24")

        if start_time.hour >= number_of_hours_per_day:
            raise ValueError("start_time must be before the end of the day")

    def get_time(self) -> datetime:
        """Get the current time, taking into account the stretch factor."""
        return self.start_time + (datetime.utcnow() - self.utc_start) * self.stretch_factor