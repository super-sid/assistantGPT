import requests
import json

access_token = "ATATT3xFfGF0emz_aSBPPcbmZIotwLiJj14mf_bCLpua1Vj3csoTIHdQIZJkKa1QMGN5_yEX4v48aVhmszVjD8DXRhBvtt0m_HyzfMUF9uoOPKM6a8Z5yIewrXctLB6WwJzRH0SyjF39Seb6l0nfOtD7NfZ-MOuE-9-a0n_WPnYzALqqYMd0Cm0=2C32570A"
user_email = "ashwin.manohar@tifin.com"


def create_jira_ticket(ticket_data_array):
    url = "https://hackathon-test.atlassian.net/rest/api/2/issue/"
    headers = {"Accept": "application/json", "Content-type": "application/json"}
    tickets = json.loads(ticket_data_array).get("tasks")
    for ticket_data in tickets:
        payload = json.dumps(
            {
                "fields": {
                    "project": {"key": "HAC"},
                    "summary": ticket_data["name"],
                    "description": ticket_data["description"],
                    "issuetype": {"name": "Task"},
                }
            }
        )

        response = requests.post(
            url,
            headers=headers,
            data=payload,
            auth=(
                user_email,
                access_token,
            ),
        )
        print(response.text)
