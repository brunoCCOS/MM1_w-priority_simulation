import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import t,chi2

class Statistcs():
    '''
    Classe para geração e informe de estatistícas
    '''
    def calc_mean(data):
        '''
        Calcula a méida de um conjunto de amostras
        '''
        return np.mean(data)
    
    def calc_var(data):
        '''
        Calcula a variança de um conjunto de amostras
        '''
        return np.var(data)
    
    def calc_std(data):
        '''
        Calcula o desvio padrão de um conjunto de amostras
        '''
        return np.std(data)    
    def calc_conf_int(data,conf=0.95,dist = "t"):
        '''
        Calcula o intervalo de confiança usando uma distribuição específica
        '''
        n = len(data) 
        dof = n - 1 #graus de liberdade
        m = Statistcs.calc_mean(data)
        s = Statistcs.calc_std(data)
        s2 = Statistcs.calc_var(data)
        
        if dist == 't':
            t_crit = np.abs(t.ppf((1-conf)/2,dof)) #Valor crítico da t-student, faz a inversa da cdf
            return (m-s*t_crit/np.sqrt(len(data)), 
                    m+s*t_crit/np.sqrt(len(data)))#Intervalo de confiança usando t-student
        elif dist == 'chi2':
            return ((n - 1) * s2 / chi2.ppf(conf / 2, dof),
                    (n - 1) * s2 / chi2.ppf(1-conf / 2, dof)) #Intervalo de confiança usando chi-square

    def plot_hist(x,title,label_x,label_y,save = False):
        '''
        Plota histogram de dados
        '''
        # the histogram of the data
        n, bins, patches = plt.hist(x, 50, density=True, facecolor='g', alpha=0.75)

        if label_x:
            plt.xlabel(label_x)
        if label_y:
            plt.ylabel(label_y)
        plt.title(title)
        plt.grid(True)
        plt.show()
        if save:
            plt.savefig(f'img/{title}.png')

    def plot_time_series(x,title,label_x,label_y,save = False):
        '''
        Plota histogram de dados
        '''
        # the histogram of the data
        plt.plot(range(len(x)),x)

        if label_x:
            plt.xlabel(label_x)
        if label_y:
            plt.ylabel(label_y)
        plt.title(title)
        plt.grid(True)
        plt.show()
        if save:
            plt.savefig(f'img/{title}.png')
    
    # def print_full_statistics(*datas):
