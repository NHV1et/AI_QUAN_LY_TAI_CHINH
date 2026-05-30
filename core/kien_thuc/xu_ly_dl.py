
import os
from core.llm.AI import goi_Agent
from llama_index.core.chat_engine import SimpleChatEngine

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Cấu hình lại đường dẫn trỏ thẳng đến file gguf.
# Dựa theo cây thư mục của bạn, file nằm ở thư mục gốc (ngang hàng với app.py)
PROJECT_ROOT = os.path.join(BASE_DIR, "..", "..") 
MODEL_PATH = os.path.join(PROJECT_ROOT, "llama-3.2-3b-instruct.Q4_K_M.gguf")

def get_chat_engine():
    """
    Khởi tạo Chat Engine sử dụng chính model Ollama từ hàm goi_Agent.
    """
    # Gọi hàm của bạn để lấy thực thể LLM từ Ollama
    llm = goi_Agent()
    
    # Thiết lập tường minh ngữ cảnh cho Chat Engine dựa trên Ollama LLM
    chat_engine = SimpleChatEngine.from_defaults(
        llm=llm,
    )
    return chat_engine