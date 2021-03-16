from src import AlgoritmoGenetico as AG
import numpy as np
import matplotlib.pyplot as plt
from math import pi

# ------------FUNCOES--------------------
def Aptidao(pop):
    vetFit = np.zeros(len(pop))
    vetFen = np.array(pop)
    for i in range(0,len(pop)):
        x1 = vetFen[i][0]
        x2 = vetFen[i][1]
        vetFit[i] = 21.5 + x1*np.sin(4*pi*x1)+ x2*np.sin(20*pi*x2)
    #endfor
    return vetFit
#endfunc


# ------------FUNCOES-END----------------

# INICIO MAIN
numReprodutores = 10
tamCromossomo = 20
xi = [-3, 4.1]
xf = [12.1, 5.8]
probMutacao = 0.1 # 5%
geracao = 0
maxGeracoes = 50
geracoes = []
aptidoes = []

#calcula o maximo exato
exato = np.array([38.8503])
exatos = []

ag = AG.AlgoritmoGenetico(xi, xf, numReprodutores, tamCromossomo, probMutacao)
ag.CriaPopulacaoBinaria()

for i in range(0,maxGeracoes):
    #Transforma populacao em fenotipo

    populacaoFen = ag.Fenotipifica(xi,xf)

    #testa aptidao da populacao inicial
    vetorAptidao = Aptidao(ag.populacaoFenotipo)
    vetorAptidao = ag.SortPopulacoes(vetorAptidao)
    #adquire os reprodutores
    #reprodutores = populacaoGen[0:numReprodutores]
    ag.SetReprodutores()
    ag.Reproducao()

    #mutacao
    populacaoGen = ag.Mutacao()
    print("Geracao: "+ str(i) + " | aptidaoMax: " + str(vetorAptidao[0]))
    geracoes.append(i)
    aptidoes.append(vetorAptidao[0])
    exatos.append(exato.max())
#endfor
print("Maximo exato: " + str(exato.max()))

plt.plot(geracoes,aptidoes, exatos)
plt.xlabel("geracoes")
plt.ylabel("aptidao max")
plt.show()
