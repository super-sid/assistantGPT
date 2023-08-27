import requests
import json


def create_jira_ticket(ticket_data_array):
    url = "https://hackathon-test.atlassian.net/rest/api/2/issue/"
    headers = {
        "Accept": "application/json",
        "Content-type": "application/json"
    }

    for ticket_data in json.loads(ticket_data_array.split("json")[1]):
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
                                                                       "ATATT3xFfGF0iVChSDll1LpJBMMohjOd6Dpun-eJzpq12QqtGXqi3GcuLRiHrpWFeqUcxRlJLj7Y15YBpNFPshpEMRENrsCvzpBnR_psgIMnXhLeB9YGm3MIx9ebkTZZcFo9enIoT2lU-RM7KMwG70ZWGoIyS47IgD_1Z3PMPHnzocITvyvdHvA=A7D16B0B"))            
            print(response.text)
