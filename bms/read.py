import sys
import pandas as pd

import bms.common.myFileDialog as myfd
from bms.common.removeD import RemoveDecimal

class ReadForm:

    df : pd.DataFrame
    cName : str #사업자번호

    def run(self):
        self.readFile()
        self.selectColumn()
        self.prepList()

    def readFile(self) -> None:        
        path = myfd.askopenfilename("사업자리스트 엑셀파일을 선택하세요")
        try:
            self.df = pd.read_excel(path)
        except Exception as e:
            print(e)
            print("파일을 읽지 못했습니다.")
            sys.exit(0)

    def selectColumn(self):
        self.df.info()
        flag:str = input("사업자등록번호 컬럼을 선택하시오>>")
        self.cName = self.df.columns[int(flag)]

    def prepList(self):        
        self.df['TARGET'] = self.df[self.cName].copy()
        self.df['TARGET'] = self.df['TARGET'].astype('string').str.strip().replace('[-]','', regex=True)
        RemoveDecimal(self.df).run('TARGET')

