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
    def start_new_costumer(self,customer):
        '''
        Função para iniciar um novo cliente na fila
        '''
        self.current:Client = customer
        service = rng.exponential(scale=self.service_time) #Gera o tempo de serviço do cliente
        self.customer.get_in_server(service)
    def arrive_costumer(self,customer):
        '''
        Função para tratamento da chegada de um novo consumidor
        '''
        if self.current is None: #Caso a fila esteja vazia
            self.start_new_costumer(customer)
            return 0
        elif self.current.get_priority() < customer.get_priority(): #Caso a prioridade do cliente novo seja maior que a do atual
            queue_out = Fila.filas[self.current.get_priority()]
            queue_in = Fila.filas[customer.get_priority()]
            queue_out.kick_out(self.current)
            queue_in.consume_costumer()
            self.start_new_costumer(customer)
            return 0
        else: #Cliente permanece em espera
            return 1
    def end_service(self):
        '''
        Encerra o periodo do cliente no servidor sinalizando a fila para repassar o cliente
        '''
        queue = Fila.filas[self.current.get_priority()]
        queue.repass_costumer()