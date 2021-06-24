####### ANA LUIZA MARTINS CESARIO - Nº USP 11811291

import sys # importando sys 
import numpy as np # importando numpy
#numpy permite trabalhar com arrays e matrizes e o problema envolve strings, ou seja, arrays de caracteres

########## FUNÇÕES ############

#Função string para dicionario
def string_to_dict(S): #recebe a palavra S
    S = np.array(list(S)) # mapeia a lista de palavras S para um vetor numpy de palvras, também chamado S
    d = {} #cria um dicionario
    for s in np.unique(S): #a função np.unique separa os elementos únicos do array
        d[s] = np.sum(S == s) # coloca  a quantidade de elementros de S na posição s do dicionário
    return d # retorna o dicionário

    #a biblioteca numpy é útil pois sem ela nao poderiamos comparar e somar S com s,
    # pois um é um caractere e o outro é uma lista de caracteres, mas o numpy entende essa comparação as soma

    
def isanagrama(p1, p2):
    return string_to_dict(p1) == string_to_dict(p2) # true se as duas palavras são anagramas e false se não
    #estamos os dicionarios gerados a partir de cada palavra 
    #se duas palavras tem o mesmo numero de letras iguais, elas são anagramas

def anagrama(P): #analisar se as palavras são anagramas umas das outras ou não
    sizes = np.array(list(map(lambda x : len(x), P))) # [1]
    ascii_sums = np.array(list(map(lambda x : np.sum(list(map(ord,list(x)))), P))) #[2]
    ascii_prods = np.array(list(map(lambda x : np.prod(list(map(ord,list(x)))), P))) # [3]
    passed = np.zeros(len(P)) # [4]
    i = 0
    palavras = [] 
    for p1 in P:
        if(passed[i] == 0): # [5]
            anagramas = [p1] # [6] 
            passed[i] = 1 # [7]
            pos = np.where((sizes == sizes[i]) & (passed == 0) & (ascii_sums == ascii_sums[i]) & (ascii_prods == ascii_prods[i]))[0] #[8]
            for j in pos:
                if(isanagrama(p1, P[j])): #[9]
                    anagramas.append(P[j]) # [10]
                    passed[j] = 1
            palavras.append(anagramas) #[11]
        i += 1
    return palavras #[12]

    #Para não ficar muito poluido, vou comentar cada linha da função anagrama com base nos indices [k] que coloquei

    # [1]: uma função lambda é uma função temporária que não precisa ser escrita separadamente,
    # como queremos executar uma ação simples, ela foi usada.
    #  A função map executa uma função para cada elemento de uma lista, ou de um iterável qualquer,
    # além de saber qual o tamanho de cada palavra eu também quero salva-lo, então usei um list,
    # coloca cada resultado do map em uma posição da lista, e por fim essa lista é passada para um vetpr numpy
    # e chamada de sizes

    #[2]: Na linha 2 foram usados os mesmos conceitos de função lambda e map porem com a função ord, que retorna um código
    # unico para cada caractere, chamado de unicode. Depois todos os unicodes são somados e colocados no vetor numpy ascii_sum,
    # cada unicode representa o código ascii de um caractere
    
    #[3]: O mesmo processo é repetido, entretanto estamos multiplicando os unicodes ao invés de somá-los

    #[4]: por fim criamos um vetor de zeros com np.zeros com o mesmo tamanho do numero de palavras, esse vetor será util 
    # para sinalizar se uma palavra já foi comparada com outras ou não

    #[5]: um if para prevenir que o programa analise a mesma palavra duas vezes

    #[6]: coloca a palavra p1 na variável anagramas

    #[7]: seta 1 para a palavra analisada nesta vez

    #[8]: Preferi separar o comando 8 em partes para explicar melhor.
    # [8.1] z = (sizes == sizes[i]) & (passed == 0) & (ascii_sums == ascii_sums[i]) & (ascii_prods == ascii_prods[i])
    # [8.2] pos = np.where(z)[0]
    #
    # [8.1] z = (sizes == sizes[i]) & (passed == 0) & (ascii_sums == ascii_sums[i]) & (ascii_prods == ascii_prods[i])
    # Retorna true para cada elemento da lista que atende a todas as condições senso elas: 
    # as duas palavras precisam ter o mesmo tamanho  -  sizes == sizes[i]
    # a palavra não pode ter sido analisada ainda - passed == 0
    #  A soma dos elementos precisa ser igual nas duas palavras - ascii_sums == ascii_sums[i]
    # O produto precisa ser igual nas duas palavras - ascii_prods == ascii_prods[i]
    # - É possível comparar sizes e sizes[i] pois sizes é um vetor do tipo numpy, que permite esse tipo de comparação 
    # sem especificar o índice
    #
    #[8.2] pos = np.where(z)[0]
    # O comando np.where retorna uma lista com as posições onde as condições são satisfeitas
    # pos é um vetor 
    
    #[9]: chama a função isanagrama com a palavra p1 e a palavra no vetor P na posição j

    #[10]: adiciona a palavra no vetor anagramas

    #[11]: retorna anagramas no vetor palavras

def save(v, filename): #função para salvar o 
    f = open(filename, "w", encoding='utf-8') # abre o aquivo f

    for l in v: #para cada linha do vetor v:
        f.write(', '.join(l)) #acrescenta a virgula entre as palavras
        f.write('\n') #quebra a linha

    f.close() #fecha o aquivo

########## RODANDO O CÓDIGO - CHAMANDO AS FUNÇÕES #############

filename = sys.argv[1] #pegando o nome do aqruivo que foi passado na linha de comando

f = open(filename, encoding='utf-8') #abrindo o aquivo 
x = list(map(lambda x : x.replace('\n','').lower(), f.readlines())) # [1]
#[1]: x é uma lista gerada a partir do map que executa uma função temporária lambda que tira a quebra de linha (\n),
# passa tudo para letra minuscula das linhas do aquivo f
v = anagrama(x) # chamando a função anagrama para a lista x
save(v, filename+".ana") # salvando o arquivo nome pedido 


