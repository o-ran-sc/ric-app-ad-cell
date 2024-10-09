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
        pass
        
    def updateScalars(self, cell, df_current):
        pass
        