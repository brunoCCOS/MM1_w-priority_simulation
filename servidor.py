import random 
import numpy as np
import simulation
from cliente import Client
from fila import Fila
rng = np.random.default_rng(42)

class Service:
    '''
    Classe de criação das instancias do servidor
    '''
    def __init__(self,service):
        self.service_time = service #tempo de serviço usado
        self.current = None #Cliente na file
    
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
        if self.current is None: #Caso a fila esteja vazia
            queue_in = Fila.filas[customer.get_priority()-1]
            queue_in.consume_costumer()
            self.start_new_costumer(customer,time)
            return (0,customer)
        elif self.current.get_priority() > customer.get_priority(): #Caso a prioridade do cliente novo seja maior que a do atual
            queue_out = Fila.filas[self.current.get_priority()-1]
            queue_in = Fila.filas[customer.get_priority()-1]
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
        return current_
        
    def get_current(self):
        return self.current