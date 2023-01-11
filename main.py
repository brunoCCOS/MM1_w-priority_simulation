from simulation import Clock, Manager
from statistcs import Statistcs
from fila import Fila
from cliente import Client
from servidor import Service
import time as tm
import numpy as np
from scipy.stats import t,chi2

def sim(rho: int, service_rate=1, max_costumers: int = None, debugging=False):
    # inicializa variaveis de fila e tempo
    clock = Clock()  # Inicia o relógio
    Fila.reset() #Reinicia globais das classes
    Client.reset()#Reinicia globais das classes
    next_arrival = 0
    finish_time = None

    fila1 = Fila(rho, 1)#Cria fila 1
    fila2 = Fila(rho, 2)#Cria fila 2
    customer = None #cliente inicial
    servidor = Service(service_rate)#Cria servidor
    
    #Variaveis para debbug
    arrive = False
    server_state = 0
    empty_time = 0
    last_time_busy = 0
    
    n_fregueses = 0 
    on = True

    manager = Manager(clock)
    while on:
        timestep = clock.get_time()
        # Programa a próxima chegada em caso de não existir
        if not next_arrival and max_costumers>n_fregueses:
            next_arrival = fila1.generate_next_arrival_time(timestep)
            n_fregueses += 1
        elif next_arrival == timestep:  # se atingir o tempo da chegada introduzir na fila
            customer = fila1.arrive_customer(timestep)
            arrive = True
            if  max_costumers>=n_fregueses:
                next_arrival = fila1.generate_next_arrival_time(
                    timestep)  # Programa a chegada seguinte
                n_fregueses+= 1 # Conta mais um freguês no sistema
            else:
                next_arrival = fila1.set_next_arrival_time(np.inf)
        else:
            arrive = False
        manager.handle_server(servidor)# Trata servidor
        manager.handle_queue(fila1, servidor)# Trata fila 1
        manager.handle_queue(fila2, servidor)# Trata fila 2
        
        if debugging:  # Logging para debug do código
            print('-'*30)
            print(f't:{timestep}')
            if arrive:
                print(f'Fregues {customer.id} chegou no sistema')
            if next_arrival:
                print(f'Próxima chegada configurada para {next_arrival}')
            print(
                f'Fila 1: {[curr.get_id() for curr in Fila.filas[0].get_queue()]}')
            print(
                f'Fila 2: {[curr.get_id() for curr in Fila.filas[1].get_queue()]}')
            if fila2.get_next() is not None:
                print('tempo servido:',fila2.get_next().get_served_time(),'serviço residual:',fila2.get_next().get_service_residual())
            if servidor.is_busy():
                finish_time = servidor.get_current().get_estimated_finish()
                print(f'Servidor: Freguês {servidor.get_current().get_id()}, fila de origem {servidor.get_current().get_priority()} , fim do serviço em {finish_time}')
                if server_state != 1:
                    print('servidor estava vazio e encheu')
                    empty_time += clock.get_time() - last_time_busy
                    server_state = 1
            else:
                print(f'Servidor: vazio')
                if server_state != 0:
                    print('servidor estava cheio e esvaziou')
                    last_time_busy = clock.get_time()
                    server_state = 0
            tm.sleep(0.5)

        if servidor.is_busy():
                if server_state != 1:
                    empty_time += clock.get_time() - last_time_busy
                    server_state = 1
        else:
                if server_state != 0:
                    last_time_busy = clock.get_time()
                    server_state = 0
        if n_fregueses > max_costumers and not servidor.is_busy():
            manager.set_busy_time(clock.get_time()) #Calcula o tempo ocupado
            return manager.get_records()
        manager.handle_clock(fila1,servidor)  # avança unidade de tempo


if __name__ == '__main__':
    results = dict({
        'T1': [],
        'W1': [],
        'N1': [],
        'Nq1': [],
        'T2': [],
        'W2': [],
        'N2': [],
        'Nq2': [],
        'rho':[],
        'total_time': []
    })
    means = dict({
        'T1': [],
        'W1': [],
        'N1': [],
        'Nq1': [],
        'T2': [],
        'W2': [],
        'N2': [],
        'Nq2': [],
        # 'N': [],
        # 'rho':[]
    })
    vars = dict({
        'W1':[],
        'W2':[],
        # 'rho':[]
    })

    n_rodadas = int(input('Insira o número de rodadas:'))
    n_fregueses = int(input('Número de fregueses por rodada:'))
    rho = float(input('Taxa de ocupação do servidor:'))
    time = tm.time()
    for simulation in range(n_rodadas):
        
        records = sim(rho, max_costumers = n_fregueses, debugging=False)
        for key in results: #Appenda os resultados das simulações
            #Descarta a fase transiente
            if key == 'rho':
                results[key]+=records[key]
            elif key[:1] == 'N': #tratamento especial para número de pessoas pois dividi-se pelo tempo total da simulação
                results[key].append(sum(records[key])/sum(records['total_time'])) #Calcula a média para o número de pessoas
                means[key].append(sum(records[key])/sum(records['total_time'])) 
            else: 
                results[key]+=records[key][:]
                if key in means:
                    means[key].append(Statistcs.calc_mean(records[key][:]))
                if key in vars:
                    vars[key].append(Statistcs.calc_var(records[key][:])) 

    # print(results['Nq1'])
    # print(results['N1'],results['Nq1'])
    # print(results['N2'],results['Nq2'])
    # Analise corretude
    # print(results['rho'])
    # Statistcs.plot_line(results['rho'],'Taxa de ocupação', 'N° de fregueses/60','rho')
    
    #Analise fase transiente]
    # print(np.mean(means['W1']))
    # print(np.mean(means['W2']))
    # intervalos = [i*1 for i in range (500)]
    # Statistcs.plot_line([np.mean(results['W1'][i:]) for i in intervalos],'Fases X W1', 'Número da coletas descartadas','W1')   
    # Statistcs.plot_line([np.mean(results['W2'][i:]) for i in intervalos],'Fases X W2', 'Número da coletas descartadas','W2')   
    # Statistcs.plot_line([np.mean(results['N'][i*3:]) for i in intervalos],'Fases X N', 'Número da coletas descartadas','N')   

    # Analise número de fregueses
    # Statistcs.plot_line(means['W1'],'N° de fregueses X W1', 'Número de fregueses/50','W1')   
    # Statistcs.plot_line(means['W2'],'N° de fregueses X W2', 'Número de fregueses/50','W2')   
    # Statistcs.plot_line(means['N'],'N° de fregueses X N', 'Número de fregueses/50','N')   

    
    ## Analise do intervalo de confiança
    # precs = []
    # for data in means:
    #     upper, lower = Statistcs.calc_conf_int(means[data])
    #     prec = Statistcs.calc_precision(upper,lower)
    #     precs.append(prec)
    # Statistcs.plot_line(precs, 'Tabela de precisão do intervalo', 'N° de rodadas', 'Precisão')
    
    #Print tabela
    Statistcs.print_full_statistics(results,means,vars,plots = False)
    
    # print('Tempo de execução:',tm.time()-time)
    