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
    
    def calc_inc_mean(mean,samples,nsamples):
        '''
        Calcula a méida de um conjunto de amostras incrementalmente
        '''
        for sample in samples:
            mean = (nsamples*mean + sample)/(nsamples+1)
            nsamples += 1
        return mean
    
    def calc_inc_var(old_mean,var,samples,nsamples):
        '''
        Calcula a variança de um conjunto de amostras incrementalmente
        '''
        
        for sample in samples:
            var = (nsamples/(nsamples + 1))*(var**2 + ((sample - old_mean)**2)/(nsamples + 1))
            nsamples += 1
        return var
    
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
            t_crit = np.abs(t.ppf((1-conf)/2,dof)) #Valor crítico da t-student usando a ppf(inversa da cdf)
            lower = m-s*t_crit/np.sqrt(len(data))
            upper = m+s*t_crit/np.sqrt(len(data))
            if lower < 0:
                lower = 0 # Sabemos que não podem haver valores negativos
            return (lower, 
                    upper)#Intervalo de confiança usando t-student
        elif dist == 'chi2':
            return ((n - 1) * s2 / chi2.ppf(1-conf / 2, dof),
                    (n - 1) * s2 / chi2.ppf(conf / 2, dof)) #Intervalo de confiança usando chi-square usando a ppf(innversa da cdf)

    def calc_precision(upper,lower):
        '''
        Calcula a precisão de um dado intervalo de confiança
        '''
        p = (upper - lower)/(upper+lower)
        return p
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

    def plot_scatter(x,title,label_x,label_y,save = False):
        '''
        Plota histogram de dados
        '''
        # the histogram of the data
        plt.scatter(range(len(x)),x)

        if label_x:
            plt.xlabel(label_x)
        if label_y:
            plt.ylabel(label_y)
        plt.title(title)
        plt.grid(True)
        plt.show()
        if save:
            plt.savefig(f'img/{title}.png')
            
    def plot_line(x,title,label_x,label_y,save = False):
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
    
    def print_full_statistics(results,means,vars,plots = True):
        '''
        Printa todas as estatisticas a respeito das métricas
        '''
        for data in results:
            
            
            print(f'Estatisticas a respeito de {data}:')
            print(f'\t\ esperança: {Statistcs.calc_mean(results[data])}')
            print(f'\t\ variancia: {Statistcs.calc_var(results[data])}')
            print(f'\t\ desvio padrão: {Statistcs.calc_std(results[data])}')
            if data in means:
                mean_conf = Statistcs.calc_conf_int(means[data])
                print(f'\t\ intervalo de confiança para média: {mean_conf}, valor médio {(mean_conf[1]-mean_conf[0])/2}, precisão: {Statistcs.calc_precision(mean_conf[1],mean_conf[0])}')
            if data in vars:
                var_conf = Statistcs.calc_conf_int(vars[data], dist = "chi2")
                print(f'\t\ intervalo de confiança para variancia: {var_conf} valor médio {(var_conf[1]-var_conf[0])/2}, precisão:{Statistcs.calc_precision(var_conf[1],var_conf[0])}')
            print('-'*30)
            if plots:
                Statistcs.plot_scatter(results[data],f'Progresso no tempo de {data}','Tempo',f'{data}')
                Statistcs.plot_hist(results[data],f'Distribuição de {data}','Valores','Frequencia')
        return
