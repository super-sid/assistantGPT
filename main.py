# Imports
import chainlit as cl
from langchain.agents import initialize_agent, AgentType
from langchain.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain import ConversationChain, PromptTemplate, LLMChain
from langchain.agents.tools import Tool
from langchain.memory import ConversationBufferMemory

# Setup
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

llm = Ollama(
    base_url="http://127.0.0.1:11434", 
    model="llama2", 
    temperature=0
)

template = """As an experienced software engineer, I understand the importance of structured projects. Given the requirement, provide a detailed folder and file structure first. Then, elaborate with the necessary code, comments, and best practices. If using specific frameworks or libraries, mention them along with their purposes.

Question: {question}
Answer: Let's think step by step."""

@cl.on_chat_start
def main():
    # Instantiate the chain for that user session
    prompt = PromptTemplate(template=template, input_variables=["question"])
    llm_chain = LLMChain(prompt=prompt, llm=llm, verbose=True)

    # Store the chain in the user session
    cl.user_session.set("llm_chain", llm_chain)

@cl.on_message
async def main(message: str):
    # Retrieve the chain from the user session
    llm_chain = cl.user_session.get("llm_chain")  # type: LLMChain

    # Call the chain asynchronously
    res = await cl.make_async(llm_chain)(
        message, callbacks=[cl.LangchainCallbackHandler()]
    )

    # Do any post processing here

    # "res" is a Dict. For this chain, we get the response by reading the "text" key.
    # This varies from chain to chain, you should check which key to read.
    await cl.Message(content=res["text"]).send()
    return llm_chain