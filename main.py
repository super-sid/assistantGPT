from langchain.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler                                  
llm = Ollama(base_url="http://127.0.0.1:11434", 
             model="llama2", 
             callback_manager = CallbackManager([StreamingStdOutCallbackHandler()]))

llm("Write crud in fastapi")