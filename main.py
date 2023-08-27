# Imports
import concurrent.futures
import logging
import chainlit as cl
from langchain.llms import Ollama
from langchain import PromptTemplate, LLMChain
from langchain.memory import ConversationBufferMemory
from pathlib import Path
from utils.githubOperations import githubOperations

import yaml
from constants import *
# Setup
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
logger = logging.getLogger(__name__)
llm = Ollama(
    base_url="http://127.0.0.1:11434", 
    model="llama2", 
    temperature=0
)

@cl.on_chat_start
def main():
    # Instantiate the chain for that user session
    prompt = PromptTemplate(template=template,
        input_variables=[
            "project_idea",
        ],
        partial_variables={"description": DESCRIPTION})
    prompt_files = PromptTemplate(template=PROJECT_FILE_TEMPLATE,
        input_variables=["project_idea", "project_structure", "file_name"],
        partial_variables={
            "description": DESCRIPTION,
        })
    llm_chain = LLMChain(prompt=prompt, llm=llm, verbose=True)
    llm_chain_files = LLMChain(prompt=prompt_files, llm=llm, verbose=True)
    

    # Store the chain in the user session
    cl.user_session.set("llm_chain", llm_chain)
    cl.user_session.set("llm_chain_files", llm_chain_files)

@cl.on_message
async def main(message: str):
    # Retrieve the chain from the user session
    llm_chain = cl.user_session.get("llm_chain")  # type: LLMChain
    llm_chain_files = cl.user_session.get("llm_chain_files")  # type: LLMChain
    print("aksjndjasndjasd", llm_chain_files)
    answer_prefix_tokens=["FINAL", "ANSWER"]

    # Call the chain asynchronously
    res = await cl.make_async(llm_chain)(
        message, callbacks=[cl.LangchainCallbackHandler(stream_final_answer=True,
        answer_prefix_tokens=answer_prefix_tokens,)]
    )

    chain_output = llm_chain.predict(project_idea=res)
    # print("askjdnjasdnjasd", chain_output)
    project_structure = yaml.safe_load(chain_output.strip())
    # print("sahdiuashdaihsd", project_structure)
    # cache the project structure
    _write_file(
        ".boilerplate_x", yaml.safe_dump(project_structure)
    )
    generate_project_files(llm_chain_files, res, project_structure)
    githubOperations(False, 'Initial commit', 'babyagi-upload-v3', 'Fastapi')
    # Do any post processing here

    # "res" is a Dict. For this chain, we get the response by reading the "text" key.
    # This varies from chain to chain, you should check which key to read.
    await cl.Message(content=res["text"]).send()
    return llm_chain

def generate_project_files(llm_chain_files, prompt, project_structure: list[str]) -> None:
    """Generates the project files."""
    # print("asdasdasdasd", llm_chain, prompt, project_structure)
    project_structure_str = yaml.safe_dump(project_structure)
    print("asdasdasd", project_structure)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for key in project_structure:
            project_structure = project_structure[key]
        for file_name in project_structure:
            print("asjndijajindasd", file_name)
            if (Path("Fastapi") / file_name).exists():
                logger.info(f"File already exists: {file_name}")
                continue
            if (Path("Fastapi") / file_name).suffix == "":
                logger.info(f"Skipping directory: {file_name}")
                continue
            logger.info(f"Generating file content: {file_name}...")
            futures.append(
                executor.submit(
                    generate_project_file, llm_chain_files, prompt, file_name, project_structure_str
                )
            )
        for future in concurrent.futures.as_completed(futures):
            if future.exception() is not None:
                logger.error(f"Failed to generate file: {future.exception()}")

def generate_project_file(llm_chain_files, prompt, file_name: str, project_structure_str: str
    ) -> None:
        """Generates a single project file."""
        file_content = llm_chain_files.predict(
            project_idea=prompt,
            project_structure=project_structure_str,
            file_name=file_name,
        )
        print("asljdniajosdjasd", file_content)
        _write_file(file_name, file_content)

def _write_file(file_name: str, file_content: str):
    """Writes the file to the output path."""
    file_path = Path("Fastapi") / file_name
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(file_content)