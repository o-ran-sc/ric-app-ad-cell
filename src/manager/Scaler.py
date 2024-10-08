from CustomFileRepository import CustomFileRepository
from ..utils.constants import REPO_COUNT, REPO_MEAN, REPO_SD

import pandas as pd

from ..utils.Util import Util

log = Util.setup_logger()

class Scaler:

    def calculateNewScore(self, cell_name, kpi_list):
        pass

    def calculateExistingScore(self, cell, kpi_list, df_kpi_value):
        pass

    def calculate_score(self, cell_names, df_kpi_value):
        pass