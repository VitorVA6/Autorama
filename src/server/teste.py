import time
from datetime import datetime, timedelta
import _thread as thread

#tempo1 = '2021-04-07 23:41:58.410152'.split(':')
#tempo2 = '2021-04-07 23:41:59.412152'.split(':')
#r=timedelta(minutes=float(tempo2[1]), seconds=float(tempo2[2]))-timedelta(minutes = float(tempo1[1]), seconds=float(tempo1[2]))
#print(r)
tags = ['carro1', 'carro2']
raceTags = []
tagBuffer = []

def dateOp():
    data1 = datetime.fromtimestamp(time.time())
    data2 = data1 + timedelta(minutes=2)
    if(data2 < data1):
        print('sim')
    else:
        print('nops')

def readerThread():
    c=0
    while c<300:
        if(tags[0] not in raceTags):
            tagBuffer.append({'tag':'carro1', 'time':datetime.fromtimestamp(time.time()), 'sent':'false'})
            raceTags.append('carro1')
            print('adicionado1')
            print(tagBuffer, raceTags)
        if(tags[1] not in raceTags):
            tagBuffer.append({'tag':'carro2', 'time':datetime.fromtimestamp(time.time()), 'sent':'false'})
            raceTags.append('carro2')
            print('adicionado2')
            print(tagBuffer, raceTags)
        time.sleep(0.1)
        c+=1
    return

def main():
    thread.start_new_thread(readerThread, ())
    while True:
        time.sleep(0.2)
        if(len(tagBuffer)>0 and tagBuffer[0]['sent'] == 'false'):
            print('enviado1')
            tagBuffer[0]['sent'] = 'true'
        if(len(tagBuffer)>1 and tagBuffer[1]['sent'] == 'false'):
            print('enviado2')
            tagBuffer[1]['sent'] = 'true'
        
        if (len(tagBuffer)>0):
            time1 = datetime.fromtimestamp(time.time()) - tagBuffer[0]['time']
            time2 = timedelta(seconds = 6)
            if(time1 > time2):
                del(tagBuffer[0])
                del(raceTags[0])
                print('deletado')


main()