
import os
import streamlit as st
from llama_index.core import (
    VectorStoreIndex, 
    SimpleDirectoryReader, 
    StorageContext, 
    load_index_from_storage, 
    Settings
)
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# Dẫn cứng, về sau nếu phải đóng gói thành ứng dụng thì làm lại đoạn lưu dẫn file.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "tai_lieu_RAG")
VECTOR_DB_PATH = os.path.join(BASE_DIR, "Luu_VectorDB")
INDEXED_FILES_PATH = os.path.join(BASE_DIR, "indexed_files.txt")
def build_or_update_index():
    embed_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    

    # Thử xem có file index nào chưa.
    indexed_files = set()
    if os.path.exists(INDEXED_FILES_PATH):
        with open(INDEXED_FILES_PATH, "r", encoding="utf-8") as f:
            indexed_files = set(line.strip() for line in f)

    # Lấy mấy cái dữ liệu đang trong chỗ tài liệu RAG
    current_files = set(os.listdir(DATA_PATH))

    # Xác định file mới
    new_files = current_files - indexed_files

    # Nếu chưa có DB → tạo mới
    if not os.path.exists((os.path.join(VECTOR_DB_PATH, "index.json"))):
        documents = SimpleDirectoryReader(DATA_PATH).load_data()
        index = VectorStoreIndex.from_documents(documents, embed_model=embed_model)
        index.storage_context.persist(persist_dir=VECTOR_DB_PATH)
        # Lưu lại danh sách file đã index
        with open(INDEXED_FILES_PATH, "w", encoding="utf-8") as f:
            for file in current_files:
                f.write(file + "\n")

    else:
        # Load DB cũ
        storage_context = StorageContext.from_defaults(
            persist_dir=VECTOR_DB_PATH
        )
        index = load_index_from_storage(storage_context)

        # Nếu có file mới → index bổ sung
        if new_files:
            print(f"📄 Phát hiện {len(new_files)} tài liệu mới, đang cập nhật…")

            new_docs = SimpleDirectoryReader(
                DATA_PATH,
                required_exts=None,
            ).load_data()

            index.insert_documents(new_docs, embed_model=embed_model)
            index.storage_context.persist(persist_dir=VECTOR_DB_PATH)

            with open(INDEXED_FILES_PATH, "a", encoding="utf-8") as f:
                for file in new_files:
                    f.write(file + "\n")
        else:
            print("✅ Không có tài liệu mới — dùng DB hiện tại")
    return index

@st.cache_resource
def get_query_engine():
    
    
    Settings.embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    # Check xem có cái index nào tồn tại chưa
    if os.path.exists(os.path.join(VECTOR_DB_PATH, "docstore.json")):
        #Load lại thôi
        storage_context = StorageContext.from_defaults(persist_dir=VECTOR_DB_PATH)
        index = load_index_from_storage(storage_context)
    else:
        
        index = build_or_update_index()
    
    
    return index.as_query_engine(streaming=True)