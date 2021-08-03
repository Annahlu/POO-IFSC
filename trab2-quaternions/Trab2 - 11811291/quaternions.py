#ANA LUIZA MARTINS CESARIO - Nº USP 11811291
import math #importando o método math para funções matematico 

class Quaternions: #criação a classe quaternions
    def __init__(self,q,i,j,k): #contrutor da classe quaternions
        self.q = q #as variaveis são passadas por parâmetro para o construtor
        self.i = i 
        self.j = j
        self.k = k
    #self faz referência ao objeto "ele mesmo", o objeto passado

    def __str__(self): #definindo o método str
        if(isinstance(self, Quaternions) == True):  
        # se o objeto é da classe quaternions printa na forma a + bi + cj + dk  
        # verifica se o objeto é da classe quaternions por meio do método isinstace  
        #ininstance: verifica se o objeto é instancia de uma classe
            if(self.i >= 0):
                i = " +" + str(self.i) + "i"
            else:
                 i = " " + str(self.i) + "i"
            if(self.j >= 0):
                j =  " +" + str(self.j) + "j"
            else:
                j = " " + str(self.j) + "j"
            if(self.k >= 0):
                k =  " +" + str(self.k) + "k"
            else:
                k = " " + str(self.k) + "k"
            s = str(self.q) + i + j + k
            return s
        else:
            return str(self)
    
    def __add__(self,other): #sobreposição de operador para o operador soma
        #agora o sinal "+" entre dois quaternions executa este método
        temp = other # cria uma variavel temporario igual a other
        #verifica se é um numero real ou inteiro, se sim cria o quaternion correspondente
        if((isinstance(other, Quaternions) == False) and (type(other) != complex)):
            other = Quaternions(temp, 0, 0, 0)
        #verifica se é um numero complexo, se sim cria o quaternion correspondente
        elif(type(other) == complex):
            other = Quaternions(temp.real, temp.imag, 0, 0)

        r = Quaternions(0,0,0,0) #cria um objeto Quaternion para guardar o resulultado

        r.q = float(self.q) + float(other.q)  #cada parametro do objeto criado recebe a soma dos parametros dos objetos recebidos
        r.i = float(self.i) + float(other.i)
        r.j = float(self.j) + float(other.j)
        r.k = float(self.k) + float(other.k)
        return str(r) #retorna o método str
    
    def __radd__(self,other): #sobreposição de operador para o operador soma, a direita
        #agora o sinal "+" entre dois quaternions executa este método
        # a diferença está na interpretação do python
        # primeiro o interpretador tenta (a).__add__(b), se nao consegue, verifica se existe o radd
        #se sim, tenta (b).__add__(b)
        # a lógica é exatamente a mesma do método add, portanto não será reescrita
        temp = other 
        if((isinstance(other, Quaternions) == False) and (type(other) != complex)):
            other = Quaternions(temp, 0, 0, 0)
        elif(type(other) == complex):
            other = Quaternions(temp.real, temp.imag, 0, 0)
        r = Quaternions(0,0,0,0)
        r.q = float(self.q) + float(other.q) 
        r.i = float(self.i) + float(other.i)
        r.j = float(self.j) + float(other.j)
        r.k = float(self.k) + float(other.k)
        return str(r) #retorna o método str

    def __sub__(self,other): # igual ao __add_ mas para subtração
        temp = other 
        if((isinstance(other, Quaternions) == False) and (type(other) != complex)):
            other = Quaternions(temp, 0, 0, 0)
        elif(type(other) == complex):
            other = Quaternions(temp.real, temp.imag, 0, 0)
        r = Quaternions(0,0,0,0) 
        r.q = float(self.q) - float(other.q)  
        r.i = float(self.i) - float(other.i)
        r.j = float(self.j) - float(other.j)
        r.k = float(self.k) - float(other.k)
        return str(r) 
    
    def __rsub__(self,other): # subtração a esquerda
        temp = other 
        if((isinstance(other, Quaternions) == False) and (type(other) != complex)):
            other = Quaternions(temp, 0, 0, 0)
        elif(type(other) == complex):
            other = Quaternions(temp.real, temp.imag, 0, 0)
        r = Quaternions(0,0,0,0) 
        r.q = float(self.q) - float(other.q)  
        r.i = float(self.i) - float(other.i)
        r.j = float(self.j) - float(other.j)
        r.k = float(self.k) - float(other.k)
        return str(r) 
    
    def __mul__(self,other): 
        #sobreposição para o operador de multiplicação
        #realiza a multipicação em partes e soma as partes
        #a ordem das variaveis são diferentes
        temp = other
        if((isinstance(other, Quaternions) == False) and (type(other) != complex)):
            other = Quaternions(temp, 0, 0, 0)
        elif(type(other) == complex):
            other = Quaternions(temp.real, temp.imag, 0, 0)
        
        m = Quaternions(0,0,0,0)

        m.q = self.q*other.q - self.i*other.i - self.j*other.j - self.k*other.k
        m.i = self.q*other.i + self.i*other.q + self.j*other.k - self.k*other.j
        m.j = self.q*other.j - self.i*other.k + self.j*other.q + self.k*other.i 
        m.k = self.q*other.k + self.i*other.j - self.j*other.i + self.k*other.q
        return m
        

    def __rmul__(self,other):
        #sobreposição para o operador de multiplicação, a esquerda
        #a multiplicação não é comutativa
        #realiza a multipicação em partes e soma as partes
        #a ordem das variaveis são diferentes
        temp = other
        if((isinstance(other, Quaternions) == False) and (type(other) != complex)):
            other = Quaternions(temp, 0, 0, 0)
        elif(type(other) == complex):
            other = Quaternions(temp.real, temp.imag, 0, 0)
        
        m = Quaternions(0,0,0,0)
        
        m.q = self.q*other.q - self.i*other.i - self.j*other.j - self.k*other.k
        m.i = self.q*other.i + self.i*other.q + self.j*other.k - self.k*other.j
        m.j = self.q*other.j - self.i*other.k + self.j*other.q + self.k*other.i 
        m.k = self.q*other.k + self.i*other.j - self.j*other.i + self.k*other.q
        return m
       
    
    def __truediv__(self,other): #divisao de quaternions
        #truediv é a divisão sem truncamento, enquanto o div corresponde a //, a divisao truncada
        temp = other
        if((isinstance(other, Quaternions) == False) and (type(other) != complex)):
            other = Quaternions(temp, 0, 0, 0)
        elif(type(other) == complex):
            other = Quaternions(temp.real, temp.imag, 0, 0)
        return self * (other.inverso())
        
        
    def __rtruediv__(self,other): #divisao de quaternions a esquerda
        #realiza a mesma operação porem a ordem mudou
        temp = other
        if((isinstance(other, Quaternions) == False) and (type(other) != complex)):
            other = Quaternions(temp, 0, 0, 0)
        elif(type(other) == complex):
            other = Quaternions(temp.real, temp.imag, 0, 0)
        return self * (other.inverso())

    def conjugado(self): #retorna o conjugado do Quaternion passado
        qconj = Quaternions(0,0,0,0)
        qconj.q = self.q 
        qconj.i = (-1)*self.i 
        qconj.j = (-1)*self.j 
        qconj.k = (-1)*self.k #multiplica as coordenadas não reais por -1
        return qconj 

    def multconj(self): # multiplicar um numero pelo seu conjugado
        q = (self.q)**2 + (self.i)**2 + (self.j)**2 + (self.k)**2
        return q

    def inverso(self): #inverso de um quaternion 
        qconj = Quaternions.conjugado(self)
        qprod = Quaternions.multconj(self)
        qinv = (1.0/qprod)*(qconj)
        return qinv

    def norma(self): #norma do quaternion
        norma = math.sqrt(Quaternions.multconj(self))
        # tira a raiz do retorno da função de multplicação de quaternion por ele mesmo
        return norma
