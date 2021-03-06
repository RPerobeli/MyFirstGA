import numpy as np
import matplotlib.pyplot as plt
import random as rnd
from src import Cataclismo as cata

class AlgoritmoGenetico:
    #atributos
    DominioVariaveisInicio =0
    DominioVariaveisFim = 0

    populacaoGenotipo = []
    populacaoFenotipo = []
    reprodutores = []
    Bests = [[0,0], [0,0], [0,0], [0,0]] #lista que armazena as melhores aptidoes de cada geracao, caso haja convergência para valor que não atende à regra

    numReprodutores = 0
    tamCromossomo = 0

    cataclismo = cata.Cataclismo()

        
    def __init__(self, xi, xf, numrep, tamCr, probMut):
        self.DominioVariaveisInicio = list(xi)
        self.DominioVariaveisFim = list(xf)

        self.numReprodutores = numrep
        self.tamCromossomo = tamCr

        self.probMutacao = probMut
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
                self.populacaoGenotipo.append(individuo)
            #endfor
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
        #self.populacaoGenotipo = np.arrayself.populacaoGenotipo)
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

    def Fenotipifica(self, xi, xf, indVarDiscretas = [], discrete = False):
        self.populacaoFenotipo = []
        indVarDiscretas = list(indVarDiscretas)

        for individuo in list(self.populacaoGenotipo):
            individuoFenotipo = []
            for i in range(0, len(xi)):
                resultado = xi[i] + self.IND(individuo[i]) * (xf[i]-xi[i])/(2**(len(individuo[i]))-1)
                if(discrete):
                    if(self.ConferirVarDiscreta(indVarDiscretas,i)):
                        resultado = round(resultado,0)
                    #endif
                #endif
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

    def ConferirVarDiscreta(self, indVarDiscretas, i):
        #Confere se o indice i de uma variável está entre as variáveis discretas
        for j in indVarDiscretas:
            if(i == j):
                return True
            #endif
        #endfor
        return False
    #endif

    def SortPopulacoes(self, vetFit, vetPenal = [] , maximize = True):
        if(vetPenal != []):
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
            #self.populacaoGenotipo = np.array(self.populacaoGenotipo)
            self.Bests.append([vetFit[0],vetPenal[0]])
            return vetFit, vetPenal
        else:
            self.populacaoGenotipo = list(self.populacaoGenotipo)
            for i in range(0,len(vetFit)):
                for j in range(i,len(vetFit)):
                    if(maximize):
                        if(vetFit[j] > vetFit[i]):
                            vetFit = np.insert(vetFit,i,vetFit[j])
                            vetFit = np.delete(vetFit,j+1)
                            
                            self.populacaoGenotipo.insert(i,self.populacaoGenotipo[j])
                            self.populacaoGenotipo.pop(j+1)
                        #endif
                    else:
                        if(vetFit[j] < vetFit[i]):
                            vetFit = np.insert(vetFit,i,vetFit[j])
                            vetFit = np.delete(vetFit,j+1)
                            
                            self.populacaoGenotipo.insert(i,self.populacaoGenotipo[j])
                            self.populacaoGenotipo.pop(j+1)

                            self.populacaoFenotipo.insert(i,self.populacaoFenotipo[j])
                            self.populacaoFenotipo.pop(j+1)
                        #endif
                    #endif
                #endfor
            #endfor
            #self.populacaoGenotipo = np.array(self.populacaoGenotipo)
            self.Bests.append([vetFit[0],0])
            return vetFit
        #endif
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

    def PenalizacaoPorDivisao(self, Fit, n, base=2):
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

    def Cataclismo(self):
        #elimina parte da populacao
        print("CATACLISMO!!!!")
        numSobreviventes = (1- self.cataclismo.prcntMortes)*len(self.populacaoGenotipo)
        self.populacaoGenotipo = self.populacaoGenotipo[0:int(numSobreviventes)]
        #print(len(self.populacaoGenotipo))
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

    def ImigrarSeNecessario(self, taxaMorte = 0.2):
        if(self.ConfereConvergenciaInvalida()):
            numPopAnterior = len(self.populacaoGenotipo)
            self.cataclismo.SetPorcentagemMortes(taxaMorte)
            self.Cataclismo()
            numFaltante = numPopAnterior - len(self.populacaoGenotipo)
            #print(numFaltante)
            self.Imigracao(numFaltante)
    #endfunc
 

#endclass
