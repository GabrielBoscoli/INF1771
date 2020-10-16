# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 13:00:32 2020

@author: Gabriel Boscoli

Módulo responsável pelo simulated annealing
"""

from random import choice, uniform
from math import exp
import copy

NOME_CAVALEIROS = ['Seya', 'Ikki', 'Shiryu', 'Hyoga', 'Shun']

MIN_CAVALEIROS_CASA = 0
MAX_CAVALEIROS_CASA = 5

# Poder cosmico default
PODER_COSMICO = { 'Seya': 1.5, 'Ikki': 1.4, 'Shiryu': 1.3, 'Hyoga': 1.2, 'Shun': 1.1 }

# Numero de vidas de cada cavaleiro
VIDA = 5

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
            neighbor = choice(solution.get_neighbors())
    
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
    for i in range(30):
        resposta = SimulatedAnnealing(dificuldade, cavaleiros, cavaleiros_faltando).simulated_annealing()
        custo = resposta.get_cost()
        minimo = min(minimo, custo)
        maximo = max(maximo, custo)
        total += custo
        #print(resposta.get_cost())
        #print(resposta.cavaleiros)
        #print(resposta.cavaleiros_faltando)
    print(total/30)
    print(minimo)
    print(maximo)
    return
    
if __name__ == '__main__':
    main()