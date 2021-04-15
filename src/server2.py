import socket
import time
from datetime import datetime, timedelta
import _thread as thread
import mercury

tags = ['E20000172211013118905493', 'E2000017221101241890547C']
rfid = []
raceTags = []
tagBuffer = []

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 5024))
s.listen(5)

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

def tagFilter(tag, tempo):
    if(tag not in raceTags and tag in tags):
        tagBuffer.append({'tag':tag, 'time': tempo, 'sent':'false'})
        raceTags.append(tag)
        print('adicionou tag' + tag)
        print(tagBuffer, raceTags)    

def readerThread():
    reader = mercury.Reader("tmr:///dev/ttyUSB0", baudrate=230400)
    reader.set_region("NA2")
    reader.set_read_plan([1], "GEN2", read_power=1500)
    reader.start_reading(lambda tag: tagFilter(tag.epc.decode(), datetime.fromtimestamp(tag.timestamp)))
    time.sleep(20)

def readerQualify(data):
    t = 0
    dataList = data.split(':')
    if(dataList[0] == 'startQualify'):
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
    else:    
        return


def get(data):
    global tags
    if (data =='autorama/cars'):
        #reader = mercury.Reader(rfid[0])
        #reader.set_region(rfid[1])
        #reader.set_read_plan(rfid[2], rfid[3], read_power=rfid[4])
        #epcs = map(lambda t: t.epc.decode(), reader.read())
        #tags = list(epcs)
        #tagsString = tagToString(tags)
        clientSocket.send(bytes(tags[0], 'utf-8'))
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
        get(msg.decode())
        post(msg.decode())
        readerQualify(msg.decode())
        if(msg.decode() == 'q'):
            print('Fechando servidor...')
            s.close()
            break
    break