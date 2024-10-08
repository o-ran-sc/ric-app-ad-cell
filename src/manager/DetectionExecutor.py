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
        pass