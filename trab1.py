# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 20:04:04 2020

@author: Gabriel Boscoli

INF1771 - Inteligência Artificial
Trabalho 1 - Busca Heurística e Busca Local
"""

# Dimensões do mapa
LINHAS = 42
COLUNAS = 42

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
            mapa[i][j] = dificuldade.get(linha[j])
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

def main():
    mapa, dificuldadeCasas, poderCosmico = leDadosConfiguraveis()
    print(mapa)
    print(dificuldadeCasas)
    print(poderCosmico)
    
main()