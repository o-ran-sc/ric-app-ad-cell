import numpy as np
import pandas as pd

from CustomFileRepository import CustomFileRepository

from ..utils.Util import Util
from ..utils.constants import KPIS_INDEXER, REPO_COUNT, REPO_MEAN, REPO_POW_SUM, REPO_SD, REPO_SUM

log = Util.setup_logger()

class TrainingBatchExecutor:

    def getData(self):
        return CustomFileRepository.scaler_dictionary
    
    def reset(self):
        CustomFileRepository.scaler_dictionary = {}
        
    def updateScalars(self, cell, df_current):
        log.info('Update scalar started for [{}]'.format(cell))

        df_current.set_index(KPIS_INDEXER, inplace=True)

        if CustomFileRepository.scaler_dictionary.get(cell) is None:
            log.info('Dictionary not contains cell [{}].'.format(cell))
            
            df_sum = df_current.groupby(KPIS_INDEXER).sum()
            log.debug('df_sum content:')
            Util.log_dataframe(df_sum)
            
            df_powsum = df_current.groupby(KPIS_INDEXER).apply(lambda x: np.square(x).sum())
            log.debug('df_powsum content:')
            Util.log_dataframe(df_powsum)

            df_count = pd.DataFrame(df_current.groupby(KPIS_INDEXER).apply(lambda x: len(x)))
            df_count.columns = ['count']
            log.debug('df_count content:')
            Util.log_dataframe(df_count)

            df_org_cumsum = df_sum
            df_org_powsum = df_powsum
            df_org_count = df_count
        else:
            log.info('Dictionary not contains cell [{}].'.format(cell))
            # TO DO - add else logic

        df_org_mean = pd.DataFrame(df_org_cumsum.values / df_org_count.values, index=df_org_cumsum.index,
                                       columns=df_org_cumsum.columns)
        log.debug('df_org_mean: ')
        Util.log_dataframe(df_org_mean)
        
        df_org_var = (df_org_powsum - (df_org_cumsum * df_org_mean)) / (df_org_count.values - 1)
        log.debug('df_org_var: ')
        Util.log_dataframe(df_org_var)

        df_org_sd = np.sqrt(df_org_var)
        log.debug('df_org_sd: ')
        Util.log_dataframe(df_org_sd)

        df_org_count =  df_org_count.fillna(0).reset_index()
        log.debug('df_org_count: ')
        Util.log_dataframe(df_org_count)

        df_org_cumsum = df_org_cumsum.fillna(0).reset_index()
        log.debug('df_org_cumsum: ')
        Util.log_dataframe(df_org_cumsum)

        df_org_mean = df_org_mean.fillna(0).reset_index()
        log.debug('df_org_mean: ')
        Util.log_dataframe(df_org_mean)

        df_org_powsum = df_org_powsum.fillna(0).reset_index()
        log.debug('df_org_powsum: ')
        Util.log_dataframe(df_org_powsum)

        df_org_sd =  df_org_sd.fillna(0).reset_index()
        log.debug('df_org_sd: ')
        Util.log_dataframe(df_org_sd)

        CustomFileRepository.scaler_dictionary[cell] =  {REPO_SUM: df_org_cumsum, REPO_MEAN: df_org_mean, REPO_SD: df_org_sd, 
                                           REPO_COUNT: df_org_count, REPO_POW_SUM: df_org_powsum}
        log.debug('Dictionary after scaler update[{}].'.format(CustomFileRepository.scaler_dictionary))
        
        df_current.reset_index(inplace=True)
        