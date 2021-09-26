import json

#Classe responsável por realizar os cadastros nos arquivos json.
class api():
#construtor da classe
    def __init__(self):
        self.paises = ['Brasil', 'Alemanha', 'França', 'Itália', 'Estados Unidos', 'Argentina', 'Áustria', 'Austrália', 'Finlândia', 'Inglaterra']
        self.marcas = ['Ford', 'Ferrari', 'McLaren', 'Mercedes', 'Honda', 'Renault', 'BMW', 'Toyota', 'Maserati']
        self.cores = ['Azul', 'Vermelho', 'Preto', 'Branco', 'Amarelo', 'Rosa', 'Cinza', 'Verde']
        self.ativ = ['Ativo', 'Inativo']
        self.ano = list(range(2000, 2020))
        self.anos = str(self.ano)
        self.rec = list(range(30, 150))
        self.rec2 = str(self.rec)
        self.duracao = list(range(1,200))
        self.duracao = str(self.duracao)
 
#Função que recebe os dados do carro e faz o cadastro do mesmo no arquivo cars.json
    def signupCars(self, tag, marca, cor):
        if(cor in self.cores and marca in self.marcas):
            file = open('dataBase/cars.json', 'r')
            linhas = file.readlines()
            data = {'tag': tag, 'marca':marca, 'cor': cor}
            data_s = json.dumps(data)
            linhas.append(data_s + '\n')
            file = open('dataBase/cars.json', 'w')
            file.writelines(linhas)
            file.close()
        else: 
            print('Dados preenchidos incorretamente')

#Função que verifica se já existe um carro com uma determinada tag cadastrado
    def checkCars(self, tag):
        a = False
        file = open('dataBase/cars.json', 'r')
        linhas = file.readlines()
        for linha in linhas:
            b = json.loads(linha)
            if(tag in b['tag']):
                return True
            else:
                a = False
        return a

#Função que recebe dados de um time e faz seu cadastro no arquivo teams.json
    def signupTeams(self, nome, nacionalidade): 
        file = open('dataBase/teams.json', 'r')
        linhas = file.readlines()
        data = {'nome': nome, 'nacionalidade': nacionalidade, 'pontos':0}
        data_s = json.dumps(data)
        linhas.append(data_s + '\n')
        file = open('dataBase/teams.json', 'w')
        file.writelines(linhas)
        file.close()

#Função que cerifica se já existe um time com um determinado nome cadastrado
    def checkTeams(self, nome):
        a = False
        file = open('dataBase/teams.json', 'r')
        linhas = file.readlines()
        for linha in linhas:
            b = json.loads(linha)
            if(nome in b['nome']):
                return True
            else:
                a = False
        return a

#Função que recebe dados de um piloto e faz seu cadastro no arquivo pilots.json
    def signupPilots(self, nome, equipe, carro):
        
        if(equipe != ''):
            file = open('dataBase/teams.json', 'r')
            linhas = file.readlines()
            x = False
            for linha in linhas:
                b = json.loads(linha)
                if(equipe in b['nome']):
                    file.close()
                    linhas.clear()
                    x = True
                else:
                    pass
            if(x == False):
                print('Equipe não existe')
                file.close()
                return

        if(carro != ''):
            file = open('dataBase/cars.json', 'r')
            linhas = file.readlines()
            x = False
            for linha in linhas:
                b = json.loads(linha)
                if(carro in b['tag']):
                    file.close()
                    linhas.clear()
                    x = True
                else:
                    pass
            if(x == False):
                print('Equipe não existe')
                file.close()
                return
  
            file = open('dataBase/pilots.json', 'r')
            linhas = file.readlines()         
            data = {'nome': nome, 'equipe': equipe, 'carro': carro}
            data_s = json.dumps(data)
            linhas.append(data_s + '\n')
            file = open('dataBase/pilots.json', 'w')
            file.writelines(linhas)
            file.close()
        else:
            print('Dados preenchidos incorretamente')
            return

#Função que verifica se já existe um piloto com um determinado nome cadastrado
    def checkPilots(self, nome):
        a = False
        file = open('dataBase/pilots.json', 'r')
        linhas = file.readlines()
        for linha in linhas:
            b = json.loads(linha)
            if(nome in b['nome']):
                return True
            else:
                a = False
        return a
    
#Função retorn os nomes dos pilotos que participarão da partida
    def getPilots(self):
        file = open('dataBase/pilots.json', 'r')
        linhas = file.readlines()
        pilotsList = []
        for linha in linhas:
            b = json.loads(linha)
            pilotsList.append(b['nome'])
        return pilotsList

#Função que retorna uma lista contendo as informações da corrida,
#sendo elas os pilotos, ducaração, numero de voltas e a pista
    def getRaceSettings(self):
        file = open('dataBase/race.json', 'r')
        linhas = file.readlines()
        settings = {'ducarao':'', 'voltas':'', 'piloto1':'', 'piloto2':''}
        for linha in linhas:
            b = json.loads(linha)
            settings['pista'] = b['pista']
            settings['duracao'] = b['duracao']
            settings['voltas'] = b['voltas']
            settings['piloto1'] = b['piloto1']  
            settings['piloto2'] = b['piloto2']
            settings['piloto3'] = b['piloto3']  
            settings['piloto4'] = b['piloto4']     
        file.close()     
        return settings

#Função responsável por receber dados de um circuito e cadastrá-lo
    def signupCircuits(self, nome, pais, recorde):
        if(pais in self.paises and recorde in self.rec2): 
            file = open('dataBase/circuits.json', 'r')
            linhas = file.readlines()
            data = {'nome': nome, 'pais': pais, 'recorde':recorde}
            data_s = json.dumps(data)
            linhas.append(data_s + '\n')
            file = open('dataBase/circuits.json', 'w')
            file.writelines(linhas)
            file.close()
        else:
            print('Preencha os dados corretamente')
            return

#Função que verifica se já existe um circuito com um determinado nome cadastrado
    def checkCircuits(self, nome):
        a = False
        file = open('dataBase/circuits.json', 'r')
        linhas = file.readlines()
        for linha in linhas:
            b = json.loads(linha)
            if(nome in b['nome']):
                return True
            else:
                a = False
        file.close()
        return a

#Função que retorna uma lista contendo os circuitos cadastrados
    def getCircuits(self):
        file = open('dataBase/circuits.json', 'r')
        linhas = file.readlines()
        circuitsList = []
        for linha in linhas:
            b = json.loads(linha)
            circuitsList.append(b['nome'])
        return circuitsList

#Função que recebe os dados de uma corrida e a cadastra
    def signupRaces(self, duracao, voltas, pista, piloto1, piloto2):
        if(pista != ''):
            file = open('dataBase/circuits.json', 'r')
            linhas = file.readlines()
            x = False
            for linha in linhas:
                b = json.loads(linha)
                if(pista in b['nome']):
                    file.close()
                    linhas.clear()
                    x = True
                else:
                    pass
            if(x == False):
                print('Pista não existe')
                file.close()
                return

        if(duracao in self.duracao and voltas in self.duracao):
            data = {'duracao': duracao, 'voltas': voltas, 'pista':pista, 'piloto1': piloto1, 'piloto2':piloto2}
            data_s = json.dumps(data)
            file = open('dataBase/race.json', 'w')
            file.write(data_s)
            file.close()
        else:
            print("Dados incorretos")
            return