import socket 
import time
from datetime import datetime, timedelta
import json

#Essa classe é responsável por estabelecer uma conexão com o server e criar uma forma 
#de comunicação com o mesmo(protocolo)
class client():

#Método construtor
    def __init__(self):
        self.port = ''
        self.host = ''
        self.msg = ''           
        self.piloto1 = {'epc': '','nome': '', 'equipe': '', 'time': 0, 'bestTime': 100, 'pos': '', 'voltas': 0}
        self.piloto2 = {'epc': '','nome': '', 'equipe': '', 'time': 0, 'bestTime': 100, 'pos': '', 'voltas': 0}
        self.piloto3 = {'epc': '','nome': '', 'equipe': '', 'time': 0, 'bestTime': 100, 'pos': '', 'voltas': 0}
        self.piloto4 = {'epc': '','nome': '', 'equipe': '', 'time': 0, 'bestTime': 100, 'pos': '', 'voltas': 0}
        
#Método que se conecta com o server
    def connect(self, porta, ip):
        self.port = int(porta)
        if (ip == ''):
            self.host = socket.gethostname()
        else:
            self.host = ip
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.host, self.port))

#Método que converte tags concatenadas em uma lista de tags
    def stringToTag(self, strn):
        strn = strn.split(':')
        del(strn[-1])
        return strn

#Método que solicita uma leitura das tags
    def get(self):
        self.s.send(bytes('GET autorama/cars:', 'utf-8'))
        msg = self.s.recv(1024).decode()
        tagsList = self.stringToTag(msg)
        return tagsList[0]

#Método que envia para o servidor os dados do RFID
    def post(self, st):
        l = ['POST autorama/rfid/settings']
        l.append(st)
        x = ':'.join(l)
        self.s.send(bytes(x, 'utf-8'))

#Função responsável por ficar recebendo dados do servidor e os transformar em informação dos pilotos participantes
# da qualificatória, até o términio da mesma    
    def readerQualify(self, d):
        qualifyCars = [self.piloto1, self.piloto2, self.piloto3, self.piloto4]
        route = 'GET autorama/startQualify:' + str(d) + ':' + self.piloto1['epc'] + ':' + self.piloto2['epc']+ \
        ':' + self.piloto3['epc'] + ':' + self.piloto4['epc']
        self.s.send(bytes(route, 'utf-8'))
        msg = self.s.recv(1024).decode()
        msg2 = msg
        msg3 = msg
        msg4 = msg
        while True:
            info = self.s.recv(1024).decode().split('/')
            if(info[0] == self.piloto1['epc']):
                self.piloto1['voltas'] = int(info[2])
                if(self.piloto1['voltas'] == 0):
                    pass
                else:    
                    aux = msg.split(':')                
                    msg = info[1]
                    aux2 = msg.split(':')
                    r=timedelta(minutes=float(aux2[1]),seconds=float(aux2[2]))-\
                    timedelta(minutes=float(aux[1]),seconds=float(aux[2]))        
                    timeLap = str(r).split(':')
                    if (float(timeLap[1])*60 + float(timeLap[2]) < float(self.piloto1['bestTime'])):
                        self.piloto1['bestTime'] = float(timeLap[1])*60 + float(timeLap[2])                
                    self.piloto1['time'] = float(timeLap[1])*60 + float(timeLap[2])
                    qualifyCars.sort(key = lambda c: c['bestTime'])
                    qualifyCars[0]['pos']='1'
                    qualifyCars[1]['pos']='2'
                    qualifyCars[2]['pos']='3'
                    qualifyCars[3]['pos']='4'

                    print('Piloto: ' + self.piloto1['nome'] + '  Equipe: ' + self.piloto1['equipe'] + \
                    '  Tempo: ' + str(self.piloto1['time']) + '  Record: ' + str(self.piloto1['bestTime']) + \
                    '  Voltas: '+str(self.piloto1['voltas'])+'  EPC: ' + self.piloto1['epc'] + \
                    '  Pos: ' + str(self.piloto1['pos']))
                
            elif(info[0] == self.piloto2['epc']):
                self.piloto2['voltas'] = int(info[2])
                if(self.piloto2['voltas'] == 0):
                    pass
                else:    
                    aux = msg2.split(':')                
                    msg2 = info[1]
                    aux2 = msg2.split(':')
                    r=timedelta(minutes=float(aux2[1]),seconds=float(aux2[2]))-\
                    timedelta(minutes=float(aux[1]),seconds=float(aux[2]))        
                    timeLap = str(r).split(':')
                    if (float(timeLap[1])*60 + float(timeLap[2]) < float(self.piloto2['bestTime'])):
                        self.piloto2['bestTime'] = float(timeLap[1])*60 + float(timeLap[2])                    
                    self.piloto2['time'] = float(timeLap[1])*60 + float(timeLap[2])
                    qualifyCars.sort(key = lambda c: c['bestTime'])
                    qualifyCars[0]['pos']='1'
                    qualifyCars[1]['pos']='2'
                    qualifyCars[2]['pos']='3'
                    qualifyCars[3]['pos']='4'

                    print('Piloto: ' + self.piloto2['nome'] + '  Equipe: ' + self.piloto2['equipe'] + \
                    '  Tempo: ' + str(self.piloto2['time']) + '  Record: ' + str(self.piloto2['bestTime']) + \
                    '  Voltas: '+str(self.piloto2['voltas'])+'  EPC: ' + self.piloto2['epc'] +\
                    '  Pos: ' + str(self.piloto2['pos']))
            elif(info[0] == self.piloto3['epc']):
                self.piloto3['voltas'] = int(info[2])
                if(self.piloto3['voltas'] == 0):
                    pass
                else:    
                    aux = msg3.split(':')                
                    msg3 = info[1]
                    aux2 = msg3.split(':')
                    r=timedelta(minutes=float(aux2[1]),seconds=float(aux2[2]))-\
                    timedelta(minutes=float(aux[1]),seconds=float(aux[2]))        
                    timeLap = str(r).split(':')
                    if (float(timeLap[1])*60 + float(timeLap[2]) < float(self.piloto3['bestTime'])):
                        self.piloto3['bestTime'] = float(timeLap[1])*60 + float(timeLap[2])                    
                    self.piloto3['time'] = float(timeLap[1])*60 + float(timeLap[2])
                    qualifyCars.sort(key = lambda c: c['bestTime'])
                    qualifyCars[0]['pos']='1'
                    qualifyCars[1]['pos']='2'
                    qualifyCars[2]['pos']='3'
                    qualifyCars[3]['pos']='4'

                    print('Piloto: ' + self.piloto3['nome'] + '  Equipe: ' + self.piloto3['equipe'] + \
                    '  Tempo: ' + str(self.piloto3['time']) + '  Record: ' + str(self.piloto3['bestTime']) + \
                    '  Voltas: '+str(self.piloto3['voltas'])+'  EPC: ' + self.piloto3['epc'] +\
                    '  Pos: ' + str(self.piloto3['pos']))    

            elif(info[0] == self.piloto4['epc']):
                self.piloto4['voltas'] = int(info[2])
                if(self.piloto4['voltas'] == 0):
                    pass
                else:    
                    aux = msg4.split(':')                
                    msg4 = info[1]
                    aux2 = msg4.split(':')
                    r=timedelta(minutes=float(aux2[1]),seconds=float(aux2[2]))-\
                    timedelta(minutes=float(aux[1]),seconds=float(aux[2]))        
                    timeLap = str(r).split(':')
                    if (float(timeLap[1])*60 + float(timeLap[2]) < float(self.piloto4['bestTime'])):
                        self.piloto4['bestTime'] = float(timeLap[1])*60 + float(timeLap[2])                    
                    self.piloto4['time'] = float(timeLap[1])*60 + float(timeLap[2])
                    qualifyCars.sort(key = lambda c: c['bestTime'])
                    qualifyCars[0]['pos']='1'
                    qualifyCars[1]['pos']='2'
                    qualifyCars[2]['pos']='3'
                    qualifyCars[3]['pos']='4'

                    print('Piloto: ' + self.piloto4['nome'] + '  Equipe: ' + self.piloto4['equipe'] + \
                    '  Tempo: ' + str(self.piloto4['time']) + '  Record: ' + str(self.piloto4['bestTime']) + \
                    '  Voltas: '+str(self.piloto4['voltas'])+'  EPC: ' + self.piloto4['epc'] +\
                    '  Pos: ' + str(self.piloto4['pos']))    
            
            elif info[1] == 'q':
                    break
        print('Fim da qualificação')
        return

#Função que recebe nomes de pilotos, busca as tags dos mesmos e preenche esses dados nos dicionários respectivos de
#cada piloto
    def getTagPilot(self, nome, nome2, nome3, nome4):
        file = open('dataBase/pilots.json', 'r')
        linhas = file.readlines()
        for linha in linhas:
            b = json.loads(linha)
            if(nome in b['nome']):
                self.piloto1['nome'] = nome
                self.piloto1['epc'] = b['carro']
                self.piloto1['equipe'] = b['equipe']   
            elif(nome2 in b['nome']):
                self.piloto2['nome'] = nome2
                self.piloto2['epc'] = b['carro']
                self.piloto2['equipe'] = b['equipe']
            elif(nome3 in b['nome']):
                self.piloto3['nome'] = nome3
                self.piloto3['epc'] = b['carro']
                self.piloto3['equipe'] = b['equipe']
            elif(nome4 in b['nome']):
                self.piloto4['nome'] = nome4
                self.piloto4['epc'] = b['carro']
                self.piloto4['equipe'] = b['equipe']
        file.close()
        linhas.clear()    
#Encerra o server
    def clc(self):        
        self.s.send(bytes('q', 'utf-8'))

#Função responsável por ficar recebendo dados do server e os transformar em informação dos pilotos participantes
# da corrida, até o términio da mesma
    def readerRace(self, v):
        route = 'GET autorama/startRace:' + str(v) + ':' + self.piloto1['epc'] + ':' + self.piloto2['epc'] +\
        ':' + self.piloto3['epc'] + ':' + self.piloto4['epc']
        self.s.send(bytes(route, 'utf-8'))
        msg = self.s.recv(1024).decode()
        msg2 = msg
        msg3 = msg
        msg4 = msg
        while True:
            info = self.s.recv(1024).decode().split('/')
            if(info[0] == self.piloto1['epc']):
                self.piloto1['voltas'] = int(info[2])
                if(self.piloto1['voltas'] == 0):
                    pass
                else:
                    aux = msg.split(':')                
                    msg = info[1]
                    aux2 = msg.split(':')
                    r=timedelta(minutes=float(aux2[1]),seconds=float(aux2[2]))-\
                    timedelta(minutes=float(aux[1]),seconds=float(aux[2]))        
                    timeLap = str(r).split(':')          
                    self.piloto1['time'] += float(timeLap[2])

                    print('Piloto: ' + self.piloto1['nome'] + '  Equipe: ' + self.piloto1['equipe'] + \
                    '  Tempo: ' + str(self.piloto1['time']) + \
                    '  Voltas: '+str(self.piloto1['voltas'])+'  EPC: ' + self.piloto1['epc'] + \
                    '  Pos: ' + self.piloto1['pos'])
                
            elif(info[0] == self.piloto2['epc']):
                self.piloto2['voltas'] = int(info[2])
                if(self.piloto2['voltas']==0):
                    pass
                else:    
                    aux = msg2.split(':')                
                    msg2 = info[1]
                    aux2 = msg2.split(':')
                    r=timedelta(minutes=float(aux2[1]),seconds=float(aux2[2]))-\
                    timedelta(minutes=float(aux[1]),seconds=float(aux[2]))        
                    timeLap = str(r).split(':')
                    self.piloto2['time'] += float(timeLap[2])

                    print('Piloto: ' + self.piloto2['nome'] + '  Equipe: ' + self.piloto2['equipe'] + \
                    '  Tempo: ' + str(self.piloto2['time']) + \
                    '  Voltas: '+str(self.piloto2['voltas'])+'  EPC: ' + self.piloto2['epc'] +\
                    '  Pos: ' + self.piloto2['pos'])

            if(info[0] == self.piloto3['epc']):
                self.piloto3['voltas'] = int(info[2])
                if(self.piloto3['voltas'] == 0):
                    pass
                else:
                    aux = msg3.split(':')                
                    msg3 = info[1]
                    aux2 = msg3.split(':')
                    r=timedelta(minutes=float(aux2[1]),seconds=float(aux2[2]))-\
                    timedelta(minutes=float(aux[1]),seconds=float(aux[2]))        
                    timeLap = str(r).split(':')          
                    self.piloto3['time'] += float(timeLap[2])

                    print('Piloto: ' + self.piloto3['nome'] + '  Equipe: ' + self.piloto3['equipe'] + \
                    '  Tempo: ' + str(self.piloto3['time']) + \
                    '  Voltas: '+str(self.piloto3['voltas'])+'  EPC: ' + self.piloto3['epc'] + \
                    '  Pos: ' + self.piloto3['pos'])
                
            elif(info[0] == self.piloto4['epc']):
                self.piloto4['voltas'] = int(info[2])
                if(self.piloto4['voltas']==0):
                    pass
                else:    
                    aux = msg4.split(':')                
                    msg4 = info[1]
                    aux2 = msg4.split(':')
                    r=timedelta(minutes=float(aux2[1]),seconds=float(aux2[2]))-\
                    timedelta(minutes=float(aux[1]),seconds=float(aux[2]))        
                    timeLap = str(r).split(':')
                    self.piloto4['time'] += float(timeLap[2])

                    print('Piloto: ' + self.piloto4['nome'] + '  Equipe: ' + self.piloto4['equipe'] + \
                    '  Tempo: ' + str(self.piloto4['time']) + \
                    '  Voltas: '+str(self.piloto4['voltas'])+'  EPC: ' + self.piloto4['epc'] +\
                    '  Pos: ' + self.piloto4['pos'])

            elif info[1] == 'q':
                    break
        self.piloto1['bestTime']=100
        self.piloto2['bestTime']=100
        self.piloto3['bestTime']=100
        self.piloto4['bestTime']=100
        print('Fim da Corrida')
        return