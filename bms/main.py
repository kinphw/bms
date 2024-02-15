from bms.read import ReadForm
from bms.call import CallBMS
from bms.export import ExportResult

class BMSmain:

    objRF:ReadForm
    objCall:CallBMS

    def run(self):
        print("BMS : BusinessMan Status query (NTS)")
        print("v0.0.1")
        
        msg = ""
        msg += "1. read form (최대 100개)\n"
        msg += "2. call\n"
        msg += "3. export\n"
        msg += '99. DEBUG\n'

        msgNow = '? : Help, q: Quit'

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
                self.objCall = CallBMS(self.objRF)
                self.objCall.run()                    
            elif flag == '3':
                ExportResult(self.objCall, self.objRF).run()        

if __name__=='__main__':
    BMSmain().run()