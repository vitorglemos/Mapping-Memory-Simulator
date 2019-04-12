
# coding: utf-8

from mapping import *;
import sys
import argparse
import os 
import stat
import getpass

parser = argparse.ArgumentParser();
parser.add_argument("-show","--mostrarConteudoCache",help="Este parâmetro, se declarado como yes ou y, exibe todo conteúdo em todas as etapas de inserção na cache. Por padrão, está definido como 'yes'",default="yes");
parser.add_argument("-mp","--capacidadeMP",help="Capacidade Total da Memória Principal: Indique a Capacidade Total da Memória Principal, por padrão este valor é de 2048 bytes",default=4096);
parser.add_argument("-cache","--capacidadeCache",help="Capacidade Total da Memória Cache: Indique a Capacidade Total de Cache Disponível, por padrão este valor é de 16 bytes",default=32);
parser.add_argument("-w","--offsetBit",help="Tamanho da Palavra da Instrução em Bits: Indique a Capacidade de Bits para Representação do campo Palavras da Instrução, por padrão este valor é 2 (em bits)",default=2);
parser.add_argument("-map","--tipoDeMapeamento",help="Tipo de mapeamento: Indique o tipo de Mapeamento desejado. As opções válidas são: direto, fully-associative e set-associative. A representação set-associative por padrão é de 2 conjuntos apenas. Para os mapeamentos fully-associative e set-associative é necessário definir uma política de substituição",default='all');
parser.add_argument("-local","--diretorio",help="Diretorio ou caminho do arquivo: Indique o Caminho do Diretório Correspondente ao Arquivo .txt com os Dados de Entrada. Este arquivo deve estar com os valores em decimal, já que o script já realiza a conversão para binário.");
parser.add_argument("-sub","--politicaDeSubstituicao",help="Politica de Substituicao: Indique a politica de Substituicao desejada ou deixe este campo em branco para executar o programa como -all. O atributo -all realiza a execução do script com todas as políticas disponíveis (FIFO,LRU,LFU e Random)",default='all');
args = parser.parse_args();

mostrarAll = args.mostrarConteudoCache;
MemoriaPrincipal = int(args.capacidadeMP);
MemoriaCache = int(args.capacidadeCache);
PalavraBit = int(args.offsetBit);
Mapeamento = args.tipoDeMapeamento;
Politicas = args.politicaDeSubstituicao;
Caminho = r'{0}'.format(args.diretorio);
if(Mapeamento == 'all' and Politicas == 'all'):
	Executar = Memoria(MemoriaPrincipal, MemoriaCache, PalavraBit, 'direto', Caminho, 'none','no');
	SUB = ['FIFO','LRU','LFU','Random']
	for i in range(0,len(SUB)):
		Executar = Memoria(MemoriaPrincipal, MemoriaCache, PalavraBit, 'fully-associative', Caminho, SUB[i],'no');
	for i in range(0,len(SUB)):
		Executar = Memoria(MemoriaPrincipal, MemoriaCache, PalavraBit, 'set-associative', Caminho, SUB[i],'no');
	print("Modo de geração automática foi encerrado com sucesso!");
if(Mapeamento == "direto"):
# Chama a classe, caso o parâmetro -map esteja com o valor (direto)"
    Executar = Memoria(MemoriaPrincipal, MemoriaCache, PalavraBit, Mapeamento, Caminho, "none", mostrarAll);
elif(Mapeamento == "fully-associative" or Mapeamento == "set-associative"):
# Chama a classe, caso o parâmetro -sub seja uma das políticas escolhidas
    Executar = Memoria(MemoriaPrincipal, MemoriaCache, PalavraBit, Mapeamento, Caminho, Politicas, mostrarAll);


