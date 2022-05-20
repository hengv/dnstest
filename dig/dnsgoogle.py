import subprocess
from time import sleep,ctime

namelist = ['kuaishou.com','kuaishoupay.com','baidu.com','qq.com']

while True:
    for i in range(4):
        # print(namelist[i])
        result = subprocess.run(['dig',namelist[i],'@8.8.8.8'],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        str_result = result.stdout.decode('utf-8')
        content=ctime()+'\n ==========================================================   '+str_result
        # print(content)
        filename=namelist[i]+'google'
        f=open(filename,'a')
        f.write(content)
        f.close()
        sleep(30)
