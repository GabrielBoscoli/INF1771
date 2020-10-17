# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 13:00:32 2020

@author: Gabriel Boscoli

Módulo responsável pelo simulated annealing
"""

from random import choice, uniform, randint
from math import exp
import copy

NOME_CAVALEIROS = ['Seya', 'Ikki', 'Shiryu', 'Hyoga', 'Shun']

MIN_CAVALEIROS_CASA = 1
MAX_CAVALEIROS_CASA = 5

# Poder cosmico default
PODER_COSMICO = { 'Seya': 1.5, 'Ikki': 1.4, 'Shiryu': 1.3, 'Hyoga': 1.2, 'Shun': 1.1 }

# Quantidade de cavaleiros
CAVALEIROS = 5

# Numero de vidas de cada cavaleiro
VIDA = 5

# Numero de casas do zodiaco
CASAS_DO_ZODIACO = 12

def setPoderCosmico(poderCosmico):
    global PODER_COSMICO
    PODER_COSMICO = poderCosmico
    
def solucaoValida(cavaleiros):
    maximo_cavaleiros = MAX_CAVALEIROS_CASA * VIDA
    qntd_cavaleiros = 0
    for i in range(len(cavaleiros)):
        if len(cavaleiros[i]) < 1:
            return False;
        qntd_cavaleiros += len(cavaleiros[i])
    if qntd_cavaleiros < maximo_cavaleiros:
        return True
    return False

def geraEstadoInicial(cavaleiros, cavaleiros_faltando):    
    # coloca todos os cavaleiros em uma casa, matando todos eles
    index_casa = 0
    for i in range(CAVALEIROS):
        for j in range(VIDA):
            cavaleiro = NOME_CAVALEIROS[i]
            cavaleiros[index_casa % CASAS_DO_ZODIACO].append(cavaleiro)
            cavaleiros_faltando[cavaleiro] -= 1
            index_casa += 1
            
    print(cavaleiros)
            
    # salva aleatoriamente um cavaleiro
    cavaleiro_salvo = NOME_CAVALEIROS[randint(0, CAVALEIROS)]
    casas_com_cavaleiro = []
    for i in range(CASAS_DO_ZODIACO):
        if cavaleiro_salvo in cavaleiros[i] and len(cavaleiros[i]) > 1:
            casas_com_cavaleiro.append(i)
    cavaleiros[choice(casas_com_cavaleiro)].remove(cavaleiro_salvo)

def trocaCasas(cavaleiros):
    casa1 = randint(0,len(cavaleiros))
    casa2 = randint(0,len(cavaleiros))
    cavaleiros[casa1], cavaleiros[casa2] = cavaleiros[casa2], cavaleiros[casa1]
    
def shiftaCavaleiros(cavaleiros):
    fileira = randint(0, 3)
    primeiro_cavaleiro = None
    # salva o cavaleiro da fileira da primeira casa
    if fileira < len(cavaleiros[0]):
        primeiro_cavaleiro = cavaleiros[0][fileira]
        cavaleiros[0].remove(primeiro_cavaleiro)   
    # para todos os outros cavaleiros
    for i in range(1, len(cavaleiros)):
        if fileira < len(cavaleiros[i]):
            cavaleiro_removido = cavaleiros[i][fileira]
            cavaleiros[i].remove(cavaleiro_removido)
            # procura casa anterior que nao tem o caveleiro que foi removido e o adiciona
            for j in range(1, CASAS_DO_ZODIACO):
                    if cavaleiro_removido not in cavaleiros[(i - j) % CASAS_DO_ZODIACO]:
                        cavaleiros[(i - j) % CASAS_DO_ZODIACO].append(cavaleiro_removido)
    # se tem primeiro cavaleiro
    for i in range(CASAS_DO_ZODIACO):
        if primeiro_cavaleiro not in cavaleiros[(i - j) % CASAS_DO_ZODIACO]:
            cavaleiros[(i - j) % CASAS_DO_ZODIACO].append(primeiro_cavaleiro)

def trocaCavaleiro(cavaleiros, cavaleiros_faltando):
    cavaleiro1 = NOME_CAVALEIROS[randint(0,len(NOME_CAVALEIROS))]
    casas_sem_cavaleiro1 = []
    casas_com_cavaleiro1 = []
    # acha casa que nao tem o cavaleiro
    for i in range(len(cavaleiros)):
        if cavaleiro1 not in cavaleiros[i]:
            casas_sem_cavaleiro1.append(i)
        else:
            casas_com_cavaleiro1.append(i)
            
    cavaleiro2 = NOME_CAVALEIROS[randint(0,len(NOME_CAVALEIROS))]
    casas_sem_cavaleiro2 = []
    casas_com_cavaleiro2 = []
    # acha casa que nao tem o cavaleiro
    for i in range(len(cavaleiros)):
        if cavaleiro2 not in cavaleiros[i]:
            casas_sem_cavaleiro2.append(i)
        else:
            casas_com_cavaleiro2.append(i)
            
    casa_sem_cavaleiro1 = choice(casas_sem_cavaleiro1)
    casa_sem_cavaleiro2 = choice(casas_sem_cavaleiro2)
    casa_com_cavaleiro1 = choice(casas_com_cavaleiro1)
    casa_com_cavaleiro2 = choice(casas_com_cavaleiro2)
    
    # remove cavaleiro 1 da sua casa original e insere na nova
    cavaleiros[casa_com_cavaleiro1].remove(cavaleiro1)
    cavaleiros[casa_sem_cavaleiro1].append(cavaleiro1)
    # remove cavaleiro 2 da sua casa original e insere na nova
    cavaleiros[casa_com_cavaleiro2].remove(cavaleiro2)
    cavaleiros[casa_sem_cavaleiro2].append(cavaleiro2)
    
    # verificar se essa vizinhança preserva o maximo e o minimo de cavaleiros
    
def trocaCavaleiroVivo(cavaleiros, cavaleiros_faltando):
    cavaleiro_vivo = None
    # pega o cavaleiro que está vivo
    for i in range(NOME_CAVALEIROS):
        if cavaleiros_faltando[NOME_CAVALEIROS[i]] > 0:
            cavaleiro_vivo = NOME_CAVALEIROS[i]
    
    # escolhe cavaleiro para viver
    cavaleiro_viver = NOME_CAVALEIROS[randint(0,len(NOME_CAVALEIROS))]
    while(cavaleiro_viver == cavaleiro_vivo):
        cavaleiro_viver = NOME_CAVALEIROS[randint(0,len(NOME_CAVALEIROS))]
    
    casas_com_cavaleiro = []
    for i in range(len(cavaleiros)):
        if cavaleiro_viver in cavaleiros[i]:
            casas_com_cavaleiro.append(i)
    
    casa_com_cavaleiro = choice(casas_com_cavaleiro)
    
    # remove o cavaleiro que vai viver
    cavaleiros[casa_com_cavaleiro].remove(cavaleiro_viver)
    cavaleiros_faltando[cavaleiro_viver] += 1
    
    casas_sem_cavaleiro = []
    for i in range(len(cavaleiros)):
        if cavaleiro_vivo not in cavaleiros[i] and len(cavaleiros[i]) < MAX_CAVALEIROS_CASA:
            casas_sem_cavaleiro.append(i)
            
    casa_sem_cavaleiro = choice(casas_sem_cavaleiro)
    
    # adiciona o cavaleiro que vai morrer
    cavaleiros[casa_sem_cavaleiro].append(cavaleiro_vivo)
    cavaleiros_faltando[cavaleiro_vivo] -= 1

class SimulatedAnnealing:
    def __init__(self, dificuldade, cavaleiros, cavaleiros_faltando, current_state=0):
        # lista com a dificuldade das casas indexadas
        self.dificuldade = dificuldade
        # lista de lista de cavaleiros na casa indexada. deve ter a mesma length de dificuldade
        self.cavaleiros = cavaleiros
        # dicionario. chave é o nome do cavaleiro e o valor é a vida dele
        self.cavaleiros_faltando = cavaleiros_faltando
        # qual casa está.
        self.current_state = current_state
    
    def get_cost(self):
        """Calculates cost of the argument state for your solution."""
        custo = 0
        for i in range(len(self.cavaleiros)):
            soma_poderes = 0
            for j in range(len(self.cavaleiros[i])):
                soma_poderes += PODER_COSMICO[self.cavaleiros[i][j]]
            if soma_poderes == 0:
                soma_poderes = 1
            custo += (self.dificuldade[i]/soma_poderes)
        #custo += len(self.dificuldade) - self.current_state
        return custo
    
    def get_neighbors(self):
        """Returns neighbors of the argument state for your solution."""
        neighbors = []
        #print("current", self.current_state)
        #print("cavaleiros no curret", self.cavaleiros[self.current_state])
        # se tiver mais de um cavaleiro, tira um cavaleiro
        if len(self.cavaleiros[self.current_state]) > MIN_CAVALEIROS_CASA:
            for i in range(len(self.cavaleiros[self.current_state])):
                aux_cavaleiros = copy.deepcopy(self.cavaleiros)
                #print('len ', len(self.cavaleiros[self.current_state]))
                #print('i ', i)
                #print('cavaleiros', self.cavaleiros)
                cavaleiro_removido = self.cavaleiros[self.current_state][i]
                aux_cavaleiros[self.current_state].remove(cavaleiro_removido)
                aux_cavaleiros_faltando = copy.deepcopy(self.cavaleiros_faltando)
                aux_cavaleiros_faltando[cavaleiro_removido] += 1
                neighbors.append(SimulatedAnnealing(self.dificuldade, aux_cavaleiros, aux_cavaleiros_faltando, self.current_state))
        # se tiver menos de 5 cavaleiros, bota um cavaleiro
        if len(self.cavaleiros[self.current_state]) < MAX_CAVALEIROS_CASA:
            for i in range(len(NOME_CAVALEIROS)):
                cavaleiro_adicionado = NOME_CAVALEIROS[i]
                # se o cavaleiro nao estiver na casa e tive vida suficiente, adiciona
                if self.cavaleiros_faltando[cavaleiro_adicionado] > 0 and cavaleiro_adicionado not in self.cavaleiros[self.current_state]:
                    aux_cavaleiros = copy.deepcopy(self.cavaleiros)
                    aux_cavaleiros[self.current_state].append(cavaleiro_adicionado)
                    aux_cavaleiros_faltando = copy.deepcopy(self.cavaleiros_faltando)
                    aux_cavaleiros_faltando[cavaleiro_adicionado] -= 1
                    neighbors.append(SimulatedAnnealing(self.dificuldade, aux_cavaleiros, aux_cavaleiros_faltando, self.current_state))
        # se tem pelo menos 1 cavaleiro, pode ir para a próxima casa, se tiver proxima casa
        if len(self.cavaleiros[self.current_state]) > 0 and self.current_state < (len(self.dificuldade) - 1):
            neighbors.append(SimulatedAnnealing(self.dificuldade,
                                                copy.deepcopy(self.cavaleiros),
                                                copy.deepcopy(self.cavaleiros_faltando), self.current_state + 1))
        # tambem pode voltar uma casa
        if self.current_state > 0:
            neighbors.append(SimulatedAnnealing(self.dificuldade,
                                                copy.deepcopy(self.cavaleiros),
                                                copy.deepcopy(self.cavaleiros_faltando), self.current_state - 1))
        return neighbors
    
    def get_neighbors2(self):
        neighbors = []
        for i in range(len(self.dificuldade)):
            # tira um cavaleiro
            for j in range(len(self.cavaleiros[i])):
                aux_cavaleiros = copy.deepcopy(self.cavaleiros)
                cavaleiro_removido = self.cavaleiros[i][j]
                aux_cavaleiros[i].remove(cavaleiro_removido)
                aux_cavaleiros_faltando = copy.deepcopy(self.cavaleiros_faltando)
                aux_cavaleiros_faltando[cavaleiro_removido] += 1
                neighbors.append(SimulatedAnnealing(self.dificuldade, aux_cavaleiros, aux_cavaleiros_faltando, self.current_state))
            # bota um cavaleiro, se tiver espaco
            if len(self.cavaleiros[i]) < MAX_CAVALEIROS_CASA:
                for j in range(len(NOME_CAVALEIROS)):
                    cavaleiro_adicionado = NOME_CAVALEIROS[j]
                    # se o cavaleiro nao estiver na casa e tiver vida suficiente, adiciona
                    if self.cavaleiros_faltando[cavaleiro_adicionado] > 0 and cavaleiro_adicionado not in self.cavaleiros[i]:
                        aux_cavaleiros = copy.deepcopy(self.cavaleiros)
                        aux_cavaleiros[i].append(cavaleiro_adicionado)
                        aux_cavaleiros_faltando = copy.deepcopy(self.cavaleiros_faltando)
                        aux_cavaleiros_faltando[cavaleiro_adicionado] -= 1
                        neighbors.append(SimulatedAnnealing(self.dificuldade, aux_cavaleiros, aux_cavaleiros_faltando, self.current_state))
        return neighbors
    
    def simulated_annealing(self):
        """Peforms simulated annealing to find a solution"""
        initial_temp = 100
        final_temp = .1
        alpha = 0.01
        
        current_temp = initial_temp
    
        # Start by initializing the current state with the initial state
        current_state = self
        solution = current_state
        melhor_solucao = solution
    
        while current_temp > final_temp:
            neighbor = choice(solution.get_neighbors2())
    
            # Check if neighbor is best so far
            cost_diff = solution.get_cost() - neighbor.get_cost()
    
            # if the new solution is better, accept it
            if cost_diff > 0:
                solution = neighbor
                if solucaoValida(solution.cavaleiros):
                    melhor_solucao = solution
            # if the new solution is not better, accept it with a probability of e^(-cost/temp)
            else:
                if uniform(0, 1) < exp(cost_diff / current_temp):
                    solution = neighbor
            # decrement the temperature
            current_temp -= alpha
    
        return melhor_solucao
    
def main():
    dificuldade = [50, 55, 60, 70, 75, 80, 85, 90, 95, 100, 110, 120]
    cavaleiros = [[], [], [], [], [], [], [], [], [], [], [], []]
    # shun tem 4 vidas pq ele é o mais fraco, o q significa que ele deve viver
    cavaleiros_faltando = { 'Seya': VIDA, 'Ikki': VIDA, 'Shiryu': VIDA, 'Hyoga': VIDA, 'Shun': VIDA }
    total = 0
    minimo = 1000
    maximo = 0
    execucoes = 30
    SimulatedAnnealing(dificuldade, cavaleiros, cavaleiros_faltando).simulated_annealing()
    return
    for i in range(execucoes):
        resposta = SimulatedAnnealing(dificuldade, cavaleiros, cavaleiros_faltando).simulated_annealing()
        custo = resposta.get_cost()
        minimo = min(minimo, custo)
        maximo = max(maximo, custo)
        total += custo
        #print(resposta.get_cost())
        #print(resposta.cavaleiros)
        #print(resposta.cavaleiros_faltando)
    print(total/execucoes)
    print(minimo)
    print(maximo)
    print(resposta.cavaleiros)
    return
    
if __name__ == '__main__':
    main()