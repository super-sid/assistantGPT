JIRA_DESCRIPTION = "You are an agent to create jira task based on the requirements provided."


JIRA_TEMPLATE = template = """{description}

You need to elaborate tasks and breakdown to smaller tasks and return a list of tasks with just summary description with no nested tasks and return in json format for that particular topic and print only the json with no explanation and wrap json in <code></code> blocks :

Project idea: {project_idea}

Output:"""
