from simulation import Clock, Manager
from statistcs import Statistcs
from fila import Fila
from cliente import Client
from servidor import Service
import time as tm
import numpy as np

def sim(rho: int, service_rate=1, time_horizon: int = None, debugging=False,stopping_arrival = 10000000):
    # inicializa variaveis de fila e tempo
    clock = Clock()  # Inicia o relógio
    Fila.reset() #Reinicia globais das classes
    Client.reset()#Reinicia globais das classes
    next_arrival = 0
    finish_time = None

    fila1 = Fila(rho, 1)
    fila2 = Fila(rho, 2)
    customer = None
    servidor = Service(service_rate)
    arrive = False
    
    on = True

    manager = Manager(clock)
    while on:
        timestep = clock.get_time()
        # Programa a próxima chegada em caso de não existir
        if not next_arrival:
            # soma 1 para garantir que nao seja gerada uma entrada <0.5
            next_arrival = fila1.set_next_arrival_time(timestep)
            # e ele arredonde para o timestep atual
        elif next_arrival == timestep and stopping_arrival>timestep:  # se atingir o tempo da chegada introduzir na fila
            customer = fila1.arrive_customer(timestep)
            arrive = True
            next_arrival = fila1.set_next_arrival_time(
                timestep)  # Programa a chegada seguinte
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
            else:
                print(f'Servidor: vazio')
            tm.sleep(0.5)


        manager.handle_clock(fila1,servidor)  # avança unidade de tempo
        if timestep >= time_horizon:
            # print('Fim da simulação')
            # print(manager.get_records())
            # Statistcs.plot_time_series(manager.get_records()['N2'],'Número de pessoas na fila 1','Tempo','Número de pessoas')
            manager.set_busy_time(clock.get_time())
            return manager.get_records()

if __name__ == '__main__':
    results = dict({
        'W1':[],
        'W2':[],
        'W':[],
        'S1':[],
        'S2':[],
        'S':[],
        'T1':[],
        'T2':[],
        'T':[],
        'Nq1':[],
        'Nq2':[],
        'N1':[],
        'N2':[],
        'rho':[]
    })
    means = list()
    for simulation in range(1):
        records = sim(0.5, time_horizon=1000, debugging=True)
        for key in records: #Appenda os resultados das simulações
            results[key]+=records[key]
        print(records['rho'])
        
        # NOTAS PARA O THIAGOOo
        #PRINTA A PORCENTAGeM DO TEMPO QUE FICA OCUPADO, REPARA QUE QUANDO AUMENTA O TIME_HORIZON O RHO FICA AUMENTANDO MTO, OU SEJA TEM T->inf A FILA ESTOURA, DESCOBRE PQ
        #AGORA O BGL ELE NAO AVANÇA UNIDADEP OR UNIDADE, ELE CALCULA O TEMPO DO PROXIMO EVENTO E PULA PRA ELE, COMO SE ELE TIVESSE UMA AGENDA DE EVENTOS FUTUROS E FOSSE 
        #RESOLVENDO UM POR UM, ASSIM ELE CONSEGUE TRABALHAR COM NÙMEROS DECIMAIS SUPER PRECISOS. EX: SÓ EXISTEM 2 TIPOS DE EVENTO, CHEGA ALGUEM NA FILA E TERMINA ALGUEM Q TA EM 
        # SERVIÇO, ENT POR EXEMPLO PROX CHEGADA: t, FIM DO SERVIÇO: t+1, PROX EVENTO = min(PROX CHEGADA,FIM DO SERVICO) ai o relogio avança direto para PROXIMO EVENTO e faz os 
        #tramentos. SE MUDAR A OPÇÂO DE DEBUGGING P TRUE ELE FICA PRINTANDO AS COISAS, DEIXA EM FALSE P RODAR MAIS RÁPIDO
        # POSSIVEIS IDEIAS, checa se a contagem de tempo ta sendo feito certa e se realmente ta estourando ou é só impressão e contagem errada(dificil), 
        #ve como a função exponencial deveria funcionar, as vezes eu to passando parametros errados(médio), faz mágica
        means.append(Statistcs.calc_mean(records['W2']))
        
    #ALGUMS POSSIVEIS PRINTS UTEIS PRO THIGS
    # Statistcs.print_full_statistics(results,plots = False)
    # interval = Statistcs.calc_conf_int(means)
    # print(f'Intervalo de confiança para o Tempo total médio: \n\tlimite inferior:{interval[0]}\n\tlimite superior{interval[1]}')
    Statistcs.plot_scatter(means,'Médias de tempo nas simulações','Simualção','Tempo médio total')
    # Statistcs.plot_hist(means,'Médias de tempo nas simulações','Simualção','Tempo médio total')
