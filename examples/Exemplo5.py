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
        x5 = vetFen[i][4]
        x6 = vetFen[i][5]
        x7 = vetFen[i][6]
        p1 = 0.7854*x1*x2**2*(3.333333333333*x3**2+14.9334*x3-43.0934)
        p2 = 1.508*x1*(x6**2+x7**2)
        p3 = 7.4777*(x6**3+x7**3)
        p4 = 0.7854*(x4*x6**2+x5*x7**2)
        vetFit[i] = p1-p2+p3+p4
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
    

        if(27/(x1*x2**2*x3) -1 >0):
            n += 1
        if(397.5/(x1*x2**2*x3**2) -1 >0):
            n+=1
        if(1.93*x4**3/(x2*x3*x6**4) -1>0):
            n+=1
        if(1.93*x5**3/(x2*x3*x7**4) -1 >0):
            n+=1
        if(np.sqrt((745*x4/(x2*x3))**2 + 16.9*10**6)/(110.0*x6**3) -1>0):
            n+=1
        if(np.sqrt((745*x4/(x2*x3))**2 + 157.5*10**6)/(85.0*x7**3) -1>0):
            n+=1
        if((x2*x3)/40 -1 >0):
            n+=1
        if((5*x2)/x1 -1 >0):
            n+=1
        if(x1/(12*x2) -1 >0):
            n+=1
        if((1.5*x6+1.9)/x4 -1 >0):
            n+=1
        if((1.1*x7+1.9)/x5 -1 >0):
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
xi = [2.6, 0.7, 17, 7.3, 7.8, 2.9, 5.0]
xf = [3.6, 0.8, 28, 8.3, 8.3, 3.9, 5.5]
VariaveisDiscretas = [2]
probMutacao = 0.05 # 5%
geracao = 0
maxGeracoes = 50
basePenalizacao = 10
geracoes = []
aptidoes = []

exato = np.array([2996.3481])
exatos = []

rnd.seed(2)
ag = AG.AlgoritmoGenetico(xi, xf, numReprodutores, tamCromossomo, probMutacao)
ag.CriaPopulacaoBinaria()
print(len(ag.populacaoGenotipo))

for i in range(0,maxGeracoes):
    #Transforma populacao em fenotipo
    populacaoFen = ag.Fenotipifica(xi,xf,VariaveisDiscretas, discrete = True)

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