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
    end_service = 0
    finish_time = None

    fila1 = Fila(rho, 1)
    fila2 = Fila(rho, 2)
    customer = None
    servidor = Service(service_rate)

    on = True

    manager = Manager(clock)
    while on:
        timestep = clock.get_time()
        # Programa a próxima chegada em caso de não existir
        if not next_arrival:
            # soma 1 para garantir que nao seja gerada uma entrada <0.5
            next_arrival = round(fila1.get_next_arrival_time(timestep+1))
            # e ele arredonde para o timestep atual
        elif next_arrival == timestep and stopping_arrival>timestep:  # se atingir o tempo da chegada introduzir na fila
            customer = fila1.arrive_customer(timestep)
            next_arrival = round(fila1.get_next_arrival_time(
                timestep+1))  # Programa a chegada seguinte

        if debugging:  # Logging para debug do código

            print('-'*30)
            print(f't:{timestep}')
            if next_arrival:
                print(f'Próxima chegada configurada para {next_arrival}')
            if customer is not None:
                print(f'Fregues {customer.id} chegou na fila 1')
            print(
                f'Fila 1: {[curr.get_id() for curr in Fila.filas[0].get_queue()]}')
            print(
                f'Fila 2: {[curr.get_id() for curr in Fila.filas[1].get_queue()]}')
            if servidor.is_busy():
                finish_time = round(
                    servidor.get_current().get_estimated_finish())
                print(f'Servidor: Freguês {servidor.get_current().get_id()}, fila de origem {servidor.get_current().get_priority()} , fim do serviço em {finish_time}')
            else:
                print(f'Servidor: vazio')
            tm.sleep(0.5)

        manager.handle_queue(fila1, servidor)# Trata fila 1
        manager.handle_queue(fila2, servidor)# Trata fila 2
        manager.handle_server(servidor)# Trata servidor

        clock.tick_clock()  # avança unidade de tempo
        if timestep == time_horizon:
            # print('Fim da simulação')
            # print(manager.get_records())
            # Statistcs.plot_time_series(manager.get_records()['N2'],'Número de pessoas na fila 1','Tempo','Número de pessoas')
            return manager.get_records()

if __name__ == '__main__':
    means = np.array([])
    for simulation in range(100):
        records = sim(0.8, time_horizon=1000, debugging=False)
        means = np.append(means,records['T1'])
    interval = Statistcs.calc_conf_int(means)
    print(f'Intervalo de confiança para o Tempo total médio: \n\tlimite inferior:{interval[0]}\n\tlimite superior{interval[1]}')
    Statistcs.plot_time_series(means,'Médias de tempo nas simulações','Simualção','Tempo médio total')
    Statistcs.plot_hist(means,'Médias de tempo nas simulações','Simualção','Tempo médio total')
