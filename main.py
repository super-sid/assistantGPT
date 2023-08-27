# Imports
import concurrent.futures
import logging
import chainlit as cl
from langchain.llms import Ollama
from langchain import PromptTemplate, LLMChain
from langchain.memory import ConversationBufferMemory
from pathlib import Path
import random
import yaml
from constants import *
from utils.githubOperations import githubOperations

# Setup
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
logger = logging.getLogger(__name__)
llm = Ollama(
    base_url="http://127.0.0.1:11434", 
    model="llama2:13b", 
    temperature=0
)

def generate_project_name_with_dash():
    # Predefined list of adjectives and nouns for generating project names
    adjectives = ["swift", "epic", "nova", "quantum", "zenith", "astral", "nebula", "dynamic", "silent", "radiant"]
    nouns = ["orion", "pulse", "horizon", "nexus", "voyager", "harbinger", "specter", "vertex", "mystic", "echo"]

    # Generating a random project name by choosing from the lists
    random_adjective = random.choice(adjectives)
    random_noun = random.choice(nouns)

    return f"{random_adjective}-{random_noun}"

project_name = generate_project_name_with_dash()

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
    
    # Call the chain asynchronously
    res = await cl.make_async(llm_chain)(
        message, callbacks=[cl.LangchainCallbackHandler()]
    )

    chain_output = llm_chain.predict(project_idea=res)
    print("DATTTTTTAAAA", clean_yaml_tabs(chain_output.strip()))
    project_structure = yaml.safe_load(chain_output.strip())
    # print("asojdioasjdiaiodasd", project_structure)
    # cache the project structure
    _write_file(
        ".boilerplate_x", yaml.safe_dump(project_structure)
    )
    generate_project_files(llm_chain_files, res, project_structure)
    githubOperations(False, 'Initial commit', project_name, project_name)
    # Do any post processing here

    # "res" is a Dict. For this chain, we get the response by reading the "text" key.
    # This varies from chain to chain, you should check which key to read.
    await cl.Message(content=res["text"]).send()
    return llm_chain

def generate_project_files(llm_chain_files, prompt, project_structure: list[str]) -> None:
    """Generates the project files."""
    project_structure_str = yaml.safe_dump(project_structure)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for key in project_structure:
            project_structure = project_structure[key]
        for file_name in project_structure:
            if (Path(project_name) / file_name).exists():
                logger.info(f"File already exists: {file_name}")
                continue
            if (Path(project_name) / file_name).suffix == "":
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
        print("FILEEE CONTENTS BEFOREEEEE", file_content)
        file_content = extract_code(file_content)
        print("FILEEE CONTENTS", file_content)
        _write_file(file_name, file_content)

def _write_file(file_name: str, file_content: str):
    """Writes the file to the output path."""
    file_path = Path(project_name) / file_name
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(file_content)

def extract_code(text):
    # A helper function to check if a line is a language identifier
    def is_language_identifier(line):
        # We assume that a line is a language identifier if it contains only alphabetical characters
        return line.isalpha()

    # Splitting based on triple backticks
    if "```" in text:
        blocks = text.split("```")
        
        # Filtering out empty blocks and taking every alternate block starting from the second one, which should contain the code
        code_blocks = [block.strip() for block in blocks if block.strip()][1::2]
        
        # Joining the blocks while ignoring the lines with backticks or language identifiers
        return "\n".join([line for block in code_blocks for line in block.splitlines() if not (line.strip().startswith("```") or is_language_identifier(line.strip()))])

    # Splitting based on triple dashes
    if "---" in text:
        blocks = text.split("---")
        
        # Filtering out empty blocks and taking every alternate block starting from the second one, which should contain the code
        code_blocks = [block.strip() for block in blocks if block.strip()][1::2]
        
        # Joining the blocks while ignoring the lines with dashes or language identifiers
        return "\n".join([line for block in code_blocks for line in block.splitlines() if not (line.strip().startswith("---") or is_language_identifier(line.strip()))])

    # Splitting based on <code></code> tags
    if "<code>" in text and "</code>" in text:
        blocks = text.split("<code>")
        end_blocks = [block.split("</code>")[0] for block in blocks if "</code>" in block]
        
        # Joining the blocks while ignoring the lines with code tags or language identifiers
        return "\n".join([line.strip() for block in end_blocks for line in block.splitlines() if not (line.strip().startswith("<code>") or line.strip().startswith("</code>") or is_language_identifier(line.strip()))])
    
    return text

def clean_yaml_tabs(yaml_content):
    # Detect the level of indentation before a tab
    lines = yaml_content.split('\n')
    cleaned_lines = []
    
    for line in lines:
        if '\t' in line:
            spaces_before_tab = len(line) - len(line.lstrip())
            # Replace tabs with newline and appropriate indentation
            line = line.replace('\t', '\n' + ' ' * spaces_before_tab)
        cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines)