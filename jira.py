import requests
import json


def create_jira_ticket(ticket_data_array):
    url = "https://hackathon-test.atlassian.net/rest/api/2/issue/"
    headers = {
        "Accept": "application/json",
        "Content-type": "application/json"
    }
    tickets = json.loads(ticket_data_array).get("tasks")
    for ticket_data in tickets:
            payload = json.dumps(
                {
                    "fields": {
                        "project":
                        {
                            "key": "HAC"
                        },
                        "summary": ticket_data["name"],
                        "description": ticket_data["description"],
                        "issuetype": {
                            "name": "Task"
                        },
                    }
                }
            )

            response = requests.post(url, headers=headers, data=payload, auth=("ashwin.manohar@tifin.com",
                                                                       "ATATT3xFfGF0De2KuzeSj01yF0vYW9DmRdSHhbRHeVFhagfY2WxH8YJn8tdFTXNIZrR5jr-UEt_L3fDeD8VQqdLmlYUXMsrygObuLxCu-TbG3VQAK3ZoSXUH880eQDpoOXH7bZ0Tbf6hZlmtK6YZAW9w42BjKluxZJ4NzmQUJHElflQEn2hokYM=984CF0AA"))            
            print(response.text)
