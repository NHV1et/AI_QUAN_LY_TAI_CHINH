import json
import os


HISTORY_DIR = r"core\chat_his"

def save_chat(session_id, messages):
    """
    Lưu danh sách tin nhắn vào file JSON.
    """
    if not os.path.exists(HISTORY_DIR):
        os.makedirs(HISTORY_DIR)  
    file_path = os.path.join(HISTORY_DIR, f"{session_id}.json")   
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(messages, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Lỗi khi lưu file: {e}")

def load_chat(file_name):
    if not file_name.endswith(".json"):
        file_name += ".json"      
    file_path = os.path.join(HISTORY_DIR, file_name)
    
    if not os.path.exists(file_path):
        return []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Lỗi khi đọc file: {e}")
        return []

def get_all_histories():
    if not os.path.exists(HISTORY_DIR):
        return []
    files = [f for f in os.listdir(HISTORY_DIR) if f.endswith(".json")]
    return sorted(files, reverse=True)

def delete_chat(session_id, history_dir):
    file_path = os.path.join(history_dir, f"{session_id}.json")
    if os.path.exists(file_path):
        os.remove(file_path)
        return True
    return False

def rename_chat(old_id, new_name, history_dir=HISTORY_DIR):
    if not new_name:
        return old_id
    clean_name = "".join(e for e in new_name if e.isalnum() or e == " ").strip().replace(" ", "_")
    suffix = old_id.split('_')[-1] if '_' in old_id else ""
    new_id = f"{clean_name}_{suffix}" if suffix else clean_name
    old_path = os.path.join(history_dir, f"{old_id}.json")
    new_path = os.path.join(history_dir, f"{new_id}.json")
    
    if os.path.exists(old_path):
        try:
            os.rename(old_path, new_path)
            return new_id
        except Exception as e:
            print(f"Lỗi khi đổi tên file: {e}")
            return old_id
    
# Sau viết nốt cái hàm: đổi tên đoạn chat và xóa đoạn chat.
