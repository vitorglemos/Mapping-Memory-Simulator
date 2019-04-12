
# coding: utf-8

# In[22]:


import math;
import random;
import string

class Memoria:
    
    def __init__(self, capacidadeMP, capacidadeCache, offset, mapeamento, diretorio, escalonamento, show_all):
        # Cálculo e Desenvolvimento da Arquitetura da Memória Principal e Cache
        self.show_all = show_all;
        self.digs = string.digits + string.ascii_letters
        self.capacidadeMP = capacidadeMP;
        self.capacidadeCache = capacidadeCache;
        self.offset = offset;
        self.mapeamento = mapeamento;
        self.diretorio = diretorio;
        self.armazenarResposta = [];
        self.tamanhoBloco = int(math.pow(2,self.offset));
        # Construção da Estrutura da Memória Principal
        self.totalMPBloco = int(math.log2(self.capacidadeMP/self.tamanhoBloco));
        self.ultimoBloco = int(math.pow(2,self.totalMPBloco)-1);
        self.ultimaPalavra = int(math.pow(2,self.offset)-1);
        self.MPArrayBloco = ["**B["+ str(i)+"] " for i in range(self.ultimoBloco + 1)];
        self.MPArrayPalavra = ["**W["+ str(i)+"] " for i in range(self.ultimaPalavra + 1)];
        self.escalonamento = escalonamento;
        
        if(self.mapeamento == "set-associative"):
            self.cacheIndex = int(math.log2((self.capacidadeCache/self.tamanhoBloco)/2));
            self.cacheTag = int(math.log2(self.capacidadeMP)) - self.offset - self.cacheIndex;
            # Conjunto 1 - Lista de Arrays 
            self.cacheIndexArray_1 = [i for i in range(int(math.pow(2, self.cacheIndex)))];
            self.cacheTagArray_1 = ["vazio" for i in range(int(math.pow(2, self.cacheIndex)))];
            self.cacheDataArray_1 = ["vazio" for i in range(int(math.pow(2, self.cacheIndex)))];
            self.cacheValidar_1 = [0 for i in range(int(math.pow(2, self.cacheIndex)))];
            # Conjunto 2 - Lista de Arrays
            self.cacheIndexArray_2 = [i for i in range(int(math.pow(2, self.cacheIndex)))];
            self.cacheTagArray_2 = ["vazio" for i in range(int(math.pow(2, self.cacheIndex)))];
            self.cacheDataArray_2 = ["vazio" for i in range(int(math.pow(2, self.cacheIndex)))];
            self.cacheValidar_2 = [0 for i in range(int(math.pow(2, self.cacheIndex)))];
            self.bitFIFO_2set = 0;
            # Conjunto de Pontuacoes para definir o candidato de substituição no LRU
            self.LRU_PontuacaoSET1 = [0 for i in range(int(math.pow(2, self.cacheIndex)))];
            self.LRU_PontuacaoSET2 = [0 for i in range(int(math.pow(2, self.cacheIndex)))];
            self.LRU_Contador = 0;
            self.controle = "";
            # Conjunto de Frequencias referentes aos endereços inseridos na cache no LFU
            self.LFU_Frequencia_S1 = [0 for i in range(int(math.pow(2, self.cacheIndex)))];
            self.LFU_Frequencia_S2 = [0 for i in range(int(math.pow(2, self.cacheIndex)))];
            self.LFU_contador = 0;
            self.LFU_CacheStatus_S1 = "vazia";
            self.LFU_Substituir = 0;
            self.LFU_Posicao = "Primeiro"
            # Inicialização e Leitura do Arquivo de Teste
            self.openFileExemplo(self.diretorio);         
        elif(self.mapeamento == "fully-associative"):
            self.escalonamento = escalonamento; 
            self.cacheIndex = int(math.log2((self.capacidadeCache/self.tamanhoBloco)));
            self.cacheTag = int(math.log2(self.capacidadeMP)) - self.offset;
            # Arrays para representar todos os Campos da Memória Cache
            self.cacheIndexArray = [i for i in range(int(math.pow(2, self.cacheIndex)))];
            self.cacheTagArray = ["vazio" for i in range(int(math.pow(2, self.cacheIndex)))];
            self.cacheValidar = [0 for i in range(int(math.pow(2, self.cacheIndex)))];
            self.cacheDataArray = ["vazio" for i in range(int(math.pow(2, self.cacheIndex)))];
            # Controle para determinar o candidato a ser substituido na política de FIFO;
            self.bitFIFO_fully = 0;
            # Controle para determinar o candidato a ser substituido na política de LRU
            self.LRU_Pontuacao = [0 for i in range(int(math.pow(2, self.cacheIndex)))];
            self.LRU_Contador = 0; 
            self.inserirPosicao = 0;
            # Controle com o array de frequência para determinar o candidato a ser substituido na política de LFU
            self.LFU_Frequencia = [0 for i in range(int(math.pow(2, self.cacheIndex)))];
            self.LFU_contador = 0;
            self.LFU_CacheStatus = "vazia";
            self.LFU_Substituir = 0;
            # Inicialização e Leitura do Arquivo de Teste
            self.openFileExemplo(self.diretorio);
        elif(self.mapeamento == "direto"):
            # Criação dos arrays correspondentes ao Mapeamento Direto
            self.cacheIndex = int(math.log2((self.capacidadeCache/self.tamanhoBloco)));
            self.cacheTag = self.totalMPBloco - self.cacheIndex;
            self.cacheIndexArray = [i for i in range(int(math.pow(2, self.cacheIndex)))];
            self.cacheTagArray = ["vazio" for i in range(int(math.pow(2, self.cacheIndex)))];
            self.cacheValidar = [0 for i in range(int(math.pow(2, self.cacheIndex)))];
            self.cacheDataArray = ["vazio" for i in range(int(math.pow(2, self.cacheIndex)))];
            # Inicialização e Leitura do Arquivo de Teste
            self.openFileExemplo(self.diretorio);
            
        self.mostrarConfiguracao();
        self.fracaoDeAcertos();

    def int2base(self,x, base):
        if x < 0:
            sign = -1
        elif x == 0:
            return self.digs[0]
        else:
            sign = 1

        x *= sign
        digits = []

        while x:
            digits.append(self.digs[int(x % base)])
            x = int(x / base)

        if sign < 0:
            digits.append('-')

        digits.reverse()

        return ''.join(digits)
            
    def fracaoDeAcertos(self):
        # Cálculo da fração de acertos(cache hit e cache miss)
        contadorMiss = 0;
        for i in range(0,len(self.armazenarResposta)):
            if(self.armazenarResposta[i] == "Miss"):
                contadorMiss = contadorMiss + 1;
        # Função de cálculo em porcentagem       
        fracaoMiss = "%.2f" % ((contadorMiss/len(self.armazenarResposta)) * 100);
        fracaoHit = "%.2f" % (100 - float(fracaoMiss));
        stringAcertos = 'Fração Miss:{0}%, Fração Hit:{1}%'.format(fracaoMiss,fracaoHit);
        # Mostra todos os acertos e erros de cada inserção
        print(stringAcertos);
        if(self.show_all == "yes" or self.show_all == "y"):
            print(self.armazenarResposta);
            
        print("=" * 70);
        
    def politicasParaSetAssociative(self):
        idSubstituicao = 0;
        politica = self.escalonamento;
        # Política de Substituição Randomica
        if(politica == "Random"):
            # Seleciona aleatóriamente uma posição para substituir do conjunto,ou seja,
            # Caso o valor seja igual a 0, o conjunto 1 é substituído com o valor recebido,
            # Caso contrário, o conjunto 2 terá o elemento substituído na cache;
            idSubstituicao = random.randint(0,1);
        # Política de Substituição FIFO
        elif(politica == "FIFO"):
            # Seleciona com base na política de FIFO, como há apenas duas posições, este
            # valor é somente alternado. Caso o acesso seja ao conjunto 1, o valor é 0
            # Caso contrário, o conjunto 2 terá o elemento substituído na cache;
            idSubstituicao = self.bitFIFO_2set;
            if(self.bitFIFO_2set == 1):
                self.bitFIFO_2set = 0;
            else:
                self.bitFIFO_2set = self.bitFIFO_2set + 1; 
        # Política de Substituição LRU
        elif(politica == "LRU"):
            # Caso a cache esteja cheia, o id da posição do vetor a ser substituído é o
            # menor entre as pontuações, que são atualizadas na função a cada acesso na cache,
            # seguindo as regras de LRU;
            xMenor_conjunto1 = self.LRU_PontuacaoSET1.index(min(self.LRU_PontuacaoSET1));
            xMenor_conjunto2 = self.LRU_PontuacaoSET2.index(min(self.LRU_PontuacaoSET2));
            if(xMenor_conjunto1 < xMenor_conjunto2):
                self.LRU_PontuacaoSET1[xMenor_conjunto1] = self.LRU_Contador + 1;
                idSubstituicao = xMenor_conjunto1;
                self.controle = "Primeiro"
            elif(xMenor_conjunto2 < xMenor_conjunto1):
                # Caso aconteça um empate, o valor é escolhido de forma aleatória, onde 
                # o PRIMEIRO, corresponde ao conjunto 1 e o SEGUNDO ao conjunto 2.
                # Este valor se alterna para evitar que uma mesma posição seja retirada sempre,
                # já que apenas dois conjuntos estão representados pelo set-associative mapping neste caso.
                self.LRU_PontuacaoSET2[xMenor_conjunto2] = self.LRU_Contador + 1;
                idSubstituicao = xMenor_conjunto2;
                self.controle = "Segundo";
            else:
                self.LRU_PontuacaoSET2[xMenor_conjunto2] = self.LRU_Contador + 1;
                idSubstituicao = xMenor_conjunto2;
                self.controle = "Segundo";
                
        # Política de Substituição de LFU
        elif(politica == "LFU"):
            # Semelhante ao funcionamento da função anterior (LRU)
            # Porém, aqui o trabalho é com frequências de acesso! 
            xMenor_conjunto1 = self.LFU_Frequencia_S1.index(min(self.LFU_Frequencia_S1));
            xMenor_conjunto2 = self.LFU_Frequencia_S2.index(min(self.LFU_Frequencia_S2));
            if(xMenor_conjunto1 < xMenor_conjunto2):
                self.LFU_Frequencia_S1[xMenor_conjunto1] = 1;
                idSubstituicao = xMenor_conjunto1;
                self.LFU_Posicao = "Primeiro"
                # Mesma ideia implementada para o LRU em caso de empate
            elif(xMenor_conjunto2 < xMenor_conjunto1):
                self.LFU_Frequencia_S2[xMenor_conjunto2] = 1;
                idSubstituicao = xMenor_conjunto2;
                self.LFU_Posicao = "Segundo"; 
            elif(xMenor_conjunto1 == xMenor_conjunto2):
                randomValue = random.randint(0,1);
                if(randomValue == 0):
                    self.LFU_Frequencia_S1[xMenor_conjunto1] = 1; idSubstituicao = xMenor_conjunto1; self.LFU_Posicao = "Primeiro"; 
                else:
                    self.LFU_Frequencia_S2[xMenor_conjunto2] = 1; idSubstituicao = xMenor_conjunto2; self.LFU_Posicao = "Segundo"; 
                    
        # Retornar o valor de substituição obtido com uma das políticas dessa função;
        return idSubstituicao;
        
            
    def politicaDeSubstituicao(self):
        idSubstituicao = 0;
        # Chama a função de política para o associativo por conjunto.
        # Já que o mapeamento direto não possui política de substituição
        # e o mapeamento totalmente associativo possui as políticas implementadas
        # dentro da própria função
        if(self.mapeamento == "set-associative"):
            idSubstituicao = self.politicasParaSetAssociative();
        else:
            print("Não há politicas de substituição para o Mapeamento Direto");
        # Retornar o id de Substituição, isto é, a posição do vetor;
        return idSubstituicao;
    
    def mapeamentoDireto(self,i,t,o):
        # Mapeamento Direto
        indexDecimal = int(i,2); # Converter para decimal
        palavraDecimal = int(o,2); # Converter para decimal
        # Inserir dado com base no endereço de index
        if(self.cacheValidar[indexDecimal] == 0):
            self.cacheTagArray[indexDecimal] = t;
            self.cacheDataArray[indexDecimal] = self.MPArrayBloco[int(t + i,2)] + self.MPArrayPalavra[palavraDecimal];
            self.cacheValidar[indexDecimal] = 1;
            self.armazenarResposta.append("Miss");
        # Verificar se determinada posição(index) na cache está preenchido
        elif(self.cacheValidar[indexDecimal] == 1):
            # Operação em caso de cache hit
            if(self.cacheTagArray[indexDecimal] == t):
                self.armazenarResposta.append("Hit");
            # Operação em caso de cache miss
            else:
                self.cacheTagArray[indexDecimal] = t;
                self.cacheDataArray[indexDecimal] = self.MPArrayBloco[int(t + i,2)] + self.MPArrayPalavra[palavraDecimal];
                self.cacheValidar[indexDecimal] = 1;
                self.armazenarResposta.append("Miss");
    
    def mapeamentoFullyAssociative(self,t,o):
        # Mapeamento Totalmente Associativo, esta função recebe as variaveis 
        # correspondentes ao campo tag e offset-bit, visto que não há index
        politica = self.escalonamento;
        resposta = "";
        palavraDecimal = int(o,2); # Converter para Binário
        # Em caso da política escolhida for a FIFO(First In, First Out)
        if(politica == "FIFO"):
            # Busca em todas as posições da cache, visto que não há index
            for i in range(0,len(self.cacheIndexArray)):
                # Percorrer e procurar um elemento com a mesma tag (cache hit)
                if(self.cacheTagArray[i] == t):
                    self.armazenarResposta.append("Hit");
                    resposta = "Sim";
                # Caso contrário, inserir em qualquer posição, baseando-se na 
                # política de substituição escolhida
            if(resposta != "Sim"):
                # No FIFO, a substituição ou inserção se baseia no id do array inserido primeiro.
                # Esta função está baseada na ordem de acesso aos endereços solicitados.
                self.cacheTagArray[self.bitFIFO_fully] = t;
                self.cacheDataArray[self.bitFIFO_fully] = self.MPArrayBloco[int(t,2)] + self.MPArrayPalavra[palavraDecimal];
                self.cacheValidar[self.bitFIFO_fully] = 1;
                self.armazenarResposta.append("Miss");
                if(self.bitFIFO_fully == len(self.cacheIndexArray) - 1):
                    self.bitFIFO_fully = 0;
                else:
                    self.bitFIFO_fully = self.bitFIFO_fully + 1;
        # Política de Substituição LFU (Por frequência de acessos, menor frequência é eliminado primeiro)
        elif(politica == "LFU"):
            # Percorrer e procurar um elemento com a mesma tag (cache hit)
            for i in range(0,len(self.cacheIndexArray)):
                if(self.cacheTagArray[i] == t):
                    self.armazenarResposta.append("Hit");
                    resposta = "Sim";
                    # Há um vetor de frequências, que armazena as frequências de cada
                    # um dos elementos, baseando-se na sua posição dentro do array.
                    self.LFU_Frequencia[i] = self.LFU_Frequencia[i] + 1;
            # Caso contrário, inserir em qualquer posição, baseando-se na 
            # política de substituição escolhida
            if(resposta != "Sim"):
                # Esta função é responsável por retornar o id do array com menor frequência.
                # Em caso de empate, o elemento mais perto do topo do array é selecionado, ou seja
                # o mais próximo da posição LFU_Frequencia[0]
                menorFrequencia = self.LFU_Frequencia.index(min(self.LFU_Frequencia));
                self.LFU_Frequencia[menorFrequencia] = 1;
                self.cacheTagArray[menorFrequencia] = t;
                self.cacheDataArray[menorFrequencia] = self.MPArrayBloco[int(t,2)] + self.MPArrayPalavra[palavraDecimal];
                self.cacheValidar[menorFrequencia] = 1;
                self.armazenarResposta.append("Miss");
        # Em caso da política escolhida for a Random 
        elif(politica == "Random"):
            # Percorrer e procurar um elemento com a mesma tag (cache hit)
            for i in range(0,len(self.cacheIndexArray)):
                if(self.cacheTagArray[i] == t):
                    self.armazenarResposta.append("Hit");
                    resposta = "Sim";
                    # Há um vetor de frequências, que armazena as frequências de cada
                    # um dos elementos, baseando-se na sua posição dentro do array.
            # política de substituição escolhida
            if(resposta != "Sim"):
                # Esta função gera randomicamente uma posição de array entre as selecionadas.
                # Os valores gerados são totalmente aleatórios, logo não é possível determinar
                # em qual posição o dado será inserido ou substituido
                x = random.randint(0,(len(self.cacheIndexArray) - 1));
                self.cacheTagArray[x] = t;
                self.cacheDataArray[x] = self.MPArrayBloco[int(t,2)] + self.MPArrayPalavra[palavraDecimal];
                self.cacheValidar[x] = 1;
                self.armazenarResposta.append("Miss");
                if(self.bitFIFO_fully == len(self.cacheIndexArray) - 1):
                    self.bitFIFO_fully = 0;
                else:
                    self.bitFIFO_fully = self.bitFIFO_fully + 1;
        # Política de Substituição LRU(Recentemente utilizado)
        elif(politica == "LRU"):
            # O elemento menos recentemente utilizado é eliminado em caso de conflito
            # Percorrer e procurar um elemento com a mesma tag (cache hit)
            for i in range(0,len(self.cacheIndexArray)):
                if(self.cacheTagArray[i] == t):
                    self.armazenarResposta.append("Hit");
                    resposta = "Sim";
                    # Há um vetor de frequências, que armazena as frequências de cada
                    # um dos elementos, baseando-se na sua posição dentro do array.
            # Política de Substituição selecionada
            if(resposta != "Sim"):
                # Há um contador e um vetor de Pontuações com base na posição do vetor de cada elemento.
                # Assim, a substituição ocorre com o elemento de menor pontuação (menos recentemente utilizado)
                self.cacheTagArray[self.inserirPosicao] = t;
                self.LRU_Pontuacao[self.inserirPosicao] = self.LRU_Contador;
                self.LRU_Contador = self.LRU_Contador + 1;
                self.cacheDataArray[self.inserirPosicao] = self.MPArrayBloco[int(t,2)] + self.MPArrayPalavra[palavraDecimal];
                self.cacheValidar[self.inserirPosicao] = 1;
                self.armazenarResposta.append("Miss");
                # Em caso da cache estar cheia !
                k = 0;
                for i in range(len(self.cacheIndexArray)):
                    if(self.cacheValidar[i] == 1):
                        k = k + 1;
                # Cálcular o menor elemento entre as pontuações no vetor LRU_Pontuação
                if(k == len(self.cacheIndexArray)):
                    xMenor = self.LRU_Pontuacao.index(min(self.LRU_Pontuacao))
                    self.inserirPosicao = xMenor;
                    self.LRU_Pontuacao[xMenor] = self.LRU_Pontuacao[xMenor] + 1;
                    # O menor elemento é selecionado e somado, para indicar que este teve um acesso.
                    # A posição é armazenada e alterada na próxima rodada do algoritmo.
                else:
                    self.inserirPosicao = self.inserirPosicao + 1;    

            
    def mapeamentoSetAssociative(self,i,t,o):
        # Mapeamento Associativo por Conjunto, definido com um tamanho fixo de 2 conjuntos no total;
        # Neste, as operações de controle são mais complexas, já que é necessário administrar duas
        # tabelas diferentes (arrays), com base na política de substituição selecionada
        indexDecimal = int(i,2);
        palavraDecimal = int(o,2);
        if(self.cacheValidar_1[indexDecimal] == 0) and (self.cacheValidar_2[indexDecimal] == 0):
            self.cacheTagArray_1[indexDecimal] = t;
            self.cacheValidar_1[indexDecimal] = 1;
            self.cacheDataArray_1[indexDecimal] = self.MPArrayBloco[int(t + i,2)] + self.MPArrayPalavra[palavraDecimal]
            self.armazenarResposta.append("Miss");
            # Armazena a potuação do LRU e também armazena a frequência do LFU.
            # Como estamos percorrendo os vetores, esta função foi aproveitada para
            # realizar todos os cálculos ao mesmo tempo, da LRU e LFU;
            self.LRU_PontuacaoSET1[indexDecimal] = self.LRU_Contador + 1; # Contador para o conjunto 1
            self.LFU_Frequencia_S1[indexDecimal] = self.LFU_Frequencia_S1[indexDecimal] + 1; # Frequencia para o conjunto 1
        # Próximo passo, verificar se um dos conjuntos possue espaço.    
        elif(self.cacheValidar_1[indexDecimal] == 1) and (self.cacheValidar_2[indexDecimal] == 0):
            if(self.cacheTagArray_1[indexDecimal] == t):
                self.armazenarResposta.append("Hit");
                # Array de Pontuação do LRU e frequência do LFU - Conjunto 1;
                self.LRU_PontuacaoSET1[indexDecimal] = self.LRU_Contador + 1;
                self.LFU_Frequencia_S1[indexDecimal] = self.LFU_Frequencia_S1[indexDecimal] + 1;
            else:
                self.cacheTagArray_2[indexDecimal] = t;
                self.cacheValidar_2[indexDecimal] = 1;
                self.cacheDataArray_2[indexDecimal] = self.MPArrayBloco[int(t + i,2)] + self.MPArrayPalavra[palavraDecimal]
                self.armazenarResposta.append("Miss");
                # Array de Pontuação do LRU e frequência do LFU - Conjunto 2;
                self.LRU_PontuacaoSET2[indexDecimal] = self.LRU_Contador + 1;
                self.LFU_Frequencia_S2[indexDecimal] = self.LFU_Frequencia_S2[indexDecimal] + 1;
        # Caso a cache esteja cheia em ambos os conjuntos:
        elif(self.cacheValidar_1[indexDecimal] == 0) and (self.cacheValidar_2[indexDecimal] == 1):
            if(self.cacheTagArray_2[indexDecimal] == t):
                self.armazenarResposta.append("Hit");
                # Array de Pontuação do LRU e frequência do LFU - Conjunto 2, em caso de HIT;
                self.LRU_PontuacaoSET2[indexDecimal] = self.LRU_Contador + 1;
                self.LFU_Frequencia_S2[indexDecimal] = self.LFU_Frequencia_S2[indexDecimal] + 1;
               # Caso seja um cache miss:
            else:
                self.cacheTagArray_1[indexDecimal] = t;
                self.cacheValidar_1[indexDecimal] = 1;
                self.cacheDataArray_1[indexDecimal] = self.MPArrayBloco[int(t + i,2)] + self.MPArrayPalavra[palavraDecimal]
                self.armazenarResposta.append("Miss");
                 # Array de Pontuação do LRU e frequência do LFU - Conjunto 1, em caso de MISS;
                self.LRU_PontuacaoSET1[indexDecimal] = self.LRU_Contador + 1;
                self.LFU_Frequencia_S1[indexDecimal] = self.LFU_Frequencia_S1[indexDecimal] + 1;
         # Caso ambos os espaços esteja ocupados - bit validator = 1 em ambos os conjuntos       
        elif(self.cacheValidar_1[indexDecimal] == 1) and (self.cacheValidar_2[indexDecimal] == 1):
                if(self.cacheTagArray_1[indexDecimal] == t):
                    self.armazenarResposta.append("Hit");
                     # Operação em caso de um hit no conjunto 1
                    self.LRU_PontuacaoSET1[indexDecimal] = self.LRU_Contador + 1;
                    self.LFU_Frequencia_S1[indexDecimal] = self.LFU_Frequencia_S1[indexDecimal] + 1;
                elif(self.cacheTagArray_2[indexDecimal] == t):
                    self.armazenarResposta.append("Hit");
                     # Operação em caso de um hit no conjunto 2
                    self.LRU_PontuacaoSET2[indexDecimal] = self.LRU_Contador + 1;
                    self.LFU_Frequencia_S2[indexDecimal] = self.LFU_Frequencia_S2[indexDecimal] + 1;
                # Caso ocorra um MISS:
                else:
                    # Chama a função que cálcula a posição do vetor cache que será substituido,
                    # conforme as políticas de substituições adotados e selecionadas;
                    escolherSubstituicao = self.politicaDeSubstituicao();
                    if(self.escalonamento == "LFU"):
                        # Em caso da política ser LFU:
                        if(self.LFU_Posicao == "Primeiro"):
                            # Realizar a substituição no primeiro conjunto (1)
                            self.armazenarResposta.append("Miss");
                            self.cacheTagArray_1[indexDecimal] = t;
                            self.cacheValidar_1[indexDecimal] = 1;
                            self.cacheDataArray_1[indexDecimal] = self.MPArrayBloco[int(t + i,2)] + self.MPArrayPalavra[palavraDecimal]     
                        elif(self.LFU_Posicao == "Segundo"):
                            # Realizar a substituição no segundo conjunto (2)
                            self.armazenarResposta.append("Miss");
                            self.cacheTagArray_1[indexDecimal] = t;
                            self.cacheValidar_1[indexDecimal] = 1;
                            self.cacheDataArray_1[indexDecimal] = self.MPArrayBloco[int(t + i,2)] + self.MPArrayPalavra[palavraDecimal]   
                    # Em caso da política ser LRU       
                    elif(self.escalonamento == "LRU"):
                        if(self.controle == "Primeiro"):
                            # Realizar a substituição no primeiro conjunto (1)
                            self.armazenarResposta.append("Miss");
                            self.cacheTagArray_1[indexDecimal] = t;
                            self.cacheValidar_1[indexDecimal] = 1;
                            self.cacheDataArray_1[indexDecimal] = self.MPArrayBloco[int(t + i,2)] + self.MPArrayPalavra[palavraDecimal]   
                        elif(self.controle == "Segundo"):
                            # Realizar a substituição no segundo conjunto (2)
                            self.armazenarResposta.append("Miss");
                            self.cacheTagArray_1[indexDecimal] = t;
                            self.cacheValidar_1[indexDecimal] = 1;
                            self.cacheDataArray_1[indexDecimal] = self.MPArrayBloco[int(t + i,2)] + self.MPArrayPalavra[palavraDecimal]   
                    # Em caso da política ser Random ou FIFO.
                    # Esta estrutura é a mesma para ambas as políticas, para aproveitamento do
                    # código, já que é apenas o conteúdo de uma determinada posição que é trocado.
                    # A função responsável por fazer a troca com base na política selecionada, é a função politicaDeSubstituicao()
                    else:
                        if(escolherSubstituicao == 0):
                            self.armazenarResposta.append("Miss");
                            self.cacheTagArray_1[indexDecimal] = t;
                            self.cacheValidar_1[indexDecimal] = 1;
                            self.cacheDataArray_1[indexDecimal] = self.MPArrayBloco[int(t + i,2)] + self.MPArrayPalavra[palavraDecimal]   
                        else:
                            self.armazenarResposta.append("Miss");
                            self.cacheTagArray_2[indexDecimal] = t;
                            self.cacheValidar_2[indexDecimal] = 1;
                            self.cacheDataArray_2[indexDecimal] = self.MPArrayBloco[int(t + i,2)] + self.MPArrayPalavra[palavraDecimal]  
            
                    self.LRU_Contador = self.LRU_Contador + 1;
        
    def openFileExemplo(self, diretorio):
        # Calcular o Tamanho Total da Instrução recebida
        tamanhoDaInstrucao = int(math.log2(self.capacidadeMP));
        # Abrir o arquivo conforme o diretório informado como parâmetro
        arquivo = open(diretorio, "r");
        items = arquivo.readlines();
        array_values = [];
        for i in range(len(items)):
            v = int(items[i].replace("\n",""));
            array_values.append(v)
   
        for i in range(0,len(array_values)):
            Decimal = str(array_values[i])
            DecimalToBinario = self.int2base(array_values[i],2)
            # Acrescentar zeros nos bits, conforme o tamanho da instrução
            bitZero = tamanhoDaInstrucao - len(DecimalToBinario);
            linha = "0" * bitZero + DecimalToBinario;
            # Formatar valores, conforme as linhas recebidas (em binário)
            i, t, o = self.formatar(linha);
            # Informa a inserção atual, o programa mostra o conteúdo da
            # memória cache a cada rodada.
            if(self.show_all == "y" or self.show_all == "yes"):
                print("Inserir(",Decimal,") ---> Binário:",linha,"\n");
                
            if(self.mapeamento == "set-associative"):
                # Chama a função de set-associative mapping
                self.mapeamentoSetAssociative(i,t,o);
            elif(self.mapeamento == "fully-associative"):
                # Chama a função de fully-associative mapping
                self.mapeamentoFullyAssociative(t,o);
            else:
                    # Chama a função de direct-associative mapping
                self.mapeamentoDireto(i,t,o);
                # Mostra o conteúdo do vetor (memória cache) a cada rodada;
                
            if(self.show_all == "y" or self.show_all == "yes"):
                self.mostrarConteudo();
                print("-" * 100);
                
    def formatar(self, enderecoExemplo):
        # Formata a entrada conforme os campos solicitados por cada estrutura de mapeamento
        if(self.mapeamento == "set-associative"):
            tagFinal = self.cacheTag - 1;
            cacheIndexInicial = tagFinal + 1;
            cacheIndexFinal = cacheIndexInicial + (self.cacheIndex - 1);
            offsetInicial = cacheIndexFinal + 1;
            offsetFinal = offsetInicial + (self.offset - 1);
            tagExemplo = enderecoExemplo[0:tagFinal + 1];
            indexExemplo = enderecoExemplo[cacheIndexInicial:cacheIndexFinal + 1];
            offsetExemplo = enderecoExemplo[offsetInicial:offsetFinal + 1];   
        elif(self.mapeamento == "fully-associative"):
            tagFinal = self.cacheTag - 1;
            offsetInicial = tagFinal + 1;
            offsetFinal = offsetInicial + (self.offset - 1);
            tagExemplo = enderecoExemplo[0:tagFinal + 1];
            offsetExemplo = enderecoExemplo[offsetInicial:offsetFinal + 1];
            indexExemplo = 0;
        else:
            tagFinal = self.cacheTag - 1;
            cacheIndexInicial = tagFinal + 1;
            cacheIndexFinal = cacheIndexInicial + (self.cacheIndex - 1);
            offsetInicial = cacheIndexFinal + 1;
            offsetFinal = offsetInicial + (self.offset - 1);
            tagExemplo = enderecoExemplo[0:tagFinal + 1];
            indexExemplo = enderecoExemplo[cacheIndexInicial:cacheIndexFinal + 1];
            offsetExemplo = enderecoExemplo[offsetInicial:offsetFinal + 1];
        # Retorna os valores de Index (caso exista), Tag e offSet-bit   
        return indexExemplo, tagExemplo, offsetExemplo;
           
    def mostrarConteudo(self):
        # Mostrar conteúdo com base na formatação do script:
        if(self.mapeamento == "set-associative"):
            stringTable = '| {i1:>3} | {v1:>4} | {t1:>9} | {d1:>20}  || {i2:>3} | {v2:>4} | {t2:>15} | {d2:>20}  |'.format(
                   i1 = 'I-S1',v1 = 'V-S1',t1 = 'Tag-S1', d1 = 'Data-S1',
                   i2 = 'I-S2',v2 = 'V-S2',t2 = 'Tag-S2', d2 = 'Data-S1');
            print(stringTable);
            for i in range(int(math.pow(2, self.cacheIndex))):
                stringCache = '| {i1:>3} | {v1:>4} | {t1:>9} | {d1:>20}  || {i2:>3} | {v2:>4} | {t2:>15} | {d2:>20}  |'.format(
                                                                   i1 = self.cacheIndexArray_1[i],v1 = self.cacheValidar_1[i],
                                                                   t1 = self.cacheTagArray_1[i], d1 = self.cacheDataArray_1[i],
                                                                   i2 = self.cacheIndexArray_2[i],v2 = self.cacheValidar_2[i],
                                                                   t2 = self.cacheTagArray_2[i], d2 = self.cacheDataArray_2[i],);
                print(stringCache);
                
        elif(self.mapeamento == "fully-associative" or self.mapeamento == "direto"):
            stringTable = '| {i:>5} | {v:>7} | {t:>15} | {d:>20}  |'.format(i = 'Index',v = 'Validar',t = 'Tag', d = 'Data');
            print(stringTable);
            for i in range(int(math.pow(2, self.cacheIndex))):
                stringCache = '| {i:>5} | {v:>7} | {t:>15} | {d:>20}  |'.format(i = self.cacheIndexArray[i],
                                                                                v = self.cacheValidar[i],
                                                                                t = self.cacheTagArray[i],
                                                                                d = self.cacheDataArray[i]);
                print(stringCache);
        else:
            print("Erro ao Exibir, mapeamento inserido não corresponde a nenhum dos listados!");

    def mostrarConfiguracao(self):
        if(self.mapeamento == "direto"):
            self.escalonamento = "nenhum"
        # Exibir todas as configurações e cálculos realizados
        # Isso inclui os valores de index, tag, tipo de mapeamento e tipo de política de Substituição
        print("=" * 70);
        stringConfiguracao = 'Capacidade MB:{0} (em bytes), nBlocos(K):{1}, Capacidade cache:{2} (em bytes)'.format(self.capacidadeMP,self.tamanhoBloco,
                                                                                               self.capacidadeCache);
        stringMP = 'MP possui blocos de B[0..{0}] com palavras de W[0..{1}]'.format(self.ultimoBloco,self.ultimaPalavra);
        print(stringConfiguracao,'\n',stringMP);
        if(self.mapeamento == "direto" or self.mapeamento == "set-associative"):
            stringCache = '--> Mapeamento:{0}   [tag:{1}, index:{2}, offset:{3}]'.format(self.mapeamento,self.cacheTag,self.cacheIndex,self.offset);
            print(stringCache,'\n Politica de Substituição:',self.escalonamento);
        else:
            stringCache = '--> Mapeamento:{0}   [tag:{1}, offset:{2}]'.format(self.mapeamento,self.cacheTag,self.offset);
            print(stringCache,'\n Politica de Substituição:',self.escalonamento);
        # Fim    
        print("=" * 70);

