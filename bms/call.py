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

    def __init__(self, objRF:ReadForm): #DI
        self.objRF = objRF

    def run(self) -> bool:        
        print("사전 준비합니다.")

        self.key = input("KEY? >> ") or r'%2FU0OKAbuaNxu6mUex7cGuk2gTjT%2BMU3xjJYVa%2BRVEZweDE0PmPxebPyk9LyRkNSfGf%2FzGtsplXf4HLTbZ3fMEw%3D%3D'

        self.getList()

        self.eachConn()        

    ##########################################

    def getList(self):            
        self.liTarget = self.objRF.df['TARGET'].to_list()
      
    def eachConn(self):
        print("조회대상:", len(self.liTarget))
        
        if len(self.liTarget) <= 100:
            print("조회대상이 100개 이하입니다. 단독 조회합니다.")            
        elif len(self.liTarget) > 100:
            print("조회대상이 100개 이하입니다. 순차 조회합니다.")

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

        pathTo = self.path + self.key

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
                  