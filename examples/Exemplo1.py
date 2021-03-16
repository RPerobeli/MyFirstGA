from src import AlgoritmoGenetico as AG
import numpy as np
import matplotlib.pyplot as plt
from math import pi

# ------------FUNCOES--------------------
def Aptidao(pop):
    vetFit = np.zeros(len(pop))
    vetFen = np.array(pop)
    vetFit = vetFen*np.sin(10*pi*vetFen)+1
    return vetFit
#endfunc


# ------------FUNCOES-END----------------

# INICIO MAIN
numReprodutores = 10
tamCromossomo = 15
xi = [-1]
xf = [2]
probMutacao = 0.05 # 5%
geracao = 0
maxGeracoes = 20
geracoes = []
aptidoes = []

#calcula o maximo exato
x = np.arange(xi[0],xf[0],0.00001,float)
exato = x*np.sin(10*pi*x) +1
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
    #populacaoFilha = Reproducao(reprodutores)
    #populacaoGen = AdmiteFilhosAptos(populacaoGen, populacaoFilha,vetorAptidao,xi,xf)

    #mutacao
    populacaoGen = ag.Mutacao()
    print("Geracao: "+ str(i) + " | aptidaoMax: " + str(vetorAptidao[0]))
    geracoes.append(i)
    aptidoes.append(vetorAptidao[0])
    exatos.append(exato.max())
#endfor
print("Maximo exato: " + str(exato.max()))

for i in range(0,len(xi)):
    print(ag.populacaoFenotipo[0][i])
#endfor


plt.plot(geracoes,aptidoes, exatos)
plt.xlabel("geracoes")
plt.ylabel("aptidao")
plt.show()