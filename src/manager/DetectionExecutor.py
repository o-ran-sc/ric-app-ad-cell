import numpy as np
import pandas as pd

from ..utils.constants  import  MODEL_AD_CELL_FILE_NAME
from ..utils.FileLoader import FileLoader
from ..utils.Util import Util

from Scaler import Scaler


log = Util.setup_logger()


class DetectionExecutor:

    def execute(self, df):
        pass

    def data_scaling(self, df):
        log.debug('input df:')
        Util.log_dataframe(df)

        scaler = Scaler()
        result_df_kpi_value, result_df_cell_scores  = scaler.calculate_score([df.iloc[0]['Short name']], df)

        log.debug('result_df_kpi_value:')
        Util.log_dataframe(result_df_kpi_value)

        log.debug('result_df_cell_scores:')
        Util.log_dataframe(result_df_cell_scores)

        df_new = []
        df_scaled = []

        df_new.append(result_df_kpi_value)
        df_scaled.append(result_df_cell_scores)

        df = pd.concat(df_new)
        df_scaled = pd.concat(df_scaled)
        df.reset_index(inplace=True)
        df_scaled.reset_index(inplace=True)
        df.drop(columns=['index'], inplace=True)
        df_scaled.drop(columns=['index'], inplace=True)
        df['is_new_cell'] = df_scaled['is_new_cell']
        df_scaled.fillna(0, inplace=True)

        log.debug('output df:')
        Util.log_dataframe(df)

        log.debug('output df_scaled:')
        Util.log_dataframe(df_scaled)
        return df, df_scaled