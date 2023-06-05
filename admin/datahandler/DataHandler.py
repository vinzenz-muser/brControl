from datetime import datetime
import admin.datahandler.provider.SqlProvider as SqlProvider
import admin.datahandler.provider.InfluxProvider as InfluxProvider


class DataHandler:
    configured_providers = {
        "sql": SqlProvider.Provider,
        "influx": InfluxProvider.Provider,
    }

    def __init__(self, provider, config):
        try:
            self.provider = self.configured_providers[provider](config)
        except KeyError:
            raise KeyError("Provoider is not implemented!")
