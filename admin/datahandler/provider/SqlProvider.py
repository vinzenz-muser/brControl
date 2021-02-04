from admin.datahandler.provider.ProviderInterface import ProviderInterface
from datetime import datetime

class Provider(ProviderInterface):
    def __init__(self, config):
        self._models = config['models']
        self.Value = self._models.Value
        self._db = config['db']
    
    def load_values(self, sensorId: int, timespan: str, start: datetime, end: datetime=None):
        if end is None:
            end = datetime.utcnow()

        relevant_values = self.Value.query.filter(self.Value.timespan==timespan).filter(self.Value.time.between(start,end)).all()
        return [(relevant_value.time, relevant_value.value) for relevant_value in relevant_values]

    def insert_value(self, sensorId: int, value: float, time: datetime=None, timespan="spot"):
        add_val = self.Value(value=value, sensorId=sensorId, time=time, timespan=timespan)
        self._db.session.add(add_val)
        self._db.session.commit()