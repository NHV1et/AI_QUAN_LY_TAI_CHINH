from llama_index.llms.ollama import Ollama
from llama_index.core import Settings

def goi_Agent():
    llm = Ollama(
        model="finance-ai:latest", 
        request_timeout=120.0,
        additional_kwargs={
            "temperature": 0.1,
            "repeat_penalty": 1.3,
            "num_ctx": 4096,      
            "num_predict": 2048   
        }
    )
    Settings.llm = llm
    return llm