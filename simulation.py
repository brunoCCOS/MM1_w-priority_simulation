from fila import Fila
from math import isclose
class Clock():
    '''
    classe para controlar e regular passagem de tempo
    '''
    def __init__(self):
        self.time = 0

    def tick_clock(self):
        '''
        Avança uma unidade de tempo no contador
        '''
        self.time += 1

    def get_time(self):
        '''
        Retorna o tempo atual
        '''
        return self.time

    def set_time(self,time):
        '''
        Define um tempo especifico pro relógio
        '''
        self.time = time 

class Manager():
    '''
    Classe para gerenciar dos eventos da fila e coletar as estatisticas
    '''
    def __init__(self,clock):
        self.clock = clock
        self.records = dict({
            'W1':[],
            'W2':[],
            'W':[],
            'S1':[],
            'S2':[],
            'S':[],
            'T1':[],
            'T2':[],
            'T':[]
        })
    def handle_queue(self,fila,service):
        '''
        Serviço de verificação e tratamento das pendencias das filas de espera
        '''
        customer = fila.get_next()
        if customer is not None:
            #Verifica como tratar o próximo da fila
            status = service.arrive_costumer(customer,self.clock.get_time())
            return status

    def handle_server(self,service):
        '''
        Serviço de verificação e tratamento das pendencias do servidor
        '''
        current = service.get_current() #Recupera cliente atual no servidor
        if current is not None:
            #Calcula e verifica quando deve terminar p encerrar o serviço
            finish_time = round(current.get_estimated_finish()) 

            if self.clock.get_time() == finish_time: #se tiver terminado o serviço
                current = service.get_current()
                service.end_service(self.clock.get_time())
                self.handle_costumer(current) #trata o fregues finalizado

    def handle_costumer(self,costumer):
        '''
        Serviço de tratamento do freguês após deixar o servidor
        '''
        if costumer.get_priority()<len(Fila.filas):# se não for da última fila
            queue = Fila.filas[costumer.get_priority()]
            #Salva as métricas da fila 1
            self.records['W1'].append(costumer.get_queue_time())
            self.records['S1'].append(costumer.get_served_time())
            self.records['T1'].append(self.records['W1'][costumer.get_id()] + self.records['S1'][costumer.get_id()])
            queue.insert_costumer(self.clock.get_time(),costumer.get_id())
        else:
            #Calcula as métricas da fila 2 e final
            self.records['W2'].append(costumer.get_queue_time())
            self.records['S2'].append(costumer.get_served_time())
            self.records['T2'].append(self.records['W2'][costumer.get_id()] + self.records['S2'][costumer.get_id()])
            self.records['W'].append(self.records['W1'][costumer.get_id()] + self.records['W2'][costumer.get_id()])
            self.records['S'].append(self.records['S2'][costumer.get_id()] + self.records['S1'][costumer.get_id()])
            self.records['T'].append(self.records['W'][costumer.get_id()] + self.records['S'][costumer.get_id()])
    
    def get_records(self):
        '''
        Retorna histórico de coleta dos fregueses
        '''
        return self.records
    
def Statistcs():
    '''
    Classe para geração e informe de estatistícas
    '''