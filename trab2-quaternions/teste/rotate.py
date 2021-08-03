#ANA LUIZA MARTINS CESARIO - Nº USP 11811291
from quaternions import Quaternions #importando o módulo pedido, quaternions
import math #importando módulo math

class Cube(): #classe Cubo
    #passa o objeto e cria os vértices
    def __init__ (self,x,y,z): #construtor da classe Cubo com as variaveis x, y e z
    #cria um vértice do cubo
        self.x = x
        self.y = y
        self.z = z
    
    def __str__(self): #método str para a classe cube
        s = "[" + str(self.x) +" ,"+ str(self.y) +" ,"+ str(self.z)+"]"
        return s
    
    def callRotate(self): #função para pedir novo angulo e novo eixo de rotação
        #passa os vértices obtidos na ultima rotação
        print("Insira o vetor de rotação v, na forma:\n 'x y z'")
        V = list(float(x) for x in input().split())

        print("Caso queirar parar o programa digite 0 0 0 no vetor de rotação, na próxima rotação")
        if(V[0] == 0 and V[1]==0 and V[2]==0):
            print("Fim")
        else:
            print("Digite o angulo de rotação, em graus")
            a = input()
            c = float(a)
            alpha = math.radians(c)
            Cube.rotate(self, V, alpha) 
            #chama a função rotate com os vértices obtidos na ultima rotação e roda o cubo novamente
        
    def findR(self, alpha): #função para encontrar R, sem poluir a função rotate
        Vrotate = Quaternions(0,self[0],self[1],self[2])
        r = Quaternions(0,0,0,0)
        ang = alpha/2
        normaV = Quaternions.norma(Vrotate)
        n = 1.0/normaV
        r.q = math.cos(ang)
        r.i = (math.sin(ang))**(1/normaV)*self[0]
        r.j =  (math.sin(ang))**(1/normaV)*self[1]
        r.k =  (math.sin(ang))**(1/normaV)*self[2]
        return r   

    def rotate(Cubeslist, v, alpha): #função para rotacionar o cubo
        #realiza a maior parte do trabalho  do programa
        #recebe os vétrices do cubo, o vetor de eixo e o angulo 
        r = Cube.findR(v,alpha) #função para encontrar r, ao inves de deixar aqui
        # todas as operações nessa função, r é um valor consante
        invR = Quaternions.inverso(r) #inverso de r
        quats = []
        for i in range(8):
            quats.append(Cube.PointToQuaternion(Cubeslist[i]))
           #Trasforma os pontos em quaternions
        newP, p1 = [],[] # newP grarda o resultado, p1 é uma lista temporária

        temp = Quaternions(0,0,0,0)
        for i in range(8):
            temp = (r*quats[i])*invR
            p1.append(temp)
            newP.append(Cube.QuaternionToPoint(p1[i]))
            #print("NewP" + str(i)+": " + str(newP))
            #cubo girado
            print(str(newP[i]))

        #chama a função callRotate para pedir o novo angulo e o novo eixo de rotação
        Cube.callRotate(newP)
        
    #Passar o quaternion resultante para Ponto x,y,z, para apresentar os resultados
    def QuaternionToPoint(self): 
        p = Cube(self.i,self.j,self.k)
        return p

    #Passar o ponto x,y,z para quaternion, para realizar a rotação 
    def PointToQuaternion(self): 
        q = Quaternions(0,self.x,self.y,self.z)
        return q

    #Função para criar os vértices do cube
    def CreateCube(self): 
        Cubeslist = [] #cria uma lista para colocar os vértices
        for i in range(8): 
            cube = Cube(0,0,0)
            cube = Cube(self[i][0],self[i][1],self[i][2])
            Cubeslist.append(cube)
        return Cubeslist

###### PROGRAMA PARA ROTACIONAR #####

#pontos iniciais do cubo
points = [[1.0, 1.0, 1.0], 
[1.0, 1.0, -1.0], 
[1.0,-1.0,1.0],  
[-1.0,1.0,1.0],
[1.0,-1.0,-1.0],
[-1.0,1.0,-1.0],
[-1.0,-1.0,1.0],
[-1.0,-1.0,-1.0]]

print("Insira o vetor de rotação v, na forma:\n 'x y z'")
v = list(float(x) for x in input().split())

print("Digite o angulo de rotação, em graus")
alpha = input()
alpha = math.radians(float(alpha))

cubes = Cube.CreateCube(points)
Cube.rotate(cubes, v, alpha)




