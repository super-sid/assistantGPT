from langchain import LLMChain


def clissifyPrompt(input_prompt='', llm=LLMChain):
    prompt = """Classify the following user query as either 'coding' or 'jira'. " \
    "A 'coding' query typically asks you to questions related to coding, api, building a repository " \
    "'jira' query typically asks you about tasks and jira" \
    "Here are some examples of each type:\n\n"""

    prompt += "Examples of 'coding' queries:\n Create a react repo"
    prompt += "\n\nExamples of jira ticket:\n Create a jira ticket"

    prompt += "\n\nReturn the and with just the type without any explanation. Like just 'coding' or 'jira'"

    prompt += "Now, determine the type of the following user query:\n"
    input_prompt = '''Create a task to assign surya'''

    prompt += f"USER: {input_prompt}\n\nClassification: "

    print(prompt)

    res = llm(prompt)

    if "jira" in res.lower():
        return 'jira'
    elif 'coding' in res.lower():
        return 'coding'
    else:
        return None
