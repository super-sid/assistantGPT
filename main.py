from huggingface_hub import hf_hub_download
from llama_cpp import Llama

model_name_or_path = "TheBloke/Llama-2-13B-chat-GGML"
model_basename = "llama-2-13b-chat.ggmlv3.q5_1.bin" # the model is in bin format

model_path = hf_hub_download(repo_id=model_name_or_path, filename=model_basename)

lcpp_llm = Llama(
    model_path=model_path,
    n_threads=2, # CPU cores
    )

prompt = "Write a linear regression in python"
prompt_template=f'''SYSTEM: You are a helpful, respectful and honest assistant. Always answer as helpfully.

USER: {prompt}

ASSISTANT:
'''

response = lcpp_llm(
    prompt=prompt_template,
    max_tokens=150,
    temperature=0.5,
    top_p=0.95,
    repeat_penalty=1.2,
    top_k=50,
    echo=True
    )

print(response["choices"][0]["text"])