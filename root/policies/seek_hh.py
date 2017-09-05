
from .base_policy import *
import talib
from datetime import datetime
import time
from ..stock_data import *
import numpy as np


@Policy.register('SeekHH', PolicyLifetime_EachCode)
class SeekHHPolicy(Policy):
    """
    Seek Hammer, Hanging-man.
    """

    def seek_hh(self, code, context):
        return True

    def handle(self, code, context):
        """
        """
        result = self.seek_hh(code, context)
        
        return result

    