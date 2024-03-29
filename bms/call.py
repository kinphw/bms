import sys
import requests
import json
import pandas as pd

from bms.read import ReadForm

class CallBMS:

    objRF:ReadForm
    path = r'https://api.odcloud.kr/api/nts-businessman/v1/status?serviceKey='

    liTarget:list
    response:requests.Response
    liResponse:list = []

    strKey:str = ''

    def __init__(self, objRF:ReadForm, strKey:str = ''): #DI
        self.objRF = objRF
        if not strKey == '': self.strKey = strKey

    def run(self) -> bool:        
        print("사전 준비합니다.")

        self.setKey()
        self.getList()
        self.eachConn()        

    ##########################################

    def setKey(self):
        if self.strKey == '':
            tmp = input("API KEY? >> ")
            if tmp == '':
                print("API KEY를 입력하지 않았습니다. 종료합니다.")
                sys.exit(0)
            else:
                self.strKey = tmp

    def getList(self):            
        #중복제거 구현
        print("조회대상 수 : ", self.objRF.df['TARGET'].shape[0])

        #NA제거
        print("결측치(NA 수): ", self.objRF.df['TARGET'].isna().sum())
        if self.objRF.df['TARGET'].isna().sum() != 0:
            print('결측치를 999-99-99999로 변환합니다.')
            self.objRF.df['TARGET'] = self.objRF.df['TARGET'].fillna("999-99-99999") #아예 바꿔야 나중에 merge 가능

        #중복제거
        dfDrop = self.objRF.df['TARGET'].drop_duplicates()                
        print("중복제거 후 조회대상 수 : ", dfDrop.shape[0])

        self.liTarget = dfDrop.to_list()
      
    def eachConn(self):
        print("조회대상:", len(self.liTarget))
        
        if len(self.liTarget) <= 100:
            print("조회대상이 100개 이하입니다. 단독 조회합니다.")            
        elif len(self.liTarget) > 100:
            print("조회대상이 100개 초과입니다. 순차 조회합니다.")

        self.liResponse = [] #결과물 초기화
        
        noStart = 0
        i = 0
        while True:
            i += 1
            noEnd = min(noStart + 100, len(self.liTarget))
            noCall = noEnd - noStart
            liSliced = self.liTarget[noStart:noEnd]
            if self.conn(liSliced): self.liResponse.append(self.response)
            print(i)            

            if noEnd == len(self.liTarget):
                print("순환 끝"); break
            else:
                noStart += noCall

    def conn(self, li:list) -> requests.Response:

        pathTo = self.path + self.strKey

        body = {
            "b_no": li
        }
        self.response = requests.post(pathTo, json=body)
        
        if self.response.status_code == 200:
            print("연결 성공")
            cntRequest = self.response.json()['request_cnt']
            cntMatch = self.response.json()['match_cnt']
            print("요청 : ",cntRequest)
            print("조회성공 : ",cntMatch)
            return True
        else:
            print("연결 실패")            
            print(self.response.status_code)
            print(self.response.json())
            return False
                  