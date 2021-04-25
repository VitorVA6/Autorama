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
        route = 'GET autorama/startQualify:' + str(d) + ':' + self.piloto1['epc'] + ':' + self.piloto2['epc']
        self.s.send(bytes(route, 'utf-8'))
        msg = self.s.recv(1024).decode()
        msg2 = msg
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
                    if (float(timeLap[2])<float(self.piloto1['bestTime'])):
                        self.piloto1['bestTime'] = timeLap[2]                
                    self.piloto1['time'] = timeLap[2]
                    if (float(self.piloto1['bestTime'])<float(self.piloto2['bestTime'])):
                        self.piloto1['pos'] = '1'
                        self.piloto2['pos'] = '2'

                    print('Piloto: ' + self.piloto1['nome'] + '  Equipe: ' + self.piloto1['equipe'] + \
                    '  Tempo: ' + self.piloto1['time'] + '  Record: ' + self.piloto1['bestTime'] + \
                    '  Voltas: '+str(self.piloto1['voltas'])+'  EPC: ' + self.piloto1['epc'] + \
                    '  Pos: ' + self.piloto1['pos'])
                
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
                    if (float(timeLap[2])<float(self.piloto2['bestTime'])):
                        self.piloto2['bestTime'] = timeLap[2]                    
                    self.piloto2['time'] = timeLap[2]
                    if (float(self.piloto2['bestTime'])<float(self.piloto1['bestTime'])):
                        self.piloto1['pos'] = '2'
                        self.piloto2['pos'] = '1'

                    print('Piloto: ' + self.piloto2['nome'] + '  Equipe: ' + self.piloto2['equipe'] + \
                    '  Tempo: ' + self.piloto2['time'] + '  Record: ' + self.piloto2['bestTime'] + \
                    '  Voltas: '+str(self.piloto2['voltas'])+'  EPC: ' + self.piloto2['epc'] +\
                    '  Pos: ' + self.piloto2['pos'])
                
            elif info[1] == 'q':
                    break
        print('Fim da qualificação')
        return

#Função que recebe nomes de pilotos, busca as tags dos mesmos e preenche esses dados nos dicionários respectivos de
#cada piloto
    def getTagPilot(self, nome, nome2):
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
        file.close()
        linhas.clear()    
#Encerra o server
    def clc(self):        
        self.s.send(bytes('q', 'utf-8'))

#Função responsável por ficar recebendo dados do server e os transformar em informação dos pilotos participantes
# da corrida, até o términio da mesma
    def readerRace(self, v):
        route = 'GET autorama/startRace:' + str(v) + ':' + self.piloto1['epc'] + ':' + self.piloto2['epc']
        self.s.send(bytes(route, 'utf-8'))
        msg = self.s.recv(1024).decode()
        msg2 = msg
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
                    if(self.piloto1['voltas']==self.piloto2['voltas']):
                        if (float(self.piloto1['time'])<float(self.piloto2['time'])):
                            self.piloto1['pos'] = '1'
                            self.piloto2['pos'] = '2'
                        else:
                            self.piloto1['pos'] = '2'
                            self.piloto2['pos'] = '1'
                    elif(self.piloto1['voltas']>self.piloto2['voltas']):
                        self.piloto1['pos'] = '1'
                        self.piloto2['pos'] = '2'
                    else:
                        self.piloto1['pos'] = '2'
                        self.piloto2['pos'] = '1'

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
                    if(self.piloto1['voltas']==self.piloto2['voltas']):
                        if (float(self.piloto1['time'])<=float(self.piloto2['time'])):
                            self.piloto1['pos'] = '1'
                            self.piloto2['pos'] = '2'
                        else:
                            self.piloto1['pos'] = '2'
                            self.piloto2['pos'] = '1'
                    elif(self.piloto1['voltas']>self.piloto2['voltas']):
                        self.piloto1['pos'] = '1'
                        self.piloto2['pos'] = '2'
                    else:
                        self.piloto1['pos'] = '2'
                        self.piloto2['pos'] = '1'


                    print('Piloto: ' + self.piloto2['nome'] + '  Equipe: ' + self.piloto2['equipe'] + \
                    '  Tempo: ' + str(self.piloto2['time']) + \
                    '  Voltas: '+str(self.piloto2['voltas'])+'  EPC: ' + self.piloto2['epc'] +\
                    '  Pos: ' + self.piloto2['pos'])
                
            elif info[1] == 'q':
                    break
        self.piloto1['bestTime']=100
        self.piloto2['bestTime']=100
        print('Fim da Corrida')
        return