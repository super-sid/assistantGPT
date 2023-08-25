from json import tool
from langchain.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain import PromptTemplate, LLMChain
from langchain.agents.tools import Tool
from langchain_experimental.plan_and_execute import PlanAndExecute, load_agent_executor, load_chat_planner
from langchain.agents.tools import Tool
from langchain import LLMChain
                                 
llm = Ollama(base_url="http://127.0.0.1:11434", 
             model="llama2", 
             callback_manager = CallbackManager([StreamingStdOutCallbackHandler()]),
             verbose=True
             )

template = """USER: {question}
ASSISTANT: You are a coding expert who provides all the necessary code for the requirements."""
prompt = PromptTemplate(template=template, input_variables=["question"])

llm_chain = LLMChain(prompt=prompt,llm=llm, verbose=True)

tools = [
    Tool(
        name="Programmer",
        func=llm_chain.run,
        description="You are a coding expert who provides all the necessary code for the requirements."
    ),
]

planner = load_chat_planner(llm)
executor = load_agent_executor(llm, tools, verbose=True)
agent = PlanAndExecute(planner=planner, executor=executor, verbose=True)
agent.run("How to create a basic blog apis with python?")