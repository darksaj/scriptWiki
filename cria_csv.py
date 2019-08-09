'''
*	cria_csv.py é parte do scriptWiki que é um software livre; você pode redistribui-lo e/ou 
*	modifica-lo dentro dos termos da Licença Pública Geral GNU como 
*	publicada pela Fundação do Software Livre (FSF); na versão 2 da 
*	Licença, ou (na sua opinião) qualquer versão.
*	
*	Este programa é distribuído na esperança que possa ser util, 
*	mas SEM NENHUMA GARANTIA; sem uma garantia implicita de ADEQUAÇÂO a qualquer
*	MERCADO ou APLICAÇÃO EM PARTICULAR. Veja a
*	Licença Pública Geral GNU para maiores detalhes.
*	
*	Você deve ter recebido uma cópia da Licença Pública Geral GNU
*	junto com este programa, Se não, veja <http://www.gnu.org/licenses/>.
*
*	scriptDGP Copyright (C) 2016  Jussara Ribeiro de Oliveira
*	https://github.com/darksaj/scriptWiki/
'''

# -*- coding: utf-8 -*
import sys
import re
import requests #importa a api para leitura da pagina web
from bs4 import BeautifulSoup


arq_tab = open('tabela.csv', 'w+') #cria o csv que vai conter os dados dos artigos
texto = arq_tab.readlines() #prepara para ler o csv com os nomes de artigos

linha = "" #conteudo dos dados de cada linha

arq = open("cientistas.csv",'r') #seleciona o arquivo com a lista de artigos a serem lidos
for ln in arq:
    
    artigo = ln.strip("\n").replace(" ","_") #tira as quebras de linha e substitui espaços por underline
    
    linha = linha + artigo + "\t" #grava o nome do artigo
    
    paginas = 'https://pt.wikipedia.org/wiki/' + artigo #Para cada artigo guarda o link de uma pagina

    print (paginas) # exibe quais paginas estao sendo lidas
    
    link_leitura=paginas.encode('cp1252')  #acerta assentos para link da web
    
    response = requests.get(link_leitura) #seleciona cada pagina

    if response.status_code == 200:
        conteudo = response.content
        parsed_html = BeautifulSoup(conteudo,"html.parser") #parsea o conteúdo

       #busca por imagens
        link_img = parsed_html.body.find('a', attrs={'title':artigo.replace("_"," ")})
        
        if (link_img != None):
            linha = linha + link_img.img['src']+ "\t"
        else:
            linha= linha + "sem foto\t"

        #pega a descricao principal
        
        miolo= parsed_html.body.find('div', attrs={'class':'mw-parser-output'}) #busca o conteúdo principal das páginas

        descricao = miolo.p.get_text()
        descricao = re.sub("\([A-Za-z]+.*:.*\)","",descricao)#tira o conteudo entre parenteses pois costuam ter outros encondings como nomes escritos no idioma original
        
        if (artigo == "Jessica_Fridrich"): #tirando o artigo que da erro, precisa melhorar tratamento de enconding
            linha= linha+ "nao deu\t"
        else:
            linha= linha + descricao.strip("\n").replace("\"","").replace("'","").replace("[","").replace("]","")+"\t" #cria uma coluna com o texto de descrição do artigo e tira as aspas pois criava erro de enconding

        #salva a nacionalidade
        if (miolo.tbody != None):
            for row in miolo.tbody.find_all('tr'):

                if (re.search("Nacionalidade", row.text)): #busca pela nacionalidade
                    nacionalidade=row.text.replace("Nacionalidade","").strip("\n") #tira os espaços em branco e o nome do atributo
                    linha= linha + nacionalidade.strip("\n") #guarda a nacionalidade
            linha = linha + "\t" #guarda a nacionalidade
        else:
            print("Sem quadro de detalhes")
            linha = linha + "??\t"

        #salva as categorias

        link_cat = parsed_html.body.find('div', attrs={'id':'mw-normal-catlinks'})
        cats = "|"
        
        if (link_cat != None):
            
            for row in link_cat.find_all('a'):
                
                if (re.search("Categorias",row.text) == None):
                    
                    cats = cats + row.text.strip("\n") + "|"
            
            linha= linha +cats.strip("\n") +"\t"

        else:
            linha= linha + "sem categoria\t"
        
    else:
        print (paginas + " não pode ser lido")
    
    linha = linha + "\n" #quebra linha do arquivo que esta sendo gravado
    
arq.close()

texto.append(linha)

arq_tab.writelines(texto)
arq_tab.close()





