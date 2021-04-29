import socket
import time
from datetime import datetime, timedelta
import _thread as thread
import mercury

#Variáveis globais responsáveis por armazenar informações das tags da corrida, configurações do RFID,
#dados do protocolo rest, além de variáveis de controle de laçoes while
tags = []
rfid = []
raceTags = []
tagBuffer = []
restAPI = {'method':'', 'route':''}
reader = True
voltaCarro1 = -1
voltaCarro2 = -1    
voltaCarro3 = -1
voltaCarro4 = -1    

#Instância do server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 5024))
s.listen(5)

#Adiciona dados de um determinado carro ao buffer
def addBufferRace(carro, tempo, volta):
    tagBuffer.append({'tag':carro, 'time': tempo, 'sent':'false', 'volta': volta})
    raceTags.append(carro)
    print('adicionado1')
    print(tagBuffer, raceTags)

#Função que ordena o raspberry realizar leituras consecutivas em um daterminado intervalo de tempo
def readerThreadRfid():
    global reader
    reader = mercury.Reader(rfid[0], baudrate=rfid[5])
    reader.set_region(rfid[1])
    reader.set_read_plan(rfid[2], rfid[3], read_power=rfid[4])
    reader.start_reading(lambda tag: tagFilter(tag.epc.decode(), datetime.fromtimestamp(tag.timestamp)))
    time.sleep(40)    
    print('Thread encerrada')
    return

#Função que vai enviar para o cliente dados obtidos pelo leito periodicamente,
#sendo o consumidor da corrida
def readerRace(data):
    global reader
    global voltaCarro1
    global voltaCarro2
    global voltaCarro3
    global voltaCarro4
    voltaCarro1 = -1
    voltaCarro2 = -1
    voltaCarro3 = -1
    voltaCarro4 = -1
    dataList = data.split(':')    
    tags.append(dataList[2])
    tags.append(dataList[3])
    tags.append(dataList[4])
    tags.append(dataList[5])
    info = str(datetime.fromtimestamp(time.time()))
    clientSocket.send(bytes(info, 'utf-8'))
    #inicia a thread do produtor
    thread.start_new_thread(readerThreadRfid, ())
    #esse looping aliado aos 'ifs', realiza a remoção de dados do buffer a partir do tempo mínimo da volta
    # além de realizar envios dos dados 
    while True: 
        time.sleep(0.2)
        if(len(tagBuffer)>0 and tagBuffer[0]['sent'] == 'false'):
            info =  raceTags[0]+ '/'+ str(tagBuffer[0]['time']) + '/' + str(tagBuffer[0]['volta'])
            clientSocket.send(bytes(info, 'utf-8')) 
            print('enviado1')
            tagBuffer[0]['sent'] = 'true'
        time.sleep(0.1)
        if(len(tagBuffer)>1 and tagBuffer[1]['sent'] == 'false'):
            info =  raceTags[1]+ '/'+ str(tagBuffer[1]['time']) + '/' + str(tagBuffer[1]['volta'])
            clientSocket.send(bytes(info, 'utf-8')) 
            print('enviado2')
            tagBuffer[1]['sent'] = 'true'
        time.sleep(0.1)
        if(len(tagBuffer)>2 and tagBuffer[2]['sent'] == 'false'):
            info =  raceTags[2]+ '/'+ str(tagBuffer[2]['time'])+ '/'+ str(tagBuffer[2]['volta'])
            clientSocket.send(bytes(info, 'utf-8')) 
            print('enviado3')
            tagBuffer[2]['sent'] = 'true'  
        time.sleep(0.1)
        if(len(tagBuffer)>3 and tagBuffer[3]['sent'] == 'false'):
            info =  raceTags[3]+ '/'+ str(tagBuffer[3]['time'])+ '/'+ str(tagBuffer[3]['volta'])
            clientSocket.send(bytes(info, 'utf-8')) 
            print('enviado4')
            tagBuffer[3]['sent'] = 'true'
        
        if (len(tagBuffer)>0):
            time1 = datetime.fromtimestamp(time.time()) - tagBuffer[0]['time']
            time2 = timedelta(seconds = 6)
            if(time1 > time2):
                del(tagBuffer[0])
                del(raceTags[0])
                print('deletado')
        
        if (len(tagBuffer)>3):
            if(tagBuffer[0]['volta']>=int(dataList[1]) and tagBuffer[1]['volta']>=int(dataList[1])and\
                tagBuffer[2]['volta']>=int(dataList[1]) and tagBuffer[3]['volta']>=int(dataList[1])):
                reader.stop_reading()
                break
    tags.clear()
    clientSocket.send(bytes('q/q', 'utf-8'))
    return

#Método que identifica se a requisição feita pelo cliente é um GET ou um POST,
#lém de identificar a url e armazenar esses dados num dicionário
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

#Adiciona dados de um determinado carro ao buffer, durante a qualificatória e a corrida
def addBuffer(carro, tempo, volta):
    tagBuffer.append({'tag':carro, 'time': tempo, 'sent':'false', 'volta':volta})
    raceTags.append(carro)
    print('adicionado1')
    print(tagBuffer, raceTags)

#Função responsável por filtras quais tags e quando as tags devem ser armazenadas no buffer,
#inicia threads para realizar o preenchimento do buffer, pra o consumidor focar apenas na leitura das tags
def tagFilter(tag, tempo):
    global voltaCarro1
    global voltaCarro2
    global voltaCarro3
    global voltaCarro4
    if(tag not in raceTags and tag == tags[0]):
        voltaCarro1+=1
        tagBuffer.append({'tag':tags[0], 'time': tempo, 'sent':'false', 'volta':voltaCarro1})
        raceTags.append(tags[0])
        print('adicionado1')
        print(tagBuffer, raceTags)
    if(tag not in raceTags and tag == tags[1]):
        voltaCarro2+=1
        tagBuffer.append({'tag':tags[1], 'time': tempo, 'sent':'false', 'volta':voltaCarro2})
        raceTags.append(tags[1])
        print('adicionado1')
        print(tagBuffer, raceTags)
    if(tag not in raceTags and tag == tags[2]):
        voltaCarro3+=1
        tagBuffer.append({'tag':tags[2], 'time': tempo, 'sent':'false', 'volta':voltaCarro3})
        raceTags.append(tags[2])
        print('adicionado1')
        print(tagBuffer, raceTags)
    if(tag not in raceTags and tag == tags[3]):
        voltaCarro4+=1
        tagBuffer.append({'tag':tags[3], 'time': tempo, 'sent':'false', 'volta':voltaCarro4})
        raceTags.append(tags[3])
        print('adicionado1')
        print(tagBuffer, raceTags)


#Função que recebe o tempo de duração da qualificatória como parâmetro, instancia o leitor
# e realiza leituras consecutivas até o fim da qualificatória
def readerThread(tempo):    
    reader = mercury.Reader(rfid[0], baudrate=rfid[5])
    reader.set_region(rfid[1])
    reader.set_read_plan(rfid[2], rfid[3], read_power=rfid[4])
    reader.start_reading(lambda tag: tagFilter(tag.epc.decode(), datetime.fromtimestamp(tag.timestamp)))
    time.sleep(tempo)
    reader.stop_reading()

#Função idêntica ao Consumidor da corrida, explicado acima
def readerQualify(data):
    global voltaCarro1
    global voltaCarro2
    global voltaCarro3
    global voltaCarro4
    voltaCarro1 = -1
    voltaCarro2 = -1
    voltaCarro3 = -1
    voltaCarro4 = -1
    t = 0
    dataList = data.split(':')    
    tags.append(dataList[2])
    tags.append(dataList[3])
    tags.append(dataList[4])
    tags.append(dataList[5])
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
        time.sleep(0.1)
        if(len(tagBuffer)>1 and tagBuffer[1]['sent'] == 'false'):
            info =  raceTags[1]+ '/'+ str(tagBuffer[1]['time'])+ '/'+ str(tagBuffer[1]['volta'])
            clientSocket.send(bytes(info, 'utf-8')) 
            print('enviado2')
            tagBuffer[1]['sent'] = 'true'
        time.sleep(0.1)
        if(len(tagBuffer)>2 and tagBuffer[2]['sent'] == 'false'):
            info =  raceTags[2]+ '/'+ str(tagBuffer[2]['time'])+ '/'+ str(tagBuffer[2]['volta'])
            clientSocket.send(bytes(info, 'utf-8')) 
            print('enviado3')
            tagBuffer[2]['sent'] = 'true'  
        time.sleep(0.1)      
        if(len(tagBuffer)>3 and tagBuffer[3]['sent'] == 'false'):
            info =  raceTags[3]+ '/'+ str(tagBuffer[3]['time'])+ '/'+ str(tagBuffer[3]['volta'])
            clientSocket.send(bytes(info, 'utf-8')) 
            print('enviado4')
            tagBuffer[3]['sent'] = 'true'
        
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


#Função responsável por gerenciar as funções pertencentes ao método GET, sempre que o cliente enviar 
#uma requisição get, essa função será chamada e determinará qual ação tomar a depender a url
def get(data):
    global tags
    global restAPI
    data = data.split(':')
    if (data[0] =='autorama/cars'):
        reader = mercury.Reader(rfid[0])
        reader.set_region(rfid[1])
        reader.set_read_plan(rfid[2], rfid[3], read_power=rfid[4])
        epcs = map(lambda t: t.epc.decode(), reader.read())
        tag = list(epcs)
        tagsString = tagToString(tag)
        clientSocket.send(bytes(tags[0], 'utf-8'))
    elif (data[0] == 'autorama/startQualify'):
        readerQualify(restAPI['route'])
    elif (data[0] == 'autorama/startRace'):
        readerRace(restAPI['route'])
    else: 
        return

#Função que gerencia as requisições POST, no entanto só existe uma no server
def post(data):
    dataList = data.split(':')
    if (dataList[0] == 'autorama/rfid/settings'):
        rfid.clear()        
        rfid.append('tmr:'+dataList[1])
        rfid.append(dataList[2])
        rfid.append([int(dataList[3])])
        rfid.append(dataList[4])
        rfid.append(int(dataList[5]))
        rfid.append(int(dataList[6]))
        print(rfid)
    else: 
        return

#Looping principal do server, responsável por aguardar um cliente se conectar
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