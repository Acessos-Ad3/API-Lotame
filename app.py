import requests
from configparser import ConfigParser  
import json

username = ""
password = 0
end_point = ""
end_point_base = ""
id_audiencia = ""

def escolher_modelo():
    tipo_de_grafico = input("Digite o nome do grafico: ")
    if(tipo_de_grafico == "genero"):
        pass

    elif(tipo_de_grafico == "idade"):
        pass
    
    elif(tipo_de_grafico == "crianças em casa"):
        pass
    
    elif(tipo_de_grafico == "educacao"):
        pass
    

#O usuarios faz digitar as informações que ele deseja
def informacoes_usuario():

    global username , password, end_point, end_point_base, id_audiencia

    end_point = input("Digite o end-point da audiencia: ")
    end_point.split()

    end_point_base = input("Digite a base do end-point: ")
    end_point_base.split()

    id_audiencia = input("Digite o Id da audiencia: ")
    id_audiencia.strip()

    username = input("Digite seu login: ")
    username.split()

    password = input("Digite sua senha: ")
    password.split()

informacoes_usuario()

#Faz a autenticação do usuario
def autenticacao():

    parser = ConfigParser()
    parser.read('config.cfg')
    authentication_url = parser.get('api_samples', 'authentication_url')
    return authentication_url

def carregar_nome_user():

    payload = {'username': username, 'password': password}
    return payload


def cabecalho():

    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain", "User-Agent":"python"}
    return headers

#Obtem o ticket do CAS(Central de altenticação de serviços)
def obter_ticket():

    autencation = autenticacao()
    payload = carregar_nome_user()
    headers = cabecalho()
    tg_ticket_location = requests.post(autencation, data=payload).headers['location']
    return tg_ticket_location

#Configura a base da url: https://api.lotame.com/2/
def base_url():
    parser = ConfigParser()
    parser.read('config.cfg')
    base_api_url = parser.get('api_samples', 'api_url')
    return base_api_url

#Configura o link da API
def services():
    base_api_url = base_url()
    service = base_api_url + end_point_base + id_audiencia 
    return service

#Baixa todas as informações em formato json
def capturar_dados(lista_dados, service_ticket, payload):

        service_call = services() + end_point
        payload = {'service': service_call}
        service_ticket = requests.post(obter_ticket(), data=payload).text

        headers = {'Accept':'application/json'}
        r = requests.get(('%s?ticket=%s') % (service_call, service_ticket), headers=headers)

        if(tratamento_erros(r) == False):
            print("Audiencia não econtrada!!")
            print("Veja o link que voce digitou: {0}".format(services())) 
            print("Dica: Copie esse link acima e cole no navegador, e veja se a saída é um json ou um xml com uma saída 404", end=" ")
            print("Caso sim, esse link não existe, voce deve ter digitado o link errado")

        else:
            try:

                dados = requests.get(('%s&ticket=%s') % (service_call, service_ticket)).json()
                #chamado a função responsavel por formatar os dados
                criar_arquivo_json(dados)

            except json.decoder.JSONDecodeError:
                print("Ocorreu um erro inexplicavel!! \n Tente novamente mais tarde.")

#Verifica se houve um erro na chamado da api
def tratamento_erros(erros):

    if(erros.status_code == 404):
        return False
    else:
        return True

#Criar o arquivo em json e adicionar o json gerado a api dentro do arquivo
def criar_arquivo_json(dados):

    arquivo_audiencia = open("arquivos_json/AUDIENCIA.json", "w")
    converter = json.dumps(dados)
    arquivo_audiencia.write(converter)
    arquivo_audiencia.close()

capturar_dados("", "", "")

