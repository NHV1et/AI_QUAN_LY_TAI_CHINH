from datetime import datetime

import streamlit as st
import core.giao_dien.gui as ui
from core.llm.AI import goi_Agent
from core.kien_thuc.xu_ly_dl import get_query_engine
from core.utils.chat_control import save_chat, load_chat


ui.init_page_config()

# Hàm dùng để nạp tài nguyên nặng (Chỉ chạy 1 lần duy nhất)
@st.cache_resource
def initial_resources():
    
    goi_Agent()
    
    engine = get_query_engine()
    return engine

# 3. Thực thi nạp tài nguyên với hiệu ứng chờ
if "query_engine" not in st.session_state:
    with st.spinner("Đang khởi động hệ thống tài chính..."):
        st.session_state.query_engine = initial_resources()

if "session_id" not in st.session_state:
    st.session_state.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")

if "messages" not in st.session_state:
    st.session_state.messages = []

if st.session_state.query_engine:
    ui.render_ui(
        query_engine = st.session_state.query_engine,
        save_func = save_chat,
        load_func = load_chat,
        history_dir = r"core\chat_his"
    )