import socket 
import time
from datetime import datetime, timedelta
import json

class client():

    def __init__(self):
        self.port = ''
        self.host = ''
        self.msg = ''           
        self.piloto1 = {'epc': '','nome': '', 'equipe': '', 'time': 100, 'bestTime': 100, 'pos': '', 'voltas': 0}
        self.piloto2 = {'epc': '','nome': '', 'equipe': '', 'time': 100, 'bestTime': 100, 'pos': '', 'voltas': 0}
        

    def connect(self, porta, ip):
        self.port = int(porta)
        if (ip == ''):
            self.host = socket.gethostname()
        else:
            self.host = ip
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.host, self.port))

    def stringToTag(self, strn):
        strn = strn.split(':')
        del(strn[-1])
        return strn

    def get(self):
        self.s.send(bytes('autorama/cars', 'utf-8'))
        msg = self.s.recv(1024).decode()
        #tagsList = self.stringToTag(msg)
        return msg

    def post(self, st):
        l = ['autorama/rfid/settings']
        l.append(st)
        x = ':'.join(l)
        self.s.send(bytes(x, 'utf-8'))
    
    def readerQualify(self):
        self.s.send(bytes('startQualify:21', 'utf-8'))
        msg = self.s.recv(1024).decode()
        msg2 = msg
        while True:
            info = self.s.recv(1024).decode().split('/')
            if(info[0] == self.piloto1['epc']):
                if(self.piloto1['voltas'] == 0):
                    self.piloto1['voltas'] +=1
                    msg = info[1]
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
                    self.piloto1['voltas'] += 1
                
            elif(info[0] == self.piloto2['epc']):
                if(self.piloto2['voltas']==0):
                    self.piloto2['voltas'] +=1
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
                    self.piloto2['voltas'] += 1
                
            elif info[1] == 'q':
                    break
        
        self.piloto1 = {'epc': '','nome': '', 'equipe': '', 'time': '', 'bestTime': 100.5, 'pos': '', 'voltas': 0}
        self.piloto2 = {'epc': '','nome': '', 'equipe': '', 'time': '', 'bestTime': 100.5, 'pos': '', 'voltas': 0}
        print('Fim da qualificação')
        return

    def getTagPilot(self, nome, nome2):
        file = open('pilots.json', 'r')
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
    
    def clc(self):        
        self.s.send(bytes('q', 'utf-8'))