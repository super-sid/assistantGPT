# assistantGPT
An AI chatbot which helps in generating the following:
 1. Scaffold of all kinds of BE/FE frameworks and libraries.
 2. Breaks down an engineering/product task into sub-task and creates tickets on Jira as soon as we type it in the prompt.

### How to run

1. Download Ollama package from here https://ollama.ai.
2. Install the most basic Llama Model i.e. 7B in your terminal by executing as follows:
```
ollama pull llama2
```
3. Once the model is downloaded and is up and running, clone this repository.
4. Run the following commands for
  #### Installing Dependencies 
```
pip install -r requirements.txt
```
  #### Running the project     
```
chainlit run main.py -w
```
5. After running the above project will be available to test at http://localhost:8000
6. Try it out!
