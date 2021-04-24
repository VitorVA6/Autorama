import socket
import time
from datetime import datetime, timedelta
import _thread as thread
import mercury

tags = []
rfid = []
raceTags = []
tagBuffer = []
restAPI = {'method':'', 'route':''}
r = True
voltaCarro1 = -1
voltaCarro2 = -1    

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 5024))
s.listen(5)

def addBufferRace(carro, tempo, volta):
    tagBuffer.append({'tag':carro, 'time': tempo, 'sent':'false', 'volta': volta})
    raceTags.append(carro)
    print('adicionado1')
    print(tagBuffer, raceTags)

def readerThreadRfid():
    global reader
    reader = mercury.Reader("tmr:///dev/ttyUSB0", baudrate=230400)
    reader.set_region("NA2")
    reader.set_read_plan([1], "GEN2", read_power=1500)
    reader.start_reading(lambda tag: tagFilter(tag.epc.decode(), datetime.fromtimestamp(tag.timestamp)))
    time.sleep(40)    
    print('Thread encerrada')
    return

def readerRace(data):
    global voltaCarro1
    global voltaCarro2
    voltaCarro1 = -1
    voltaCarro2 = -1
    dataList = data.split(':')    
    tags.append(dataList[2])
    tags.append(dataList[3])
    info = str(datetime.fromtimestamp(time.time()))
    clientSocket.send(bytes(info, 'utf-8'))
    thread.start_new_thread(readerThreadRfid, ())
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
                reader.stop_reading()
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


def decode():
    tags2 = []
    for t in tags:
        tags2.append(t.decode())
    return tags2

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


def tagFilter(tag, tempo):
    global voltaCarro1
    global voltaCarro2
    if(tag not in raceTags and tag == tags[0]):
        voltaCarro1+=1
        addBuffer(tags[0], tempo, voltaCarro1)
    if(tag not in raceTags and tag == tags[1]):
        voltaCarro2+=1
        addBuffer(tags[1], tempo, voltaCarro2)  

def readerThread(tempo):    
    reader = mercury.Reader("tmr:///dev/ttyUSB0", baudrate=230400)
    reader.set_region("NA2")
    reader.set_read_plan([1], "GEN2", read_power=1500)
    reader.start_reading(lambda tag: tagFilter(tag.epc.decode(), datetime.fromtimestamp(tag.timestamp)))
    time.sleep(tempo)
    reader.stop_reading()

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
            info =  raceTags[0]+ '/'+ str(tagBuffer[0]['time'])+ '/'+ str(tagBuffer[0]['volta'])
            clientSocket.send(bytes(info, 'utf-8')) 
            print('enviado1')
            tagBuffer[0]['sent'] = 'true'
        time.sleep(0.3)
        if(len(tagBuffer)>1 and tagBuffer[1]['sent'] == 'false'):
            info =  raceTags[1]+ '/'+ str(tagBuffer[1]['time'])+ '/'+ str(tagBuffer[1]['volta'])
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