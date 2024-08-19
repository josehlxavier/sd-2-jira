import requests
import json
from requests.exceptions import ConnectionError

class TicketExtractor:
    def __init__(self, user_name, password, file_output):
        self.user_name = user_name
        self.password = password
        self.file_output = file_output
    
    def login(self):
        
        url = 'https://servicedesk.openfinancebrasil.org.br/api/v1/login'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Content-Type': 'application/json'
        }
        payload = {'user_name': self.user_name,'password': self.password, 'accountId' : 'obkbrasil'}
        payload = json.dumps(payload)
        
        session = requests.Session()
        response = session.post(url, headers=headers, data=payload)
        
        if response.status_code == 200:
            cookies = response.cookies
            session.cookies = cookies
            return session
        else:
            print('Failed to login')
    
    def extract_ticket(self, tickets):
        for i in tickets:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
                'Content-Type': 'application/json'
            }
            url_busca_sr = 'https://servicedesk.openfinancebrasil.org.br/api/v1/sr/' + str(i)
            response_leitura = self.session.get(url_busca_sr, headers=headers)
            
            if response_leitura.status_code == 200:
                arqv_leitura = open(self.file_output + '.csv', 'a', encoding='utf-8')
                with arqv_leitura as file:
                    file.writelines(self.extract_data_from_ticket(response_leitura.text))
                    file.write('\n')
            else:
                print('Failed to extract data for ticket #' + str(i))
    
    def extract_data_from_ticket(self, response):     # Obter os dados de um objeto JSON
        data = json.loads(response)
        linha_csv = []
        notas_concat = ''
        linha_csv.append(data['id'])
        for i in data['info']:
            if i['key'] == 'CustomColumn155sr': # "CustomColumn155sr" = "Usuário Solicitante"
                linha_csv.append(i['valueCaption'].replace('\\t',''))
            if i['key'] == 'insert_time': # Data de criação
                linha_csv.append(str(i['valueCaption']))
            if i['key'] == 'title': #Título da SR
                linha_csv.append(i['valueCaption'])
            if i['key'] == 'description': #Descrição da SR
                linha_csv.append(str(i['valueCaption']).replace('\t', '').replace('\n', '').replace('|','')) #Removendo linhas novas, tabs e pipes. Não quebrar a formatação do CSV(separador é o pipe)
            if i['key'] == 'notes': #
                if i['value'] is not None:
                    for value in i['value']:
                        notas_concat += str(value) + '#'
                    linha_csv.append(notas_concat.replace('\t', '').replace('\n', ''))
                else:
                    linha_csv.append('Ainda não há')
            if i['key'] == 'CustomColumn114sr':
                linha_csv.append(i['valueCaption'])
            if i['key'] == 'category':
                linha_csv.append(i['valueCaption'])
            if i['key'] == 'close_time':
                if i['valueCaption'] != '' :
                    linha_csv.append(i['valueCaption'])
                else:
                    linha_csv.append('Em aberto')
            if i['key'] == 'CustomColumn16sr': # "CustomColumn16sr" = "Equipe de Atendimento"
                if i['valueCaption'] != '' :
                    linha_csv.append(i['valueCaption'])
                else:
                    linha_csv.append('Ticket ainda sem solução')
        linha_csv = '|'.join(map(str, linha_csv))
        linha_csv = filter(str.strip, linha_csv.splitlines())
        return linha_csv
    
    def run(self, tickets):
        self.session = self.login()
        if self.session is not None:
            self.extract_ticket(tickets)