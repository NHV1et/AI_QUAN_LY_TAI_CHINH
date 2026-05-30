from llama_index.llms.ollama import Ollama
from llama_index.core import Settings
import json
def goi_Agent():

    llm = Ollama(
        model="finance-ai:latest", 
        request_timeout=120.0,
        additional_kwargs={
            "temperature": 0.1,
            "repeat_penalty": 1.15,
            "num_ctx": 2048,      # Hai cái thông số dưới
                                  # Nếu thấy chạy chậm thì giảm bớt đi
            "num_predict": 512,
            "num_threads": 6
        }
    )

    Settings.llm = llm
    return llm

def format_jsonl():
    input_file = "dataset_cua_Viet.jsonl"
    output_file = "../../clean.jsonl"

    buffer = ""
    objects = []

    
    with open(input_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # bắt đầu object mới
            if line.startswith("{"):
                buffer = [line]

            elif line.endswith("}"):
                buffer.append(line)
                raw = " ".join(buffer)

                try:
                    obj = json.loads(raw)
                    objects.append(obj)
                except Exception as e:
                    print("❌ lỗi parse:", raw[:100])

                buffer = []

            else:
                buffer.append(line)

    # ghi ra JSONL
    with open(output_file, "w", encoding="utf-8") as f:
        for obj in objects:
            f.write(json.dumps(obj, ensure_ascii=False) + "\n")

    print("✅ Số object:", len(objects))


format_jsonl()