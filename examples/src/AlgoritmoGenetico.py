import numpy as np
import matplotlib.pyplot as plt
import random as rnd

class AlgoritmoGenetico:
    #atributos
    DominioVariaveisInicio =0
    DominioVariaveisFim = 0

    populacaoGenotipo = []
    populacaoFenotipo = []
    reprodutores = []

    Bests = [] #lista que armazena as melhores aptidoes de cada geracao, caso haja convergência para valor que não atende à regra
    porcentagemCataclisma = 0

    numReprodutores = 0
    tamCromossomo = 0
    def __init__(self, xi, xf, numrep, tamCr, probMut):
        self.DominioVariaveisInicio = list(xi)
        self.DominioVariaveisFim = list(xf)

        self.numReprodutores = numrep
        self.tamCromossomo = tamCr

        self.probMutacao = probMut
    #endfunc

    def SetCataclisma(self, valor):
        self.porcentagemCataclisma = valor
    #endfunc

    def CriaPopulacaoBinaria(self, num  = 0, imigracao = False):
        if(imigracao):
            imigrantes = []
            for i in range(0,num):
                individuo = []
                for i in range(0,len(self.DominioVariaveisInicio)):
                    individuoGene = []
                    for j in range(0,self.tamCromossomo):
                        individuoGene.append(rnd.randint(0,1))
                    #endfor
                    individuo.append(individuoGene)
                #endfor
                imigrantes.append(individuo)
            #endfor
            self.populacaoGenotipo.append(imigrantes)
        else:
            for i in range(0,self.numReprodutores):
                individuo = []
                for i in range(0,len(self.DominioVariaveisInicio)):
                    individuoGene = []
                    for j in range(0,self.tamCromossomo):
                        individuoGene.append(rnd.randint(0,1))
                    #endfor
                    individuo.append(individuoGene)
                #endfor
                self.reprodutores.append(individuo)
            #endfor
            self.Reproducao()
        #endif
    #endfunc

    def Reproducao(self):
        self.populacaoGenotipo = []
        for i in range(0,len(self.reprodutores)):
            for j in range(0,len(self.reprodutores)):
                filho1, filho2 = self.CrossOver(self.reprodutores[i], self.reprodutores[j])
                self.populacaoGenotipo.append(filho1)
                self.populacaoGenotipo.append(filho2)
            #endfor
        #endfor
        self.populacaoGenotipo = np.array(self.populacaoGenotipo)
    #endfunc

    def CrossOver(self, pai1, pai2):
        pontoXover = rnd.randint(0,len(pai1[0]))
        for j in range(0,len(pai1)):
            for i in range(0,pontoXover):
                p1 = pai1[j]
                p2 = pai2[j]
                p1 = np.insert(p1,i,p2[i])
                p2 = np.insert(p2,i,p1[i+1])
                p1 = np.delete(p1,i+1)
                p2 = np.delete(p2,i+1)
            #endfor
        #endfor
        return np.array(pai1),np.array(pai2)
    #endfunc

    def Fenotipifica(self, xi, xf):
        self.populacaoFenotipo = []
        for individuo in list(self.populacaoGenotipo):
            individuoFenotipo = []
            for i in range(0, len(xi)):
                resultado = xi[i] + self.IND(individuo[i]) * (xf[i]-xi[i])/(2**(len(individuo[i]))-1)
                individuoFenotipo.append(resultado)
            #endfor
            self.populacaoFenotipo.append(individuoFenotipo)
        #endfor
    #endfunc

    def IND(self,i):
        tamanhoCadeiaBits = range(0,len(i))
        ind = 0
        for j in tamanhoCadeiaBits:
            ind += i[j]*2**(len(i)-1-j)
        #endfor
        return ind
    #endfunc

    def SortPopulacoes(self, vetFit, vetPenal, maximize = True):
        self.populacaoGenotipo = list(self.populacaoGenotipo)
        for i in range(0,len(vetFit)):
            for j in range(i,len(vetFit)):
                if(maximize):
                    if(vetFit[j] > vetFit[i]):
                        vetFit = np.insert(vetFit,i,vetFit[j])
                        vetFit = np.delete(vetFit,j+1)
                        
                        self.populacaoGenotipo.insert(i,self.populacaoGenotipo[j])
                        self.populacaoGenotipo.pop(j+1)

                        vetPenal = np.insert(vetPenal,i,vetPenal[j])
                        vetPenal = np.delete(vetPenal,j+1)
                    #endif
                else:
                    if(vetFit[j] < vetFit[i]):
                        vetFit = np.insert(vetFit,i,vetFit[j])
                        vetFit = np.delete(vetFit,j+1)
                        
                        self.populacaoGenotipo.insert(i,self.populacaoGenotipo[j])
                        self.populacaoGenotipo.pop(j+1)

                        self.populacaoFenotipo.insert(i,self.populacaoFenotipo[j])
                        self.populacaoFenotipo.pop(j+1)

                        vetPenal = np.insert(vetPenal,i,vetPenal[j])
                        vetPenal = np.delete(vetPenal,j+1)
                    #endif
                #endif
            #endfor
        #endfor
        self.populacaoGenotipo = np.array(self.populacaoGenotipo)
        self.Bests.append([vetFit[0],vetPenal[0]])
        self.Confere
        return vetFit, vetPenal
    #endfunc

    def SetReprodutores(self):
        self.reprodutores = []
        for i in range(0,self.numReprodutores):
            self.reprodutores.append(self.populacaoGenotipo[i])
        #endfor
        #self.reprodutores = np.array(self.reprodutores)
    #endfunc

    def Mutacao(self):
        for ind in self.populacaoGenotipo:
            for i in range(0,len(ind)):
                for j in range(0,len(ind[i])):
                    if(rnd.uniform(0,1) <= self.probMutacao):
                        if(ind[i][j] == 0):
                            ind[i][j]=1
                        else:
                            ind[i][j]=0
                        #endif
                    #endif
                #endfor
            #endfor
        #endfor
    #endfunc

    def PenalizacaoPorDivisao(self, Fit, n, base):
        Fit = Fit/(base**n)
        return Fit
    #endfunc

    def PenalizacaoPorMultiplicacao(self, Fit, n, base = 2):
        Fit = Fit*(base**n)
        return Fit
    #endfunc
    
    def Penalize(self, vetFit, vetPenal, base = 2, maximize = True):
        if(maximize):
            for i in range(0,len(vetFit)):
                vetFit[i] = self.PenalizacaoPorDivisao(vetFit[i], vetPenal[i], base)
            #endfor
        else:
            for i in range(0,len(vetFit)):
                vetFit[i] = self.PenalizacaoPorMultiplicacao(vetFit[i], vetPenal[i], base)
        #endif
        return vetFit
    #endfunc

    def Cataclisma(self):
        #elimina parte da populacao
        print("CATACLISMA!!!!")
        self.numSobreviventes = (1- self.porcentagemCataclisma)*len(self.populacaoGenotipo)
        self.populacaoGenotipo = self.populacaoGenotipo[0:self.numSobreviventes]
    #endfunc

    def Imigracao(self, numFaltante):
        self.CriaPopulacaoBinaria(num = numFaltante, imigracao = True)
    #endfunc

    def ConfereConvergenciaInvalida(self):
        listaAux = self.Bests[::-1]
        resp = False
        if(listaAux[0][1] != 0):
            if(listaAux[0][0] == listaAux[1][0] and listaAux[0][0] == listaAux[2][0] and listaAux[0][0] == listaAux[3][0] and listaAux[0][0] == listaAux[4][0]):
                resp = True
            #endif
        #endif
        return resp
    #endfunc

    def ImigrarSeNecessario(self):
        if(self.ConfereConvergenciaInvalida):
            numPopAnterior = len(self.populacaoGenotipo)
            self.Cataclisma()
            numFaltante = numPopAnterior - len(self.populacaoGenotipo)
            print(numFaltante)
            self.Imigracao(numFaltante)
    #endfunc
 

#endclass
