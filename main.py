from simulation import Clock, Manager
from fila import Fila 
from cliente import Client
from servidor import Service
import time as tm

def run(rho:int,service_rate = 3,time_horizon:int = None,debugging = False):
    #inicializa variaveis de fila e tempo
    clock = Clock() #Inicia o relógio
    
    next_arrival = 0 
    end_service = 0
    finish_time = None

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
            next_arrival = round(fila1.get_next_arrival_time(timestep+1))
        elif next_arrival == timestep:# se atingir o tempo da chegada introduzir na fila
            customer = fila1.arrive_customer(timestep)
            next_arrival = round(fila1.get_next_arrival_time(timestep)) #Programa a chegada seguinte
        manager.handle_queue(fila1,servidor)

        if debugging: #Logging para debug do código

            print('-'*30)
            print(f't:{timestep}')
            if next_arrival:
                print(f'Próxima chegada configurada para {next_arrival}')
            if customer is not None:
                print(f'Fregues {customer.id} chegou na fila 1')
            if servidor.is_busy():
                finish_time = round(servidor.get_current().get_estimated_finish())
            print(f'Fila 1: {Fila.filas[0].get_queue()}')
            print(f'Fila 2: {Fila.filas[1].get_queue()}')
            print(f'Servidor: {servidor.get_current()} , fim do serviço em {finish_time}')
            tm.sleep(0.5)
            
        manager.handle_server(servidor)



        clock.tick_clock()#avança unidade de tempo
        if timestep == time_horizon:
            print('Fim da simulação')
            break



if __name__ == '__main__':
    run(0.6,time_horizon=20,debugging= True)