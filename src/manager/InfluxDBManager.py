import configparser
import time
import influxdb_client
import pandas as pd

from .DetectionExecutor import DetectionExecutor

from ..utils import Util

from influxdb_client.client.write_api import SYNCHRONOUS

config = configparser.ConfigParser()
config.read('/tmp/src/configuration/config.ini')

log = Util.get_logger()

class InfluxDBManager:

    def getLatestData(self, measurement) -> pd.DataFrame:
        log.debug('InfluxDBManager.getLatestData :: getLatestData called')
        
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

    def query(self):
        log.debug('InfluxDBManager.query :: query called')
        while True:
            measurement = config.get('APP', 'MEASUREMENT_NAME')
            log.debug('measurement name [{}]'.format(measurement))
            latestDataDF = self.getLatestData(measurement)

            if not latestDataDF.empty:
                log.info(f"Latest data from measurement: '{measurement}'")
                Util.log_dataframe(latestDataDF)

                latestDataDF  = latestDataDF.drop(['table', '_start', '_stop', '_time', '_measurement', 'result'], axis=1)

                if len(latestDataDF.index) > int(config.get('APP', 'DETECTION_COUNT')):
                    log.info(f"Greater than 1 day suffiecient data is present to detect anamoly for cell  '{latestDataDF.loc[0, 'Short name']}'")
                    log.debug('latestDataDF.shape: [{}]'.format(latestDataDF.shape))
                    detectionExecutor = DetectionExecutor()
                    detectionExecutor.execute(latestDataDF.drop(['Short name'], axis=1))  
                else:
                    log.info(f"No suffiecient data to detect anamoly for cell  '{latestDataDF.loc[0, 'Short name']}'")       
            else:
                log.info(f"No data available in measurement '{measurement}'.")
            time.sleep(5)


    def write(self):
        client = influxdb_client.InfluxDBClient(url = config.get('APP', 'INFLUX_URL'),
                                     token=config.get('APP', 'INFLUX_TOKEN'),
                                     org=config.get('APP', 'INFLUX_ORG'))

        write_api = client.write_api(write_options=SYNCHRONOUS)

        point = influxdb_client.Point("g-nodeb").tag("Short name", "Cell-Name-01").field("DRB.UEThpDl", 100.0)\
            .field("DRB.UEThpUl", 100)\
            .field("ThpVolDl", 10)\
            .field("ThpVolUl", 10)\
            .field("RRC.ConnMean", 0.000001)\
            .field("CARR.WBCQIMean.BinX.BinY.BinZ", 10.0)\
            .field("Avg. DL PRB Utilization", 1.0)\
            .field("Avg. UL PRB Utilization", 1.0)\
            .field("DRB.PacketLossRateUl", 0.0)\
            .field("RRC Connection Success Rate (%)", 100.0)\
            .field("RRC Drop Rate (Session Drop Rate, %)", 0.0)\
            .field("HO Success Rate (%)", 100.0)\
            .field("RRE Success Rate (%)", 0.0)
        write_api.write(bucket=config.get('APP', 'INFLUX_BUCKET'), org=config.get('APP', 'INFLUX_ORG'), record=point)