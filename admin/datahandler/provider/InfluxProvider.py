from admin.datahandler.provider.ProviderInterface import ProviderInterface
from datetime import datetime, timedelta
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS


class Provider(ProviderInterface):
    def __init__(self, config):
        self._client = influxdb_client.InfluxDBClient(
            url=config["url"],
            token=config["token"]
        )

        self.org = config["org"]
        self.bucket = config["bucket"]
        self.token = config["token"]
        self._write_api = self._client.write_api(write_options=SYNCHRONOUS)
        self._query_api = self._client.query_api()
    
    def load_values(self, sensorId: int, timespan: str, start: datetime, end: datetime=None):
        if end is None:
            end = datetime.utcnow()

        diff = int((end - start).total_seconds())

        if timespan == "point":
            query = ((  f'from(bucket: "{self.bucket}") |> range(start:-{diff}s)'
                        f' |> filter(fn:(r) => r._measurement == "sensor_data_point" and r.sensor == "{sensorId}")'))
        else:
            query = ((  f'from(bucket: "{self.bucket}") |> range(start:-{diff}s)'
                f' |> filter(fn:(r) => r._measurement == "sensor_data_point" and r.sensor == "{sensorId}")'
                f' |> aggregateWindow(every: {timespan}, fn: mean)'))


        tables = self._client.query_api().query(query, org=self.org)
        if len(tables) > 0:
            ans = [(row["_time"], row["_value"]) for row in tables[0].records]
        else:
            ans = []

        return ans

    def insert_value(self, sensorId: int, value: float, time: datetime=None, timespan="spot"):
        p = influxdb_client.Point("sensor_data_point").tag("sensor", sensorId).field("value", value)
        self._write_api.write(bucket=self.bucket, org=self.org, record=p)