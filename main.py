from huggingface_hub import hf_hub_download
from llama_cpp import Llama

model_name_or_path = "TheBloke/Llama-2-13B-chat-GGML"
model_basename = "llama-2-13b-chat.ggmlv3.q5_1.bin" # the model is in bin format

model_path = hf_hub_download(repo_id=model_name_or_path, filename=model_basename)

lcpp_llm = Llama(
    model_path=model_path,
    n_threads=2, # CPU cores
    )

print("MODEEELLLLLL", lcpp_llm.params.n_gpu_layers)