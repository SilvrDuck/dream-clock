from datetime import time, datetime


class StretcheableClock:
    """A clock that can be stretched so that hours are longer or shorter than 60 minutes."""

    def __init__(
        self, 
        start_time: time,
        hour_duration_in_minutes: float,
    ):
        """
        Args:
            start_time: The time at which the clock starts.
            hour_duration_in_minutes: The duration of an hour in minutes.
        """

        self.utc_start = datetime.utcnow()
        self.start_time = self.utc_start.replace(hour=start_time.hour, minute=start_time.minute)
        self.stretch_factor = 60 / hour_duration_in_minutes

    def get_time(self) -> datetime:
        """Get the current time, taking into account the stretch factor."""
        return self.start_time + (datetime.utcnow() - self.utc_start) * self.stretch_factor