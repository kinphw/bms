import os

from bms.read import ReadForm
from bms.call import CallBMS
from bms.export import ExportResult
from bms.common.colors import Colors

class BMSmain:

    objRF:ReadForm
    objCall:CallBMS
    strKey:str = ''

    def __init__(self, key:str = ''):
        if not key == '': self.strKey = key
    
    def run(self):
        os.system("")
        
        print(Colors.RED + "BMS : BusinessMan Status query (NTS) by PHW" + Colors.END)
        print("v0.0.6")
        
        msg = ""
        msg += "1. read form\n"
        msg += "2. call\n"
        msg += "3. export\n"
        msg += '99. DEBUG\n'

        msgNow = Colors.RED + '? : Help, q: Quit' + Colors.END

        while True:
            print(msgNow)
            flag = input(">>")

            if flag == '?': print(msg)
            elif flag == 'q':
                print("종료합니다."); break
            
            elif flag == '99': breakpoint()

            elif flag == '1':
                self.objRF = ReadForm()
                self.objRF.run()
            elif flag == '2':
                self.objCall = CallBMS(self.objRF, self.strKey)
                self.objCall.run()                    
            elif flag == '3':
                ExportResult(self.objCall, self.objRF).run()

def run():
    BMSmain().run()

if __name__=='__main__':
    BMSmain().run()