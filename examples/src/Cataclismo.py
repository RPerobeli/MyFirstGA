import numpy as np
import matplotlib.pyplot as plt
import random as rnd

class Cataclismo:
    prcntMortes = 0
    def __init__(self,_prcnt=0.8):
        self.prcntMortes = _prcnt
    #endfunc

    def SetPorcentagemMortes(self, valor):
        self.prcntMortes = valor
    #endfunc