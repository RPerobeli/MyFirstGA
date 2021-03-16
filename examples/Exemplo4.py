from src import AlgoritmoGenetico as AG
import numpy as np
import random as rnd
import matplotlib.pyplot as plt

# ------------FUNCOES--------------------
def Aptidao(pop):
    vetFit = np.zeros(len(pop))
    vetFen = np.array(pop)
    for i in range(0,len(pop)):
        x1 = vetFen[i][0]
        x2 = vetFen[i][1]
        x3 = vetFen[i][2]
        x4 = vetFen[i][3]
        vetFit[i] = 1.10471*(x1**2)*x2+ 0.04811*x3*x4*(14.0+x2)
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
        
        t1 = 6000/(np.sqrt(2)*x1*x2)
        alfa = np.sqrt(0.25*((x2**2) + ((x1+x3)**2)))
        # t2 = (6000.0*(14.0+0.5*x2)*alfa)/(2*(0.707*x1*x2*(x2**2/12.0+ 0.25*((x1+x3)**2))))
        num = 6000.0*(14.0+0.5*x2)*alfa
        den = 2*(0.707*x1*x2*((x2**2)/12.0 + 0.25*((x1+x3)**2)))
        t2 = num/den
        Pc = 64746.022*(1-0.0282346*x3)*x3*(x4**3)

        if(-13600+np.sqrt((t1**2)+ (t2**2) + (x2*t1*t2)/alfa) >0):
            n += 1
        if(-30000 + 504000/((x3**2)*x4) >0):
            n+=1
        if(-x4+x1>0):
            n+=1
        if(-Pc + 6000 >0):
            n+=1
        if(-0.25 + 2.1952/((x3**3)*x4)>0):
            n+=1
        #endif
        vetorPenalty.append(n)
    #endfor
    return np.array(vetorPenalty)
#endfunc
# ------------FUNCOES-END----------------

# INICIO MAIN
numReprodutores = 50
tamCromossomo = 15
xi = [0.125, 0.1, 0.1, 0.1]
xf = [10.0, 10.0, 10.0, 10.0]
probMutacao = 0.05 # 5%
geracao = 0
maxGeracoes = 100
basePenalizacao = 10
geracoes = []
aptidoes = []

exato = np.array([2.38113])
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
    ag.SetReprodutores()

    ag.Reproducao()
    #mutacao
    populacaoGen = ag.Mutacao()
    print("Geracao: "+ str(i) + " | aptidao(Max/Min): " + str(vetorAptidao[0]) + " | falhou em: " + str(vetorPenalty[0]))
    geracoes.append(i)
    aptidoes.append(vetorAptidao[0])
    exatos.append(exato.max())
#endfor
print("Esperado Exato: " + str(exato.max()))


for i in range(0,len(xi)):
    print(ag.populacaoFenotipo[0][i])
#endfor

plt.plot(geracoes,aptidoes, exatos)
plt.xlabel("geracoes")
plt.ylabel("aptidao")
plt.show()