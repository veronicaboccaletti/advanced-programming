import pandas as pd
from abc import ABC, abstractmethod

class Reader(ABC):
    @abstractmethod
    def __init__(self, cols: list, *arg, **kwargs):
        pass

    @abstractmethod
    def read(self):
        pass

class GFF3Reader(Reader):
    def __init__(self, cols: list):
        self.__cols = cols

    def read(self, filepath: str):
        return pd.read_csv(filepath, sep='\t', names=self.__cols, comment='#', low_memory=False)
