# This code sample uses the 'requests' library:
# http://docs.python-requests.org
from configparser import RawConfigParser
from unidecode import unidecode
from sr_gather import TicketExtractor
from jira_create_issue import CreateIssue


config = RawConfigParser()
config.read('config.properties_local')
tickets = config.get('SDSRSection', 'lista_tickets')
lista_tickets = tickets.split(',')
file_output_name = config.get('SDSRSection', 'outfile_name')
extractor = TicketExtractor(user_name=config.get('SDUserSection','user.email'), password=config.get('SDUserSection','user.password'),
                            file_output=file_output_name)
extractor.run(tickets=lista_tickets)
file_output_name = file_output_name+'.csv'
with open(file_output_name, 'r',encoding='utf-8') as f:
    for ticket in f:
      execute_creation = CreateIssue()
      response = execute_creation.run(ticket)
      print(response)


