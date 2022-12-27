from simulation import Clock
import numpy as np
class Client():
    '''
    Classe para manipulação do freguês
    '''
    id = 0
    def __init__(self,fila):
        self.id = Client.id
        Client.id += 1
        self.served_time = 0 #tempo servido
        self.queue_time = 0 #tempo na fila
        self.queue = fila #fila que se encontra
        self.last_arrivel_time = Clock.get_time() #instante da ultima vez que entrou na fila
        self.total_time = 0
        self.service_residual = np.inf
    
    def get_in_server(self,service):
        '''
        Define o inicio do atendimento do fregues
        '''
        self.last_start_served_time = Clock.get_time() 
        self.queue_time += Clock.get_time() - self.last_arrivel_time
        self.service_residual = service
    def leave_server(self):
        '''
        Retira o fregues da fila e retorna o tempo servido
        '''
        self.served_time = Clock.get_time() - self.last_start_served_time
        self.last_arrivel_time = Clock.get_time()#Reinicia o ultimo instante na fila
        self.service_residual -= self.served_time
        return self.served_time
    def change_queue(self,queue):
        '''
        Muda o fregues de fila
        '''
        self.queue = queue
    def get_priority(self):
        '''
        Retorna prioridade do fregues
        '''
        return self.queue
    def leave_queue(self):
        '''
        Encerra ciclo do freguês na fila
        '''
        self.total_time = self.queue_time + self.served_time
    def get_total_time(self):
        '''
        Retorna total_time do fregues
        '''
        return self.total_time
    def get_served_time(self):
        '''
        Retorna served_time do fregues
        '''
        return self.served_time
    def get_queue_time(self):
        '''
        Retorna queue_time do fregues
        '''
        return self.queue_time
    def get_service_residual(self):
        '''
        Retorna tempo de serviço residual
        '''
        return self.service_residual