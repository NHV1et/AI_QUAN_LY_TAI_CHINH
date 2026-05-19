import streamlit as st
import os
from datetime import datetime
import core.utils.chat_control as cc
from llama_index.core.base.llms.types import ChatMessage, MessageRole
def init_page_config():
    st.title("💰 Hybrid Finance AI Agent")
    st.caption("AI Chatbot tư vấn tài chính do NHV đẹp trai phát triển")

def render_ui(query_engine, save_func, load_func, history_dir):
    # --- 1. SIDEBAR: QUẢN LÝ LỊCH SỬ ---
    with st.sidebar:
        st.title("💬 Finance AI")
        if st.button("➕ Cuộc trò chuyện mới", use_container_width=True):
            st.session_state.messages = []
            st.session_state.session_id = None
            st.rerun()
        
        st.markdown("---")
        st.subheader("Gần đây")
        
        history_files = []
        if os.path.exists(history_dir):
            history_files = sorted(
                [f for f in os.listdir(history_dir) if f.endswith(".json")], 
                reverse=True
            )

        if not history_files:
            st.info("Chưa có cuộc trò chuyện nào giữa tôi và bạn, hãy bắt đầu nào!")
        else:
            for file_name in history_files:
                chat_id = file_name.replace(".json", "")
                display_name = chat_id.split('_')[0].replace("_", " ") # Lấy phần chữ trước phần thời gian
                if len(display_name) > 15:
                    display_name = display_name[:12] + "..."

                col_chat, col_menu = st.columns([4, 1])
                with col_chat:
                    if st.button(f"📌 {display_name}", key=f"select_{chat_id}", use_container_width=True):
                        st.session_state.messages = load_func(file_name)
                        st.session_state.session_id = chat_id
                        st.rerun()

                with col_menu:
                    with st.popover("⋮", help="Tùy chọn"):
                        new_name_input = st.text_input("Tên mới:", key=f"edit_{chat_id}")
                        if st.button("Lưu tên", key=f"save_{chat_id}"):
                            new_id = cc.rename_chat(chat_id, new_name_input, history_dir)
                            if st.session_state.get("session_id") == chat_id:
                                st.session_state.session_id = new_id
                            st.rerun()
                        
                        st.markdown("---")
                        if st.button("🗑️ Xóa đoạn chat", key=f"del_{chat_id}", type="primary"):
                            cc.delete_chat(chat_id, history_dir)
                            if st.session_state.get("session_id") == chat_id:
                                st.session_state.messages = []
                                st.session_state.session_id = None
                            st.rerun()

    # --- 2. HIỂN THỊ NỘI DUNG CHAT ---
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Chỗ này là hiển thị tin nhắn trong một phiên 
    # Kiểu tin giữa bot với user qua lại cho nhau thì nhét vào cái container này 
    # Nó di chuyển bằng cái cuộn cuộn, do t muốn nhái thao tác mấy  
    # con AI phổ biến kiểu gemini, chat, claude,...
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # --- 3. XỬ LÝ NHẬP LIỆU VÀ PHẢN HỒI ---
    if prompt := st.chat_input("Nhập câu hỏi..."):
        
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_container:
            with st.chat_message("user"):
                st.markdown(prompt)

        
        with chat_container:
            with st.chat_message("assistant"):
                # Cái spinner này nó quay quay với load chữ để user biết là 
                # con Ai không bị treo, nó đang load thôi
                with st.spinner("Đang suy nghĩ..."):
                
                    response = query_engine.query(prompt)

                    if hasattr(response, "response_gen"):
                        full_response = st.write_stream(response.response_gen)
                    else:
                        full_response = st.write(str(response))
            
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        
        
        if not st.session_state.get("session_id"):
            # Cái id đoạn chat này chủ yếu để lưu lịch sử đoạn chat 
            # Có thể có kiểu lưu khác hay hơn? 
            # #
            clean_content = "".join(e for e in prompt[:20] if e.isalnum() or e == " ")
            clean_content = clean_content.strip().replace(" ", "_")
            time_str = datetime.now().strftime("%H%M%S")
            st.session_state.session_id = f"{clean_content}_{time_str}"
        
        save_func(st.session_state.session_id, st.session_state.messages)
        
        st.rerun()

        # Sau này bổ sung thêm sửa tên đoạn chat với xóa đoạn chat rồi 
        # Thì ném lại vô đây do người dùng thao tác trên giao diện là chủ yếu mà 
        # Mà nhớ là viết ở trong cái utils/chat_control nhé do t tổ chức theo kiểu modules
        # Để về sau cần sửa chỗ nào thì chỉ việc sửa chỗ đấy thôi cho code đỡ ngu.
        # T cũng note ở bên chat_control rồi#


        