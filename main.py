from simulation import Clock, Manager
from fila import Fila 
from cliente import Client
from servidor import Service
import time as tm
def run(rho:int,service_rate = 1,time_horizon:int = None,debugging = False):
    #inicializa variaveis de fila e tempo
    clock = Clock() #Inicia o relógio
    
    next_arrival = 0 
    end_service = 0

    fila1 = Fila(rho,1)
    fila2 = Fila(rho,2)
    customer = None
    servidor = Service(service_rate)
    on = True
    
    manager = Manager(clock)
    while on:
        timestep = clock.get_time()
        #Programa a próxima chegada em caso de não existir
        if not next_arrival:
            next_arrival = round(fila1.get_next_arrival_time(timestep))
        elif next_arrival == timestep:# se atingir o tempo da chegada introduzir na fila
            customer = fila1.arrive_customer(timestep)
            next_arrival = round(fila1.get_next_arrival_time(timestep)) #Programa a chegada seguinte
        response = manager.handle_queue(fila1,servidor)

        if debugging: #Logging para debug do código
            print(f't:{timestep}')
            print('-'*30)
            if next_arrival:
                print(f'Próxima chegada configurada para {next_arrival}')
            if customer is not None:
                print(f'Fregues {customer.id} chegou na fila 1')
            if response is None:
                print('Ninguem na fila de espera')
            elif response[0] == 0:
                print('Fila ocupada,servidor vazio')
            elif response[0] == 1:
                print('Fila ocupada,servidor ocupado com prioridade mais baixa, swap')
            elif response[0] == 2:
                print('Fila ocupada,servidor ocupado com prioridade mais alta,espera')
            finish_time = round(customer.get_estimated_finish()) 
            print(f'Termina em t={finish_time} para o fim do serviço atual')
            print('-'*30)
            tm.sleep(0.5)
            
        manager.handle_server(servidor)



        clock.tick_clock()#avança unidade de tempo
        if timestep == time_horizon:
            print('Fim da simulação')
            break



if __name__ == '__main__':
    run(0.6,time_horizon=10,debugging= True)