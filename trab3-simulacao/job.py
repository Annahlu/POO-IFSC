# Ana Luiza Martins Cesario - nº USP: 11811291
###################### Trabalho 3 - simulação #############################

'''Não foram feitos tantos comentarios, tanto porque usei o arquivo base da simulação do banco
quanto porque algumas funções são autoexplicativas agora no fim da disciplina'''

#importando as bibliotecas e arquivos necessarios
from abc import ABC, abstractmethod
import random
from collections import namedtuple
from queue import Queue
import sys
from desimul import Calendar, Event, Server

class Job():
    #work - duração, quantidade de trabalho
    #priority: 1 ou 0 
    def __init__(self, duracao, priority):
        self._priority = priority
        self._total_work = duracao
        self._arrival_time = None
        self._departure_time = None

    #métodos que setam atributos ou os retornam:
    #retorna a prioridade
    def priority(self):
        return self._priority

    #funções de tempo
    #arrival e departure: controle do tempo de chegada e saída
    def arrival(self, time):
        self._arrival_time = time
    
    def departure(self, time): 
        self._departure_time = time

    def start_time(self):
        #tempo inicial = partida - duração
        return self._departure_time - self._total_work
  
    def report(self):
        #tempo inicial = final - duração
        return self._departure_time, self._arrival_time

    def work(self):
        #gerado pela distribuição gaussiana com os parâmetros dados
        #duracao do processamento
        return self._total_work

class QueueingSystem(ABC, Server):
    #Herda da classe Server, para que seja definido um sistema de filas

    def __init__(self, calendar):
        Server.__init__(self, calendar)
        self._free_processors = Queue()

    #quando um novo job é criado, verifica se existe algum processador livre
    # se sim, manda para ele, senão coloca na fila
    def new_job(self, job):
        if self._free_processors.empty():
            self.enqueue(job)
        else:
            processor = self._free_processors.get()
            calend = self.calendar()
            current_time = calend.current_time()
            event = JobToprocessorEvent(current_time, processor, job)
            calend.put(event)

    def free_processor(self, processor):
        #verifica se existe algum processador livre
        #verifica se existe algum job na fila, se sim manda para o processador
        #se existe algum processador livre o coloca na lista de processadores
        if self.has_waiting_job():
            job = self.get_next_job()
            calend = self.calendar()
            current_time = calend.current_time()
            #cria um objeto evento da classe JobToProcessorEvent
            event = JobToprocessorEvent(current_time, processor, job)
            calend.put(event)
        else:
            self._free_processors.put(processor)

    #métodos abstratos que serão instanciados nas classes depois
    @abstractmethod
    def enqueue(self, job):
        pass

    @abstractmethod
    def has_waiting_job(self):
        pass

    @abstractmethod
    def get_next_job(self, processor):
        pass

class PriorityQueue(QueueingSystem):
  #Sistema de filas que leva em conta a prioridade das tarefas

    def __init__(self, calendar):
        QueueingSystem.__init__(self, calendar)
        #cria uma namedTuple para guardar a prioridade
        Queues = namedtuple('Queues', ['ap', 'normal'])
        #Adiciona um objeto Queues ao self._Queues
        self._queues = Queues(ap = Queue(), normal = Queue())

    def enqueue(self, job):
        #instancia do método abstrato criado anteriormente
        #colocar na fila
         if(job.priority() == 1):
            self._queues.ap.put(job)
         else:
            self._queues.normal.put(job)

    def has_waiting_job(self):
        #verifica se ja existe alguem na fila
        if((self._queues.ap.empty()) and (self._queues.normal.empty()) == True):
            return False
        else:
            return True

    def get_next_job(self):
        #pega o próximo job de acordo com a prioridade
        #sempre o de alta prioridade, depois os normais
        if(self._queues.ap.empty() == False):
            return self._queues.ap.get()
        else:
            return self._queues.normal.get()
       
class Processor(Server):
    #Processador, herda do Server
    def __init__(self, calendar, queue):

        Server.__init__(self, calendar)
        self._queue = queue
        self._free_time = []
        self._last_attending = 0.0
        self.n_jobs = 0
        self.n_jobs_ap = 0
        self.n_jobs_normal = 0

    def attend_job(self, job):

        curr_time = self.calendar().current_time()
        self._free_time.append(curr_time - self._last_attending)
        time_to_finish = job.work()
        finish_time = curr_time + time_to_finish
        
        event = processorFreeEvent(finish_time, self._queue, self)
        self.calendar().put(event)
        self._last_attending = finish_time

        #define o tempo final do job
        job.departure(finish_time)

        #conta o job na sua respectiva categoria
        self.add_job(job)

    def free_times(self):
        #conta quanto tempo o processador ficou livre
        return self._free_time
    
    def add_job(self, job):
        #método para contar um novo job
        AP = job.priority()

        if (AP == 1):
            self.n_jobs_ap += 1
        else:
            self.n_jobs_normal += 1

        self.n_jobs += 1

# Event types - define os eventos de chegada e saida 
# Dos processadores e dos jobs

class JobArrivalEvent(Event):
    #job chegou
    def __init__(self, time, queue, job):
        Event.__init__(self, time, queue)
        self._job = job
        #cria um atributo job para que seja possivel pegar um por um

    def process(self):
        self._job.arrival(self.time())
        self.server().new_job(self._job)
        #processar a tarefa

    def job(self):
        #job agora como método da classe
        return self._job

class JobToprocessorEvent(Event):
#job a ser processado
    def __init__(self, time, processor, job):
        Event.__init__(self, time, processor)
        self._job = job
        #mesma coisa do outro 

    def process(self):
        self.server().attend_job(self._job)

class processorFreeEvent(Event):

    def __init__(self, time, queue, processor):
        Event.__init__(self, time, queue)
        self._free_processor = processor

    def process(self):
        #verificar se um processador está livre ou não
        self.server().free_processor(self._free_processor)
    

# Simulações
Job_par = namedtuple('Job_par', ['total', 'work', 'arrival', 'priority'])
Processor_par = namedtuple('Processor_par', ['total'])

#a tupla de jobs é composta por: numero total de jobs, duração = work, chegada = arrival e prioridade
#só é necessario conhecer o numero de processadores, pois ao contrário do código do banco
#os processadores nao possuem taxas de trabalho (eficiencia) diferentes, é sempre a mesma

#uma namedTuple permite acessar as posições pelo seu nome, uma espécie de objeto, ao invés de indices como listas
#ou tuplas comuns

# Funções para gerar o relatório
def write_job_data(jobs):
   #vai gerar o relatorio sobre os jobs, escrever em um arquivo
    #a função job.report facilita muito o trabalho, pois nao é necessário pegar os tempos "na mão"
    #Criar e dar permissao de escrita ao arquivo
    with open('jobs.dat', 'w') as outfile:
        for job in jobs:
            saida, chegada = job.report()
            line = str(chegada) + " " + str(job.priority()) + " " + str(job.work()) + " " + str( job.start_time())
            print(line ,file=outfile)

def write_free_times(processors):
    #escrever os dados sobre os processadores
    #tempo livre e quantidade de tarefas executadas

    with open('processors.dat', 'w') as outfile:
        for p in processors:
            line = str(p.n_jobs) + " " + str(p.n_jobs_ap) + " " + str(p.n_jobs_normal) 
            print(line, end=' ',file=outfile)
            tempoLivreLista = p.free_times()
            for tempoLivre in tempoLivreLista:
                print(tempoLivre, end=' ', file=outfile)
            print(file=outfile)


def simple_simulation(filename, processors_p, jobs_p):
#roda o grosso da simulação
    calendar = Calendar()
    queue = PriorityQueue(calendar)

    # Cria os processadores
    processors = [Processor(calendar, queue)
               for i in range(processors_p.total)]

    # seta os processadores para estarem prontos para trabalhar
    for processor in processors:
        calendar.put(processorFreeEvent(0.0, queue, processor))

    # Criando Jobs
    jobs = [Job(jobs_p.work(i), jobs_p.priority(i)) for i in range(jobs_p.total)]

    # Jobs Chegando
    for i, job in enumerate(jobs):
        calendar.put(JobArrivalEvent(jobs_p.arrival(i), queue, job))

    #Processa todos os eventos, é do módulo desimul
    calendar.process_all_events()

    #Escreve os resultados
    write_job_data(jobs)
    write_free_times(processors)

    StringT = "Tempo total de simulação do arquivo com o sistema " + str(filename) + ": " + str(calendar.current_time()) + ""
    print(StringT)


if __name__ == '__main__':
    #Define o grosso da simulação, função main, principal do programa

     # Define as configurações da simulação
     #pega os parâmetros pedidos
    filename =  sys.argv[0]
    p = int(sys.argv[1])
    tau = float(sys.argv[2])
    sigma = float(sys.argv[3])
    T = float(sys.argv[4])
    m = int(sys.argv[5])
    alpha = float(sys.argv[6])

    #quantidade de tarefas pedidas
    ap = int(m//alpha)
    jobst = m+ap

    priority = [1 for i in range(ap)] #lista de tarefas com prioridade 1
    nonpriority = [0 for i in range(m)] #lista de tarefas sem prioridade (0)
    prioritylist = priority+nonpriority #junta as duas listas
    ordem = random.sample(prioritylist, len(prioritylist)) #cria uma lista na qual a prioridade é aletaoria
    #para que as tarefas não estejam sempre ordenadas
    #cria o par de simulação, igual no código base
    SIMUL_PAR = [
    ('PriorityQueue',
     Processor_par(p),
     Job_par(jobst,
     lambda i: abs(float(random.gauss(tau, sigma))),
     lambda i: random.random() * T,
     lambda i: ordem[i],
     ))]

    #Coloca a simulação para rodar
    for par in SIMUL_PAR:
        simple_simulation(par[0], par[1], par[2])
        #como só temos um tipo de simulação, uma fila, esse for rodará apenas 1 vez
