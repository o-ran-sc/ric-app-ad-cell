from CustomFileRepository import CustomFileRepository
from ..utils.constants import REPO_COUNT, REPO_MEAN, REPO_SD

import pandas as pd

from ..utils.Util import Util

log = Util.setup_logger()

class Scaler:

    def calculateNewScore(self, cell_name, kpi_list):
        df_cell_score = dict()
        df_cell_score['Short name'] = cell_name
        for kpi in kpi_list:
            df_cell_score[kpi] = 0
        df_cell_score['is_new_cell'] = 1
        return pd.DataFrame([df_cell_score])

    def calculateExistingScore(self, cell, kpi_list, df_kpi_value):
        df_cell_mean = CustomFileRepository.scaler_dictionary.get(cell).get(REPO_MEAN)
        log.debug('df_cell_mean:')
        Util.log_dataframe(df_cell_mean)

        
        df_cell_sd = CustomFileRepository.scaler_dictionary.get(cell).get(REPO_SD)
        log.debug('df_cell_sd:')
        Util.log_dataframe(df_cell_sd)

        df_current_cell = df_kpi_value.loc[(df_kpi_value['Short name'] == cell),:]
        log.debug('df_current_cell:')
        Util.log_dataframe(df_current_cell)

        df_cell_score = dict()
        df_cell_score['Short name'] = cell
        for kpi in kpi_list:
            log.debug('kpi [{}]'.format(kpi))
            mean = df_cell_mean[kpi].values[0]
            log.debug('mean [{}]'.format(mean))
            sd = df_cell_sd[kpi].values[0]
            log.debug('sd [{}]'.format(sd))
            kpi_value = df_current_cell.loc[:, kpi].values[0]
            log.debug('kpi_value [{}]'.format(kpi_value))
            if sd == 0:
                df_cell_score[kpi] = 0
            else:
                df_cell_score[kpi] = (kpi_value - mean) / sd
        df_cell_score['is_new_cell'] = 0
        return pd.DataFrame([df_cell_score])

    def calculate_score(self, cell_names, df_kpi_value):
        pass