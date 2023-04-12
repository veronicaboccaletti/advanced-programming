import pandas as pd
from abc import ABC, abstractmethod
from dataset_reader import GFF3Reader

class Dataset(ABC):
    @abstractmethod
    def dataframe(self):
        pass

class GFF3Dataset(Dataset):
    def __init__(self, filename):
        self.__df = GFF3Reader(['seqid', 'source', 'type', 'start', 'end', 'score', 'strand', 'phase', 'attributes']).read(filename)

    @property
    def dataframe(self) -> pd.core.frame.DataFrame:
        return self.__df