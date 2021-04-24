import socket
import time
from datetime import datetime, timedelta
import _thread as thread
#import mercury

tags = []
rfid = []
raceTags = []
tagBuffer = []
restAPI = {'method':'', 'route':''}
r = True

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 5022))
s.listen(5)

def addBufferRace(carro, tempo, volta):
    tagBuffer.append({'tag':carro, 'time': tempo, 'sent':'false', 'volta': volta})
    raceTags.append(carro)
    print('adicionado1')
    print(tagBuffer, raceTags)

def readerThreadRfid(voltas):
    voltaCarro1 = -1
    voltaCarro2 = -1
    c=0
    while (r):
        if(tags[0] not in raceTags):
            voltaCarro1+=1
            thread.start_new_thread(addBufferRace, ('carro1', datetime.fromtimestamp(time.time()), voltaCarro1))
        if(tags[1] not in raceTags):
            voltaCarro2+=1
            thread.start_new_thread(addBufferRace, ('carro2', datetime.fromtimestamp(time.time()), voltaCarro2))
        time.sleep(0.1)
        c+=1
    print('Thread encerrada')
    return

def readerRace(data):
    global r
    t = 0
    dataList = data.split(':')    
    tags.append(dataList[2])
    tags.append(dataList[3])
    info = str(datetime.fromtimestamp(time.time()))
    clientSocket.send(bytes(info, 'utf-8'))
    thread.start_new_thread(readerThreadRfid, (int(dataList[1]),))
    while True: 
        time.sleep(0.2)
        if(len(tagBuffer)>0 and tagBuffer[0]['sent'] == 'false'):
            info =  raceTags[0]+ '/'+ str(tagBuffer[0]['time']) + '/' + str(tagBuffer[0]['volta'])
            clientSocket.send(bytes(info, 'utf-8')) 
            print('enviado1')
            tagBuffer[0]['sent'] = 'true'
        time.sleep(0.3)
        if(len(tagBuffer)>1 and tagBuffer[1]['sent'] == 'false'):
            info =  raceTags[1]+ '/'+ str(tagBuffer[1]['time']) + '/' + str(tagBuffer[1]['volta'])
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
        
        if (len(tagBuffer)>1):
            if(tagBuffer[0]['volta']>=int(dataList[1]) and tagBuffer[1]['volta']>=int(dataList[1])):
                r = False
                break
    tags.clear()
    clientSocket.send(bytes('q/q', 'utf-8'))
    return

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

def addBuffer(carro, tempo, volta):
    tagBuffer.append({'tag':carro, 'time': tempo, 'sent':'false', 'volta':volta})
    raceTags.append(carro)
    print('adicionado1')
    print(tagBuffer, raceTags)

def readerThread(tempo):
    c=0
    voltaCarro1 = -1
    voltaCarro2 = -1
    while c<tempo*10:
        if(tags[0] not in raceTags):
            voltaCarro1+=1
            thread.start_new_thread(addBuffer, ('carro1', datetime.fromtimestamp(time.time()), str(voltaCarro1)))
        if(tags[1] not in raceTags):
            voltaCarro2+=1
            thread.start_new_thread(addBuffer, ('carro2', datetime.fromtimestamp(time.time()), str(voltaCarro2)))
        time.sleep(0.1)
        c+=1
    print('Thread encerrada')
    return

def readerQualify(data):
    t = 0
    dataList = data.split(':')    
    tags.append(dataList[2])
    tags.append(dataList[3])
    info = str(datetime.fromtimestamp(time.time()))
    clientSocket.send(bytes(info, 'utf-8'))
    thread.start_new_thread(readerThread, (int(dataList[1]),))
    while t<int(dataList[1]): 
        time.sleep(0.1)
        if(len(tagBuffer)>0 and tagBuffer[0]['sent'] == 'false'):
            info =  raceTags[0]+ '/'+ str(tagBuffer[0]['time'])+ '/'+ tagBuffer[0]['volta']
            clientSocket.send(bytes(info, 'utf-8')) 
            print('enviado1')
            tagBuffer[0]['sent'] = 'true'
        time.sleep(0.3)
        if(len(tagBuffer)>1 and tagBuffer[1]['sent'] == 'false'):
            info =  raceTags[1]+ '/'+ str(tagBuffer[1]['time'])+ '/'+ tagBuffer[1]['volta']
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
    tags.clear()
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
    elif (data[0] == 'autorama/startRace'):
        readerRace(restAPI['route'])
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