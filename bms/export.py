import time
import pandas as pd
from bms.call import CallBMS
from bms.read import ReadForm

class ExportResult:

    objCall:CallBMS
    objRF:ReadForm
    dfResult:pd.DataFrame

    def __init__(self, objCall:CallBMS, objRF:ReadForm): #DI
        self.objCall = objCall        
        self.objRF = objRF

    def run(self):
        print("조회결과를 추출합니다.")
        dfResultRaw = self.extract()
        self.prep(dfResultRaw)
        self.merge()
        self.export()
        self.clean()
    #############################################################

    def extract(self):
        dfCon = pd.DataFrame()
        for res in self.objCall.liResponse:
            df = pd.json_normalize(res.json()['data'])
            dfCon = pd.concat([dfCon, df])
        print("총 추출건수 : ", dfCon.shape[0])
        return dfCon

    def prep(self, df:pd.DataFrame) -> pd.DataFrame:
        
        #전처리        
        dfSliced = df[[
            'b_no',
            'b_stt',
            'tax_type',
            'end_dt',
            'utcc_yn',
            'tax_type_change_dt',
            'invoice_apply_dt',
            'rbf_tax_type'
        ]].copy()

        diMapColumn = {
            'b_no':'사업자등록번호',
            'b_stt':'납세자상태',
            'tax_type':'과세유형메시지',
            'end_dt':'폐업일',
            'utcc_yn':'단위과세전환폐업여부',
            'tax_type_change_dt':'최근과세유형전환일자',
            'invoice_apply_dt':'세금계산서적용일자',
            'rbf_tax_type': '직전과세유형메세지'
        }
        self.dfResult = dfSliced.rename(columns=diMapColumn)
    
    def merge(self):

        print("요청자료 행수: ",self.objRF.df.shape[0])
        self.dfResult = pd.merge(self.objRF.df, self.dfResult, how='left', left_on='TARGET', right_on='사업자등록번호')         
        print("결과 행수: ", self.dfResult.shape[0])

        self.dfResult.drop(columns=['TARGET'], inplace=True)
    
    def export(self):
        strName = input("회사명? >>")
        strDatetime = time.strftime("%Y%m%d_%H%M%S")
        strFile = "휴폐업조회_" + strName + "_" + strDatetime + ".xlsx"        
        self.dfResult.to_excel(strFile, index=False)
        
        print("DONE")        

    def clean(self):
        print("객체에서 이번 결과를 삭제합니다. (다음 결과에 영향을 주지 않도록)")
        self.objCall.liResponse = []