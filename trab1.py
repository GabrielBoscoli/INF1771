# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 20:04:04 2020

@author: Gabriel Boscoli

INF1771 - Inteligência Artificial
Trabalho 1 - Busca Heurística e Busca Local
"""

import interface
from heapq import heappush, heappop
from time import sleep

# Dimensões do mapa
LINHAS = 42
COLUNAS = 42

# Coordenada da casa final
CASA_FINAL = (4, 37)

# Coordenada da casa inicial
CASA_INICIAL = (37, 37)

# Retorna uma matriz linhasXcolunas com 0 em todas as posições
def inicializaMatriz(linhas, colunas):
    mapa = []
    for i in range(LINHAS):
        mapa.append([])
        for j in range(COLUNAS):
            mapa[i].append(0)
    return mapa

# 'file' deve estar nas linhas dos dados do mapa
# 'dificuldade' éum dicionário com a dificuldade das casas
# Retorna o mapa
def inicializaMapa(file, dificuldade):
    mapa = inicializaMatriz(LINHAS, COLUNAS)
    for i in range(LINHAS):
        linha = file.readline()
        for j in range(COLUNAS):
            #mapa[i][j] = dificuldade.get(linha[j])
            mapa[i][j] = linha[j]
    return mapa
        
# O parâmetro 'dificuldade' deve ser uma lista com 3 inteiros
# O primeiro elemento representa a dificuldade das casas com terreno montanhoso
# O segundo elemento representa a dificuldade das casas com terreno plano
# O terceiro elemento representa a dificuldade das casas com terreno montanhoso
# Retorna a dificuldade das casas do mapa
def inicializaDificuldade(dificuldade):
    dificuldadeCasas = dict()
    dificuldadeCasas['M'] = dificuldade[0]
    dificuldadeCasas['P'] = dificuldade[1]
    dificuldadeCasas['R'] = dificuldade[2]
    return dificuldadeCasas

# O parâmetro 'poder' deve ser uma lista com 3 inteiros
# O primeiro elemento representa o poder cosmico do Seya
# O segundo elemento representa o poder cosmico do Ikki
# O terceiro elemento representa o poder cosmico do Shiryu
# O quarto elemento representa o poder cosmico do Hyoga
# O quinto elemento representa o poder cosmico do Shun
# Retorna o poder cosmico dos cavaleiros
def inicializaPoderCosmico(poder):
    # será que faz sentido ser um dicionário?
    poderCosmico = dict()
    poderCosmico['Seya'] = poder[0]
    poderCosmico['Ikki'] = poder[1]
    poderCosmico['Shiryu'] = poder[2]
    poderCosmico['Hyoga'] = poder[3]
    poderCosmico['Shun'] = poder[4]
    return poderCosmico

# le os dados configurados através do arquivo 'dados-trab-1.txt'
def leDadosConfiguraveis():
    try:
        f = open('dados-trab-1.txt', 'r')
    except:
        exit()
    linhaDificuldades = f.readline();
    dificuldadeCasas = inicializaDificuldade(list(map(int, linhaDificuldades.split(" "))))
    # lê linha vazia
    f.readline()
    linhaPoder = f.readline();
    poderCosmico = inicializaPoderCosmico(list(map(float, linhaPoder.split(" "))))
    # lê linha vazia
    f.readline()
    mapa = inicializaMapa(f, dificuldadeCasas)
    f.close()
    return mapa, dificuldadeCasas, poderCosmico

# Calcula a distancia de manhattan de cada uma das casas dos mapa em relação ao objetivo
# Retorna uma matriz LINHAS X COLUNAS em que cada elemento representa sua distancia até o objetivo
def calculaDistancia():
    manhattan = []
    for i in range(LINHAS):
        manhattan.append([])
        for j in range(COLUNAS):
            manhattan[i].append(abs(i - CASA_FINAL[0]) + abs(j - CASA_FINAL[1]))
    return manhattan

class Node:
    def __init__(self, coords, pai, g, h):
        self.coords = coords
        self.pai = pai
        self.g = g
        self.h = h
        self.f = g + h
        
    def __lt__(self, other):
        return self.f < other.f
    
    def __eq__(self, other):
        return self.coords == other.coords

def noValido(linha, coluna):
    return (linha >= 0 and linha < LINHAS) and (coluna >= 0 and coluna < COLUNAS)

# Retorna uma lista de nós vizinhos da casa
def getVizinhos(node, dificuldade, manhattan):
    vizinhos = []
    coords = node.coords
    x = coords[0]
    y = coords[1]
    if noValido(x - 1, y):
        xx = x - 1
        yy = y
        vizinhos.append(Node((xx, yy), node, node.g + dificuldade[node.coords[0]][node.coords[1]],
                             manhattan[xx][yy]))
    if noValido(x - 1, y + 1):
        xx = x - 1
        yy = y + 1
        vizinhos.append(Node((xx, yy), node, node.g + dificuldade[node.coords[0]][node.coords[1]],
                             manhattan[xx][yy]))
    if noValido(x, y + 1):
        xx = x
        yy = y + 1
        vizinhos.append(Node((xx, yy), node, node.g + dificuldade[node.coords[0]][node.coords[1]],
                             manhattan[xx][yy]))
    if noValido(x + 1, y + 1):
        xx = x + 1
        yy = y + 1
        vizinhos.append(Node((xx, yy), node, node.g + dificuldade[node.coords[0]][node.coords[1]],
                             manhattan[xx][yy]))
    if noValido(x + 1, y):
        xx = x + 1
        yy = y
        vizinhos.append(Node((xx, yy), node, node.g + dificuldade[node.coords[0]][node.coords[1]],
                             manhattan[xx][yy]))
    if noValido(x + 1, y - 1):
        xx = x + 1
        yy = y - 1
        vizinhos.append(Node((xx, yy), node, node.g + dificuldade[node.coords[0]][node.coords[1]],
                             manhattan[xx][yy]))
    if noValido(x, y - 1):
        xx = x
        yy = y - 1
        vizinhos.append(Node((xx, yy), node, node.g + dificuldade[node.coords[0]][node.coords[1]],
                             manhattan[xx][yy]))
    if noValido(x - 1, y - 1):
        xx = x - 1
        yy = y - 1
        vizinhos.append(Node((xx, yy), node, node.g + dificuldade[node.coords[0]][node.coords[1]],
                             manhattan[xx][yy]))
    return vizinhos

# Checa se existe no com mesmas coordenadas na lista que possuam 'f' menor
def checkNode(lista, node):
    for e in lista:
        if e == node:
            if e.f < node.f:
                return e
    return None

# algoritmo baseado em https://brilliant.org/wiki/a-star-search/
# principalmente -> https://www.geeksforgeeks.org/a-search-algorithm/
# https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
def aStar(mapa, dificuldade, manhattan):
    openList = []
    node = Node(CASA_INICIAL, None, 0, 0)
    heappush(openList, node)
    closedList = []
    while(len(openList) > 0):
        q = heappop(openList)
        vizinhos = getVizinhos()
        for proximo in vizinhos:
            if proximo.coords == CASA_FINAL:
                coords = proximo.coords
                # acho que tem que pegar a dificuldade do q, nao do proximo
                proximo.g = q.g + dificuldade.get(mapa[coords[0]][coords[1]])
                proximo.h = manhattan(mapa[coords[0]][coords[1]])
                proximo.f = proximo.g + proximo.f
                return proximo
            if checkNode(openList, proximo) == None and checkNode(closedList, proximo) == None:
                continue;
            else:
                heappush(openList, proximo)
        closedList.append(q)

def main():
    mapa, dificuldadeCasas, poderCosmico = leDadosConfiguraveis()
    manhattan = calculaDistancia()
    interface.inicializaInterface(LINHAS, COLUNAS, "INF1771")
    interface.setGrid(mapa)
    interface.desenhaGrid()
    print(mapa)
    print(dificuldadeCasas)
    print(poderCosmico)
    print(manhattan)
    sleep(20)
    interface.fechaInterface()
    
main()