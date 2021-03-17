from src import AlgoritmoGenetico as AG
import numpy as np
import random as rnd
import matplotlib.pyplot as plt
from math import pi

# ------------FUNCOES--------------------
def Aptidao(pop):
    vetFit = np.zeros(len(pop))
    vetFen = np.array(pop)
    for i in range(0,len(pop)):
        x1 = vetFen[i][0]
        x2 = vetFen[i][1]
        x3 = vetFen[i][2]
        vetFit[i] = x1+x2+x3
    #endfor
    return vetFit
#endfunc

def Restricoes(popFen):
    vetorPenalty = []
    for individuo in popFen:
        n=0
        x1 = individuo[0]
        x2 = individuo[1]
        x3 = individuo[2]
        x4 = individuo[3]
        x5 = individuo[4]
        x6 = individuo[5]
        x7 = individuo[6]
        x8 = individuo[7]
        if(-1 + 0.0025*(x4+x6) >0):
            n += 1
        if(-1 + 0.0025*(x5+x7-x4) >0):
            n+=1
        if(-1+0.01*(x8-x5)>0):
            n+=1
        if(-x1*x6 +  833.33252*x4 + 100*x1 - 83333.333 >0):
            n+=1
        if(-x2*x7 + 1250*x5 + x2*x4 - 1250*x4 >0):
            n+=1
        if(-x3*x8 + 1250000+ x3*x5 - 2500*x5>0):
            n+=1
        #endif
        vetorPenalty.append(n)
    #endfor
    return np.array(vetorPenalty)
#endfunc
# ------------FUNCOES-END----------------

# INICIO MAIN
numReprodutores = 10
tamCromossomo = 15
xi = [100, 1000, 1000, 10, 10, 10, 10, 10]
xf = [10000, 10000, 10000, 1000, 1000, 1000, 1000, 1000]
probMutacao = 0.05 # 5%
geracao = 0
maxGeracoes = 100
basePenalizacao = 10
geracoes = []
aptidoes = []

exato = np.array([7049.248021])
exatos = []

rnd.seed(2)
ag = AG.AlgoritmoGenetico(xi, xf, numReprodutores, tamCromossomo, probMutacao)
ag.CriaPopulacaoBinaria()
print(len(ag.populacaoGenotipo))

for i in range(0,maxGeracoes):
    #Transforma populacao em fenotipo
    populacaoFen = ag.Fenotipifica(xi,xf)

    #testa aptidao da populacao inicial
    vetorAptidao = Aptidao(ag.populacaoFenotipo)
    vetorPenalty = Restricoes(ag.populacaoFenotipo)
    vetorAptidao = ag.Penalize(vetorAptidao, vetorPenalty, basePenalizacao ,maximize = False)
    vetorAptidao, vetorPenalty = ag.SortPopulacoes(vetorAptidao, vetorPenalty, maximize = False)
    #adquire os reprodutores
    #reprodutores = populacaoGen[0:numReprodutores]
    ag.SetReprodutores()
    ag.Reproducao()
    #populacaoFilha = Reproducao(reprodutores)
    #populacaoGen = AdmiteFilhosAptos(populacaoGen, populacaoFilha,vetorAptidao,xi,xf)

    #mutacao
    populacaoGen = ag.Mutacao()
    print("Geracao: "+ str(i) + " | aptidao(Max/Min): " + str(vetorAptidao[0]) + " | falhou em: " + str(vetorPenalty[0]))
    geracoes.append(i)
    aptidoes.append(vetorAptidao[0])
    exatos.append(exato.max())
    ag.ImigrarSeNecessario()
#endfor
print("Esperado Exato: " + str(exato.max()))


for i in range(0,len(xi)):
    print(ag.populacaoFenotipo[0][i])
#endfor

plt.plot(geracoes,aptidoes, exatos)
plt.xlabel("geracoes")
plt.ylabel("aptidao")
plt.show()