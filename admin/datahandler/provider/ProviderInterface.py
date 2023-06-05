from datetime import datetime


class ProviderInterface:
    def __init__(self, config):
        pass

    def load_values(
        self, sensorId: int, timespan: str, start: datetime, end: datetime = None
    ):
        pass

    def insert_value(self, sensorId: int, value: float, time: datetime = None):
        pass
