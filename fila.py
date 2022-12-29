from cliente import Client
import numpy as np
rng = np.random.default_rng()

class Fila:
    '''
    Classe de objetos do tipo Fila para simulação de ação e suass propriedades
    '''
    filas = [] # lista com todas as filas
    def __init__(self,busy,priority):
        self.id = len(Fila.filas) + 1 #1-index base
        self.busy_time = busy #parametro rho
        self.priority_order = priority #prioridade da fila
        self.arrival_time = busy/2 #tempo de chegada
        self.queue = []
        self.number_customers = 0
        Fila.filas.append(self)
    def arrive_customer(self,time):
        '''
        Anuncia chegada de novo freguês na fila
        '''
        customer = Client(self.id,time)
        self.number_customers += 1
        self.queue.append(customer)
        return customer
    def insert_costumer(self,time,id):
        '''
        Equivalente a arrive_costumer porém dessa vez invés de um 
        cliente novo é inserido um freguês arbitrário
        '''
        customer = Client(self.id,time,id)
        self.number_customers += 1
        self.queue.append(customer)
        return customer
    def kick_out(self,customer,time):
        '''
        Anuncia para a fila que um dos seus fregueses foi expulso do servidor e retorna ele para primeira posição
        '''
        self.queue.insert(0,customer)
        customer.leave_server(time)
        self.number_customers += 1
    def consume_costumer(self):
        '''
        Consome um fregues da fila de espera
        '''
        customer = self.queue[0]
        self.number_customers -= 1
        self.queue.pop(0)
        return customer
    def get_next(self):
        '''
        Retorna o próximo fregues da fila
        '''
        if self.queue:
            next = self.queue[0]
        else:
            next = None
        return next
    def get_next_arrival_time(self,time):
        '''
        Programa a próxima chegada na fila
        '''
        arrival = rng.exponential(scale=1/self.arrival_time) #Gera o tempo de serviço do cliente
        print(arrival)
        return time + arrival
    
    def get_queue(self):
        '''
        Retorna a lista de fregueses na fila
        '''
        return self.queue