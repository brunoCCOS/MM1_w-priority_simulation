from fila import Fila
from math import isclose
import numpy as np

class Clock():
    '''
    classe para controlar e regular passagem de tempo
    '''
    def __init__(self):
        self.time = 0.0
        self.last_saved_time = 0.0
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

    def get_saved_time(self):
        '''
        Retorna o tempo salvo
        '''
        return self.last_saved_time
    
    def save_time(self):
        '''
        Salva o tempo atual
        '''
        self.last_saved_time = self.time
    
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
            'T':[],
            'Nq1':[],
            'Nq2':[],
            'N1':[],
            'N2':[],
            'N': [],
            'rho':[]
        })
        self.next_event = 0
    def handle_queue(self,fila,service):
        '''
        Serviço de verificação e tratamento das pendencias das filas de espera
        '''
        last_saved = self.clock.get_saved_time() #Recupera último tempo salvo
        customer = fila.get_next()
        interval = self.clock.get_time() - last_saved
        if customer is not None:
            #Verifica como tratar o próximo da fila
            service.arrive_costumer(customer,self.clock.get_time())
        # print(fila.get_weighted_number_costumers())
        self.records[f'Nq{fila.id}'] = fila.get_weighted_number_costumers() #Registra os números de fregueses ponderados pelo tempo até o momento


    def handle_server(self,service):
        '''
        Serviço de verificação e tratamento das pendencias do servidor
        '''
        current = service.get_current() #Recupera cliente atual no servidor
        if current is not None:
            #Calcula e verifica quando deve terminar p encerrar o serviço
            finish_time = current.get_estimated_finish()

            if self.clock.get_time() == finish_time: #se tiver terminado o serviço
                current = service.get_current()
                service.end_service(self.clock.get_time())
                self.handle_costumer(current) #trata o fregues finalizado

    def handle_costumer(self,costumer):
        '''
        Serviço de tratamento do freguês após deixar o servidor
        '''
        if costumer.get_queue_id()<len(Fila.filas):# se não for da última fila
            queue = Fila.filas[costumer.get_queue_id()]
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
        self.records[f'N{costumer.get_queue_id()}'].append(costumer.get_served_time()) #Como nossa quantidade de fregueses é ponderada pelo tempo cada fregues que termina seu
        #serviço tem seu tempo em serviço adicionado a lista 1*served_time
    def handle_clock(self,fila,servidor):
        '''
        Serviço de tratamento do tempo de simulação, verifica qual o próximo evento(fim de serviço ou chegada de fregues) e avança até ele
        '''
        self.clock.save_time() # salva o tempo para o próxima iteração
        #Verifica qual o próximo evento
        prox_chegada = fila.get_next_arrival_time()
        if servidor.is_busy():
            fim_servico = servidor.get_current().get_estimated_finish()
            if fim_servico < prox_chegada:
                time = fim_servico
            else:
                time = prox_chegada
        else:
            time = prox_chegada
        if time == np.inf: #Se estiver configurado para parar
            time = self.clock.get_time()
        self.clock.set_time(time) #Avança o tempo

    def get_records(self):
        '''
        Retorna histórico de coleta dos fregueses
        '''
        return self.records
    def set_busy_time(self,time):
        self.records['rho'].append(sum(self.records['S'])/time)
         #Appenda os valores da fila de espera
        self.records['N1'] += self.records['Nq1']
        self.records['N2'] += self.records['Nq2']
        self.records['total_time'] = [self.clock.get_time()]
    def get_n_customers(self):
        '''
        Retorna o número de fregueses que já passaram pelo sistema
        '''
        return self.customers