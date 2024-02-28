import pandas as pd

from bms.common.ErrRetry import ErrRetryF
from bms.common.protoSelector import ProtoABSSelector

class RemoveDecimal(ProtoABSSelector):

    # df:pd.DataFrame

    # def __init__(self, df:pd.DataFrame):
    #     self.df = df

    @ErrRetryF    
    def run(self, cName:str): #Drop Column
        
        print("문자열 dtype으로 바꿉니다.")
        self.df[cName] = self.df[cName].astype('string')

        print("NA는 ''으로 전처리합니다.")
        self.df[cName] = self.df[cName].fillna('')
        
        print("본작업 개시")
        self.df[cName] = self.df[cName].apply(self.remove)
        print("DONE")

    def remove(self, text):
        if ".0" in text:
            return text[:text.rfind('.0')]
        else:
            return text
        
