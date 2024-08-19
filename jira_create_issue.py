import requests
from requests.auth import HTTPBasicAuth
from configparser import RawConfigParser
import json
from requests.exceptions import ConnectionError

class CreateIssue:
    def get_user_config(self):
        self.config = RawConfigParser(allow_no_value=False)
        self.config.read("config.properties_local")
        self.user = self.config.get('JiraUserSection','user.email')
        self.api_token = self.config.get('JiraUserSection','user.api_token')
        return self.user, self.api_token

    def create_on_jira(self, payload):
        url = "https://openfinancebrasil.atlassian.net/rest/api/3/issue" 
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        user,api_token = self.get_user_config()
        auth = HTTPBasicAuth(user, api_token)
        response = requests.post(url=url, headers=headers, auth=auth, data=payload)
        return response.text
    
    def format_payload(self, ticket_data):
        ticket_row = ticket_data.rsplit("|")
        payload_string = '{"fields":{"project":{"id":"10000"},"summary":"Teste ticket aberto pelo José","description":{"content":[{"content":[{"text":"Isso é um ticket teste, sendo criado pelo @José Henrique Lemos Xavier","type":"text"}],"type":"paragraph"}],"type":"doc","version":1},"issuetype":{"id":"10019"}}}'
        payload_json = json.loads(payload_string)
        payload_json["fields"]["description"]["content"][0]["content"][0]['text'] = ticket_row[3]
        payload_json["fields"]["summary"] = ticket_row[4]
        payload_json = json.dumps(payload_json)
        return payload_json

    def run(self, ticket_data):
        payload = self.format_payload(ticket_data=ticket_data)
        response_payload = self.create_on_jira(payload=payload)
        return response_payload


        
    





