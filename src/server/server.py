import socket
import time
from datetime import datetime, timedelta
import _thread as thread
#import mercury

tags = ['carro1', 'carro2']
rfid = []
raceTags = []
tagBuffer = []
restAPI = {'method':'', 'route':''}

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 5022))
s.listen(5)

def methodIdentifier(data):
    global restAPI
    data = data.split(' ')
    restAPI['method'] = data[0]
    restAPI['route'] = data[1]
    if (restAPI['method'] == 'GET'):
        get(restAPI['route'])
    elif (restAPI['method'] == 'POST'):
        post(restAPI['route'])

def tagToString(t):
    result = ''
    for i in t:
        result = result + i + ':'
    return result

def readerThread():
    c=0
    while c<200:
        if(tags[0] not in raceTags):
            tagBuffer.append({'tag':'carro1', 'time': datetime.fromtimestamp(time.time()), 'sent':'false'})
            raceTags.append('carro1')
            print('adicionado1')
            print(tagBuffer, raceTags)
        if(tags[1] not in raceTags):
            tagBuffer.append({'tag':'carro2', 'time':datetime.fromtimestamp(time.time())-timedelta(seconds=0.32), 'sent':'false'})
            raceTags.append('carro2')
            print('adicionado2')
            print(tagBuffer, raceTags)
        time.sleep(0.1)
        c+=1
    print('Thread encerrada')
    return

def readerQualify(data):
    t = 0
    dataList = data.split(':')    
    info = str(datetime.fromtimestamp(time.time()))
    clientSocket.send(bytes(info, 'utf-8'))
    thread.start_new_thread(readerThread, ())
    while t<int(dataList[1]): 
        time.sleep(0.1)
        if(len(tagBuffer)>0 and tagBuffer[0]['sent'] == 'false'):
            info =  raceTags[0]+ '/'+ str(tagBuffer[0]['time'])
            clientSocket.send(bytes(info, 'utf-8')) 
            print('enviado1')
            tagBuffer[0]['sent'] = 'true'
        time.sleep(0.3)
        if(len(tagBuffer)>1 and tagBuffer[1]['sent'] == 'false'):
            info =  raceTags[1]+ '/'+ str(tagBuffer[1]['time'])
            clientSocket.send(bytes(info, 'utf-8')) 
            print('enviado2')
            tagBuffer[1]['sent'] = 'true'
        
        if (len(tagBuffer)>0):
            time1 = datetime.fromtimestamp(time.time()) - tagBuffer[0]['time']
            time2 = timedelta(seconds = 6)
            if(time1 > time2):
                del(tagBuffer[0])
                del(raceTags[0])
                print('deletado')
        #time.sleep(2.4)
        #info =  tags[1]+ '/'+ str(datetime.fromtimestamp(time.time()))
        #clientSocket.send(bytes(info, 'utf-8'))  
        #time.sleep(0.4)        
        #info =  tags[0]+ '/'+ str(datetime.fromtimestamp(time.time()))
        #clientSocket.send(bytes(info, 'utf-8'))    
        t +=0.3
        #print(t)
    clientSocket.send(bytes('q/q', 'utf-8'))
    return



def get(data):
    global tags
    global restAPI
    data = data.split(':')
    if (data[0] =='autorama/cars'):
        #reader = mercury.Reader(rfid[0])
        #reader.set_region(rfid[1])
        #reader.set_read_plan(rfid[2], rfid[3], read_power=rfid[4])
        #epcs = map(lambda t: t.epc.decode(), reader.read())
        #tags = list(epcs)
        #tagsString = tagToString(tags)
        clientSocket.send(bytes(tags[0], 'utf-8'))
    elif (data[0] == 'autorama/startQualify'):
        readerQualify(restAPI['route'])
    else: 
        return

def post(data):
    dataList = data.split(':')
    if (dataList[0] == 'autorama/rfid/settings'):
        rfid.clear()        
        rfid.append('tmr:'+dataList[1])
        rfid.append(dataList[2])
        rfid.append([int(dataList[3])])
        rfid.append(dataList[4])
        rfid.append(int(dataList[5]))
        print(rfid)
    else: 
        return

while True: 
    clientSocket, address = s.accept()
    print('Conexão estabelecida com: ', address)
    while True:    
        msg = clientSocket.recv(1024)
        methodIdentifier(msg.decode())
        if(msg.decode() == 'q'):
            print('Fechando servidor...')
            s.close()
            break
    break