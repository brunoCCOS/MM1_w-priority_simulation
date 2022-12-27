from cliente import Client
class Fila:
    '''
    Classe de objetos do tipo Fila para simulação de ação e suass propriedades
    '''
    filas = [] # lista com todas as filas
    def __init__(self,busy,service,priority):
        self.id = len(Fila.filas) + 1 #1-index base
        self.busy_time = busy #parametro rho
        self.priority_order = priority #prioridade da fila
        self.arrivel_time = busy/2 #tempo de chegada
        self.queue = []
        self.number_customers = 0
        Fila.fila.append(self)
    def arrive_customer(self):
        '''
        Anuncia chegada de novo freguês na fila
        '''
        customer = Client(self.id)
        self.number_customers += 1
        self.queue.append(customer)
    def kick_out(self,customer):
        '''
        Anuncia para a fila que um dos seus fregueses foi expulso do servidor
        '''
        self.queue.insert(0,customer)
        customer.leave_server()
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
        '''R
        Retorna o próximo fregues da fila
        '''
        return self.queue[0]
    def repass_costumer(self,costumer):
        costumer.leave_server()
        costumer.leave_queue()
        return costumer