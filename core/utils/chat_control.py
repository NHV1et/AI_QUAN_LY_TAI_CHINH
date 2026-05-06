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
            # indent=4 giúp file JSON dễ đọc khi bạn mở bằng VS Code
            json.dump(messages, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Lỗi khi lưu file: {e}")

def load_chat(file_name):
    """
    Đọc dữ liệu từ file JSON và trả về danh sách tin nhắn.
    """
    # Nếu file_name chưa có đuôi .json thì thêm vào
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
    """
    Trả về danh sách các phiên chat đã lưu để hiển thị lên Sidebar.
    """
    if not os.path.exists(HISTORY_DIR):
        return []
    # Lấy các file .json và sắp xếp theo thời gian mới nhất
    files = [f for f in os.listdir(HISTORY_DIR) if f.endswith(".json")]
    return sorted(files, reverse=True)

# Sau viết nốt cái hàm: đổi tên đoạn chat và xóa đoạn chat.