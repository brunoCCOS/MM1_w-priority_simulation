## Cliente.py



Contem a  classe que atribui e implementa as funções e atributos relacionados ao cliente



Atributos:

```
        id #id do cliente
        served_time #tempo servido
        queue_time#tempo na fila
        queue#fila que se encontra
        last_arrival_time  #instante da ultima vez que entrou na fila
        total_time #tempo total no sistema
        service_residual #tempo residual
        last_start_served_time #instante da ultima vez que entrou no servidor
```



Métodos:

```
def get_in_server(self,service,time):
        '''
        Define o inicio do atendimento do fregues
        '''

    def leave_server(self,time):
        '''
        Retira o fregues da fila e retorna o tempo servido
        '''

    def change_queue(self,queue):
        '''
        Muda o fregues de fila
        '''

    def get_priority(self):
        '''
        Retorna prioridade do fregues
        '''

    def get_queue_id(self):
        '''
        Retorna prioridade do fregues
        '''

    def leave_queue(self,time):
        '''
        Encerra ciclo do freguês na fila
        '''

    def get_total_time(self):
        '''
        Retorna total_time do fregues
        '''

    def get_served_time(self):
        '''
        Retorna served_time do fregues
        '''

    def get_queue_time(self):
        '''
        Retorna queue_time do fregues
        '''

    def get_service_residual(self):
        '''
        Retorna tempo de serviço residual
        '''

    def get_estimated_finish(self):
        '''
        Retorna o instante t que o serviço deve acabar caso não seja interrompido
        '''

    def get_id(self):
        '''
        Retorna o id do freguês
        '''


    def get_last_start_served_time(self):
        '''
        Retorna o último instante que entrou no servidor
        '''

    def reset():
        '''
        Retorna o estado inicial da classe
        '''

```



## Fila.py

Contem a  classe que atribui e implementa as funções e atributos relacionados a fila



Atributos:

```
    id #1-index base*

​    busy_time #parametro rho*

​    priority_order#prioridade da fila*

​    arrival_time #tempo de chegada*

​    queue #Lista de clientes na fila

​    weighted_number_costumers *#lista do número pessoas ponderada pelo tempo, serve pois como não iteramos os instantes temos que pesar cada coleta pelo tempo que ficou no estado*

​    number_customers *#número de pessoas na fila*

​    next_arrival # Tempo da próxima chegada

​    last_chg_time *#Momento da última chegada ou partida da fila*
```



Métodos:

```
def arrive_customer(self,time):
        '''
        Anuncia chegada de novo freguês na fila
        '''

def insert_costumer(self,time,id):
'''
Equivalente a arrive_costumer porém dessa vez invés de um 
cliente novo é inserido um freguês arbitrário
'''

def kick_out(self,customer,time):
'''
Anuncia para a fila que um dos seus fregueses foi expulso do servidor e retorna ele para primeira posição
'''


def consume_costumer(self,time):
'''
Consome um fregues da fila de espera
'''

def get_next(self):
'''
Retorna o próximo fregues da fila
'''


def get_next_arrival_time(self):
'''
Retorna a próxima chegada configurada
'''


def set_next_arrival_time(self,t):
'''
Define a próxima chegada na fila para um t específico
'''


def generate_next_arrival_time(self,time):
'''
Programa a próxima chegada na fila
'''


def get_last_arrival_time(self):
'''
Retorna o tempo da última chegada à fila
'''


def get_last_depart_time(self):
'''
Retorna o tempo da última partida à fila
'''


def get_number_customers(self):
'''
Retorna o número de pessoas na fila
'''

def get_weighted_number_costumers(self):
'''
Retorna o número de pessoas na fila ponderado
'''


def get_id(self):
'''
Retorna o id da fila
'''


def get_queue(self):
'''
Retorna a lista de fregueses na fila
'''


def get_priority(self):
'''
Retorna a prioridade da fila
'''



def reset():
'''
Retorna o estado inicial da classe
'''
```



## Servidor.py

Contem a  classe que atribui e implementa as funções e atributos relacionados ao servidor



Atributos

```
        service_time #tempo de serviço usado
        current  #Cliente na file
        last_ended_job#TEmpo que o último serviço foi finalizado
        empty_time  #Tempo vazio do servidor
```



Métodos:

```
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
            queue_in.consume_costumer(time)
            self.start_new_costumer(customer,time)
            return (0,customer)
        elif self.current.get_priority() > customer.get_priority(): #Caso a prioridade do cliente novo seja maior que a do atual
            queue_out = Fila.filas[self.current.get_queue_id()-1]
            queue_in = Fila.filas[customer.get_queue_id()-1]
            queue_out.kick_out(self.current,time)
            queue_in.consume_costumer(time)
            self.start_new_costumer(customer,time)
            return (1,self.current)
        else: #Cliente permanece em espera e retorna flag de ocupado
            return (2,customer)
    
    def end_service(self,time):
        '''
        Encerra o periodo do cliente no servidor sinalizando a fila para repassar o cliente
        '''
        
    def get_current(self):
        '''
        Retorna o fregues atual
        '''


    def is_busy(self):
        '''
        Retorna o status do servidor se está ocupado ou não
        '''

```



### Statistics.py

Contem a  classe que atribui e implementa as funções e atributos relacionada ao calculo das estatisticas do simulador



Atributos

```
```



Métodos:

````
   def calc_mean(data):
        '''
        Calcula a méida de um conjunto de amostras
        '''

    
    def calc_var(data):
        '''
        Calcula a variança de um conjunto de amostras
        '''

    
    def calc_inc_mean(mean,samples,nsamples):
        '''
        Calcula a méida de um conjunto de amostras incrementalmente
        '''

    
    def calc_inc_var(old_mean,var,samples,nsamples):
        '''
        Calcula a variança de um conjunto de amostras incrementalmente
        '''
        

    
    def calc_std(data):
        '''
        Calcula o desvio padrão de um conjunto de amostras
        '''
  
    def calc_conf_int(data,conf=0.95,dist = "t"):
        '''
        Calcula o intervalo de confiança usando uma distribuição específica
        '''


    def calc_precision(upper,lower):
        '''
        Calcula a precisão de um dado intervalo de confiança
        '''

    def plot_hist(x,title,label_x,label_y,save = False):
        '''
        Plota histogram de dados
        '''


    def plot_scatter(x,title,label_x,label_y,save = False):
        '''
        Plota gráfico de dispersão de dados
        '''
            
    def plot_line(x,title,label_x,label_y,save = False):
        '''
        Plota linha de dados
        '''

    
    def print_full_statistics(results,means,vars,plots = True):
        '''
        Printa todas as estatisticas a respeito das métricas
        '''


````



### Simulation.py

Contem as  classes que atribuem e implementam as funções e atributos relacionados ao funcionamento da simulação



##### Classe Clock

​	Atributos:

```
        self.time = 0.0 #Tempo atual
        self.last_saved_time = 0.0 #Último tempo salvo
```

​	Métodos:

```
    def tick_clock(self):
        '''
        Avança uma unidade de tempo no contador
        '''

    def get_time(self):
        '''
        Retorna o tempo atual
        '''


    def get_saved_time(self):
        '''
        Retorna o tempo salvo
        '''

    
    def save_time(self):
        '''
        Salva o tempo atual
        '''
        self.last_saved_time = self.time
    
    def set_time(self,time):
        '''
        Define um tempo especifico pro relógio
        '''

```



#### Manager

​	Atributos:

```
self.clock = clock
        self.records #Dicionario de registros das estatisticas coletadas
        self.next_event = 0 #tempo do próximo evento
```

​	Métodos:

```
 def handle_queue(self,fila,service):
        '''
        Serviço de verificação e tratamento das pendencias das filas de espera
        '''


    def handle_server(self,service):
        '''
        Serviço de verificação e tratamento das pendencias do servidor
        '''


    def handle_costumer(self,costumer):
        '''
        Serviço de tratamento do freguês após deixar o servidor
        '''

    def handle_clock(self,fila,servidor):
        '''
        Serviço de tratamento do tempo de simulação, verifica qual o próximo evento(fim de serviço ou chegada de fregues) e 			avança até ele
        '''


    def get_records(self):
        '''
        Retorna histórico de coleta dos fregueses
        '''

    def set_busy_time(self,time):
        '''
        Calcula o tempo de ocupação da fila e o número de pessoas total no servidor pra cada fila
        '''
       
    def get_n_customers(self):
        '''
        Retorna o número de fregueses que já passaram pelo sistema
        '''

```



### Main.py

Função principal que orquestra e organiza a simulação e componentes