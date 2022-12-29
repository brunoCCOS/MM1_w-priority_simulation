import numpy as np
class Client():
    '''
    Classe para manipulação do freguês
    '''
    id = 0
    def __init__(self,fila,time,_id = None):
        if _id is None:
            self.id = int(Client.id)
            Client.id += 1  
        else:
            self.id = _id
        self.served_time = 0 #tempo servido
        self.queue_time = 0 #tempo na fila
        self.queue = fila #fila que se encontra
        self.last_arrival_time = time #instante da ultima vez que entrou na fila
        self.total_time = 0
        self.service_residual = np.inf
        self.last_start_served_time = np.inf#instante da ultima vez que entrou no servidor
    def get_in_server(self,service,time):
        '''
        Define o inicio do atendimento do fregues
        '''
        self.last_start_served_time = time
        self.queue_time += time - self.last_arrival_time
        if self.service_residual == np.inf:
            self.service_residual = service
    def leave_server(self,time):
        '''
        Retira o fregues da fila e retorna o tempo servido
        '''
        self.served_time = time - self.last_start_served_time
        self.last_arrival_time = time#Reinicia o ultimo instante na fila
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
    def leave_queue(self,time):
        '''
        Encerra ciclo do freguês na fila
        '''
        self.leave_server(time)
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
    def get_estimated_finish(self):
        '''
        Retorna o instante t que o serviço deve acabar caso não seja interrompido
        '''
        return self.service_residual + self.last_start_served_time
    def get_id(self):
        '''
        Retorna o id do freguês
        '''
        return self.id