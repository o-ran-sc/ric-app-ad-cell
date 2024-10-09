import configparser
import os
import influxdb_client
import pandas as pd

from ..utils.Util import Util

config = configparser.ConfigParser()
config.read(os.path.join(os.getcwd(), '../configuration/config.ini'))

log = Util.setup_logger()

class InfluxDBManager:

    def getLatestData(measurement) -> pd.DataFrame:
        client = influxdb_client.InfluxDBClient(url = config.get('APP', 'INFLUX_URL'),
                                     token=config.get('APP', 'INFLUX_TOKEN'),
                                     org=config.get('APP', 'INFLUX_ORG'))
        query_api = client.query_api()

        INFLUXDB_BUCKET = config.get('APP', 'INFLUX_BUCKET')
        flux_query = f'''
        from(bucket: "{INFLUXDB_BUCKET}")
            |> range(start: -5s)  // Adjust the range as needed
            |> filter(fn: (r) => r["_measurement"] == "{measurement}")
            |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
            |> sort(columns: ["_time"], desc: true)
            |> limit(n:1)
        '''

        try:
            df = query_api.query_data_frame(flux_query)
            return df
        except Exception as e:
            log.error(f"An error occurred while querying InfluxDB: {e}")
            return pd.DataFrame()
        finally:
            client.close() 

    def query(self, query):
        pass

    def write(self, data):
        pass