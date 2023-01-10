import random 
import numpy as np
import simulation
from cliente import Client
from fila import Fila
rng = np.random.default_rng()

class Service:
    '''
    Classe de criação das instancias do servidor
    '''
    def __init__(self,service):
        self.service_time = service #tempo de serviço usado
        self.current = None #Cliente na file
        self.last_ended_job = 0 #TEmpo que o último serviço foi finalizado
        self.empty_time = 0 #Tempo vazio do servidor
    def start_new_costumer(self,customer,time):
        '''
        Função para iniciar um novo cliente na fila
        '''
        self.current:Client = customer
        service = rng.exponential(scale=self.service_time) #Gera o tempo de serviço do cliente
        customer.get_in_server(service,time)
        
    def arrive_costumer(self,customer,time):
        '''
        Função para tratamento da chegada de um novo consumidor
        '''
        if not self.is_busy(): #Caso a fila esteja vazia
            queue_in = Fila.filas[customer.get_queue_id()-1]
            queue_in.consume_costumer()
            self.start_new_costumer(customer,time)
            return (0,customer)
        elif self.current.get_priority() > customer.get_priority(): #Caso a prioridade do cliente novo seja maior que a do atual
            queue_out = Fila.filas[self.current.get_queue_id()-1]
            queue_in = Fila.filas[customer.get_queue_id()-1]
            queue_out.kick_out(self.current,time)
            queue_in.consume_costumer()
            self.start_new_costumer(customer,time)
            return (1,self.current)
        else: #Cliente permanece em espera e retorna flag de ocupado
            return (2,customer)
    
    def end_service(self,time):
        '''
        Encerra o periodo do cliente no servidor sinalizando a fila para repassar o cliente
        '''
        current_ = self.current
        current_.leave_server(time)
        current_.leave_queue(time)
        self.current = None
        self.last_ended_job = time
        return current_
        
    def get_current(self):
        '''
        Retorna o fregues atual
        '''
        return self.current

    def is_busy(self):
        '''
        Retorna o status do servidor se está ocupado ou não
        '''
        if self.current is not None:
            return True
        else:
            return False 