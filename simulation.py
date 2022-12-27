
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

class Manager():
    '''
    Classe para gerencia dos eventos da fila
    '''