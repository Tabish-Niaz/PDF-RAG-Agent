# import os 
# import tempfile
# import streamlit as st
# from langchain_community.document_loaders import PyPDFLoader
# from langchain_community.vectorstores import FAISS
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.runnables import RunnablePassthrough
# from langchain_openai import ChatOpenAI, OpenAIEmbeddings
# from langchain_text_splitters import RecursiveCharacterTextSplitter


# st.set_page_config(page_title="PDF RAG Agent", page_icon="📄", layout="wide")
# st.title("📄 PDF RAG Agent")
# st.caption("Upload a PDF, then ask question - answers come only from the document.") 


# with st.sidebar:
#     st.header("Settings")
#     api_key = st.text_input("OpenAI API Key", type="password", value=os.getenv("OPENAI_API_KEY"))
#     model_name = st.selectbox("Chat model", ["gpt-4o-mini", "gpt-4o", "gpt-4.1-mini"])
#     chunk_size = st.slider("Chunk size", 500, 2000, 1000, step=100)
#     chunk_overlap = st.slider("Chunk overlap", 0, 400, 150, step=50)
#     top_k = st.slider("Retrieved chunks (k)", 2, 10, 4)


# if not api_key:
#     st.info("Enter your OpenAI API key in the sidebar to begin.")
#     st.stop()


# os.environ["OPENAI_API_KEY"] = api_key


# uploaded_pdf = st.file_uploader("Upload a PDF", type=["pdf"])


# def build_vectorstore(pdf_bytes: bytes, size: int, overlap: int) -> FAISS:
#     with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
#         tmp.write(pdf_bytes)
#         tmp_path = tmp.name

#     try:
#         docs = PyPDFLoader(tmp_path).load()
#     finally:
#         os.unlink(tmp_path)

#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size = size,
#         chunk_overlap = overlap,
#         separators=["\n\n", "\n", ". ", " ", ""]
#     )
#     chunks = splitter.split_documents(docs)

#     embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
#     return FAISS.from_documents(chunks, embeddings)

# if uploaded_pdf is not None:
#     file_sig = (uploaded_pdf.name, uploaded_pdf.size, chunk_size, chunk_overlap)
#     if st.session_state.get("file_sig") != file_sig:
#         with st.spinner("Reading and indexing PDF..."):
#             st.session_state.vectorstore = build_vectorstore(
#                 uploaded_pdf.getvalue(), chunk_size, chunk_overlap
#             )
#             st.session_state.file_sig = file_sig
#             st.session_state.messages = []
#         st.success(f"Indexed **{uploaded_pdf.name}** - ask away!")

# # def format_docs(docs):
# #     return "\n\n".join(
# #         f"Page {doc.metadata.get('page', '?') + 1}: {doc.page_content}"
# #         for doc in docs
# #     )

# def format_docs(docs):
#     return "\n\n".join(
#         f"Page {doc.metadata.get('page', 0) + 1}: {doc.page_content}"
#         for doc in docs
#     )


# RAG_PROMPT = ChatPromptTemplate.from_messages([
#     ("system",
#      "You are a helpful assistant that answers questions strictly using the "
#      "provided context from a PDF document.\n"
#      "Rules:\n"
#      "1. Answer ONLY from the context below.\n"
#      "2. If the answer is not in the context, say: "
#      "\"I couldn't find that in the document.\"\n"
#      "3. Cite the page number(s) you used, e.g. (p. 3).\n\n"
#      "Context:\n{context}"),
#      ("human", "{question}"),
# ])


# def get_chain(vectorstore: FAISS, model: str, k: int):
#     retriever = vectorstore.as_retriever(search_kwargs={"k": k})
#     llm = ChatOpenAI(model=model, temperature=0)
#     return(
#         {"context" : retriever | format_docs, "question": RunnablePassthrough()}
#         | RAG_PROMPT
#         | llm
#         | StrOutputParser(),
#     ), retriever


# if "vectorstore" in st.session_state:
#     if "messages" not in st.session_state:
#         st.session_state.messages = []


#     for msg in st.session_state.messages:
#         with st.chat_message(msg["role"]):
#             st.markdown(msg["content"])



#     question = st.chat_input("Ask a question about the PDF...")
#     if question:
#         st.session_state.messages.append({"role": "user", "content": question})
#         with st.chat_message("user"):
#             st.markdown(question)

#         chain, retriever = get_chain(
#             st.session_state.vectorstore, model_name, top_k
#         )



#         with st.chat_message("assistant"):
#             with st.spinner("Thinking..."):
#                 answer = chain.invoke(question)
#                 st.markdown(answer)

    
#                 with st.expander("🔍 Sources (retrieved chunks)"):
#                     for doc in retriever.invoke(question):
#                         page = doc.metadata.get("page", "?")
#                         st.markdown(f"**Page {page + 1 if isinstance(page,int) else page}**")
#                         st.text(doc.page_content[:500])
#                         st.divider()


#         st.session_state.messages.append({"role": "assistant", "content": answer})


# else:
#     st.info("👆 Upload a PDF to get started.")






# import os 
# import tempfile
# import streamlit as st
# from datetime import datetime
# from langchain_community.document_loaders import PyPDFLoader
# from langchain_community.vectorstores import FAISS
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.runnables import RunnablePassthrough
# from langchain_openai import ChatOpenAI, OpenAIEmbeddings
# from langchain_text_splitters import RecursiveCharacterTextSplitter

# # ==========================================
# # PAGE CONFIGURATION
# # ==========================================
# st.set_page_config(
#     page_title="Premium PDF RAG Agent", 
#     page_icon="📄", 
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # ==========================================
# # ADVANCED CUSTOM CSS FOR PREMIUM GLASSMORPHIC UI
# # ==========================================
# st.markdown("""
# <style>
#     /* Global Fonts & Futuristic Dark Backdrop */
#     @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
#     html, body, [class*="css"] {
#         font-family: 'Plus Jakarta Sans', sans-serif !important;
#         background-color: #0b0c10 !important;
#         color: #e2e8f0 !important;
#     }
    
#     /* Full App Glass effect */
#     .stApp {
#         background: radial-gradient(circle at top right, rgba(79, 70, 229, 0.08), transparent), 
#                     radial-gradient(circle at bottom left, rgba(147, 51, 234, 0.05), transparent),
#                     #0c0d14 !important;
#     }

#     /* Sidebar Aesthetic customization */
#     [data-testid="stSidebar"] {
#         background-color: #08090d !important;
#         border-right: 1px solid rgba(255, 255, 255, 0.04) !important;
#         padding-top: 10px;
#     }
    
#     /* Branding design matching Aura AI */
#     .brand-container {
#         background: linear-gradient(135deg, rgba(37, 99, 235, 0.1), rgba(139, 92, 246, 0.1));
#         padding: 16px;
#         border-radius: 14px;
#         margin-bottom: 20px;
#         display: flex;
#         align-items: center;
#         gap: 12px;
#         border: 1px solid rgba(99, 102, 241, 0.15);
#     }
#     .brand-logo {
#         background: linear-gradient(135deg, #2563eb, #8b5cf6);
#         border-radius: 10px;
#         width: 38px;
#         height: 38px;
#         display: flex;
#         align-items: center;
#         justify-content: center;
#         box-shadow: 0px 4px 12px rgba(37, 99, 235, 0.3);
#     }
#     .brand-title {
#         font-size: 1.15rem;
#         font-weight: 800;
#         background: -webkit-linear-gradient(45deg, #3b82f6, #a855f7);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent;
#     }

#     /* Modern sleek input fields inside sidebar */
#     .stTextInput > div > div > input, .stSelectbox > div > div > div {
#         background-color: #0f111a !important;
#         border: 1px solid rgba(255, 255, 255, 0.08) !important;
#         color: #e2e8f0 !important;
#         border-radius: 8px !important;
#     }

#     /* Message view bubbles customized padding and card blur */
#     [data-testid="chatAvatarIcon-user"] {
#         background-color: #4f46e5 !important;
#     }
#     [data-testid="chatAvatarIcon-assistant"] {
#         background: linear-gradient(135deg, #3b82f6, #a855f7) !important;
#     }
    
#     .stChatMessage {
#         border-radius: 12px;
#         margin-bottom: 12px;
#         border: 1px solid rgba(255,255,255,0.02) !important;
#     }

#     /* Premium Welcome UI screen styling */
#     .welcome-header {
#         font-size: 3.8rem;
#         font-weight: 800;
#         letter-spacing: -1.5px;
#         color: #ffffff;
#         text-align: center;
#         margin-bottom: 5px;
#     }
#     .welcome-subtext {
#         color: #94a3b8;
#         font-size: 1.15rem;
#         text-align: center;
#         margin-bottom: 30px;
#     }

#     /* Sidebar elements scroll & spacing */
#     .sidebar-section-title {
#         font-size: 0.72rem;
#         font-weight: 700;
#         color: #475569;
#         letter-spacing: 1.5px;
#         text-transform: uppercase;
#         margin-top: 24px;
#         margin-bottom: 8px;
#     }
    
#     /* Login Screen Container styling */
#     .login-wrapper {
#         border-radius: 20px;
#         background: rgba(13, 14, 22, 0.65);
#         border: 1px solid rgba(255, 255, 255, 0.05);
#         backdrop-filter: blur(20px);
#         box-shadow: 0 20px 40px rgba(0,0,0,0.4);
#     }
# </style>
# """, unsafe_allow_html=True)

# # ==========================================
# # RAG HELPER FUNCTIONS
# # ==========================================
# def build_vectorstore(pdf_bytes: bytes, size: int, overlap: int) -> FAISS:
#     with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
#         tmp.write(pdf_bytes)
#         tmp_path = tmp.name

#     try:
#         docs = PyPDFLoader(tmp_path).load()
#     finally:
#         os.unlink(tmp_path)

#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size = size,
#         chunk_overlap = overlap,
#         separators=["\n\n", "\n", ". ", " ", ""]
#     )
#     chunks = splitter.split_documents(docs)
#     embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
#     return FAISS.from_documents(chunks, embeddings)

# def format_docs(docs):
#     return "\n\n".join(
#         f"Page {doc.metadata.get('page', 0) + 1}: {doc.page_content}"
#         for doc in docs
#     )

# RAG_PROMPT = ChatPromptTemplate.from_messages([
#     ("system",
#      "You are a helpful assistant that answers questions strictly using the "
#      "provided context from a PDF document.\n"
#      "Rules:\n"
#      "1. Answer ONLY from the context below.\n"
#      "2. If the answer is not in the context, say: "
#      "\"I couldn't find that in the document.\"\n"
#      "3. Cite the page number(s) you used, e.g. (p. 3).\n\n"
#      "Context:\n{context}"),
#      ("human", "{question}"),
# ])

# def get_chain(vectorstore: FAISS, model: str, k: int):
#     retriever = vectorstore.as_retriever(search_kwargs={"k": k})
#     llm = ChatOpenAI(model=model, temperature=0)
#     return(
#         {"context" : retriever | format_docs, "question": RunnablePassthrough()}
#         | RAG_PROMPT
#         | llm
#         | StrOutputParser()
#     ), retriever

# # ==========================================
# # SESSION STATE
# # ==========================================
# if 'api_key' not in st.session_state: st.session_state.api_key = None
# if 'messages' not in st.session_state: st.session_state.messages = []
# if 'selected_model' not in st.session_state: st.session_state.selected_model = 'gpt-4o-mini'
# if 'chunk_size' not in st.session_state: st.session_state.chunk_size = 1000
# if 'chunk_overlap' not in st.session_state: st.session_state.chunk_overlap = 150
# if 'top_k' not in st.session_state: st.session_state.top_k = 4

# def login():
#     st.session_state.api_key = st.session_state.api_key_input
#     os.environ["OPENAI_API_KEY"] = st.session_state.api_key_input

# def logout():
#     st.session_state.api_key = None
#     st.session_state.messages = []
#     if "vectorstore" in st.session_state: del st.session_state.vectorstore

# def handle_preset_click(preset_text):
#     st.session_state.preset_triggered = preset_text

# # ==========================================
# # STATE 1: LOGIN PAGE
# # ==========================================
# if not st.session_state.api_key:
#     st.markdown("<br><br><br>", unsafe_allow_html=True)
#     col1, col2, col3 = st.columns([1, 1.3, 1])
#     with col2:
#         st.markdown("""
#         <div style="text-align: center; margin-bottom: 30px;">
#             <div style="display: inline-flex; align-items: center; justify-content: center; background: linear-gradient(135deg, #2563eb, #8b5cf6); border-radius: 16px; width: 60px; height: 60px; margin-bottom: 16px; box-shadow: 0 8px 24px rgba(37,99,235,0.4)">
#                 <span style="color: white; font-size: 32px;">📄</span>
#             </div>
#             <h1 style="font-size: 2.8rem; font-weight: 800; margin: 0; background: -webkit-linear-gradient(45deg, #3b82f6, #a855f7); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Docu-AI RAG</h1>
#             <p style="color: #64748b; font-size: 1.1rem; margin-top: 5px;">Unlock intelligent insights directly from your PDF documents</p>
#         </div>
#         """, unsafe_allow_html=True)
        
#         with st.form("login_form", clear_on_submit=True):
#             st.markdown("<p style='font-size:0.9rem; font-weight:600; margin-bottom:-5px; color:#94a3b8;'>OpenAI API Key</p>", unsafe_allow_html=True)
#             st.text_input("", type="password", key="api_key_input", placeholder="sk-proj-...", help="Your key runs strictly in your current tab.")
#             st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
#             st.form_submit_button("🔑 Unlock Assistant", use_container_width=True, on_click=login)

# # ==========================================
# # STATE 2: RAG CHATROOM
# # ==========================================
# else:
#     # --- Sidebar ---
#     with st.sidebar:
#         st.markdown("""
#         <div class="brand-container">
#             <div class="brand-logo">📄</div>
#             <div style="display: flex; flex-direction: column;">
#                 <span class="brand-title">Docu-AI</span>
#                 <span style="font-size: 0.72rem; color: #64748b; font-weight: 500;">PDF Document Analyzer</span>
#             </div>
#         </div>
#         """, unsafe_allow_html=True)

#         st.markdown("<p class='sidebar-section-title'>Upload Document</p>", unsafe_allow_html=True)
#         uploaded_pdf = st.file_uploader("Upload a PDF to scan", type=["pdf"], label_visibility="collapsed")

#         if uploaded_pdf is not None:
#             file_sig = (uploaded_pdf.name, uploaded_pdf.size, st.session_state.chunk_size, st.session_state.chunk_overlap)
#             if st.session_state.get("file_sig") != file_sig:
#                 with st.spinner("Indexing PDF data..."):
#                     st.session_state.vectorstore = build_vectorstore(
#                         uploaded_pdf.getvalue(), st.session_state.chunk_size, st.session_state.chunk_overlap
#                     )
#                     st.session_state.file_sig = file_sig
#                     st.session_state.messages = []
#                 st.success(f"Indexed *{uploaded_pdf.name}*")

#         st.markdown("<p class='sidebar-section-title'>Settings</p>", unsafe_allow_html=True)
#         with st.expander("⚙️ Parsing & Model Options"):
#             st.selectbox("Chat model", ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"], key="selected_model")
#             st.slider("Chunk size", 500, 2000, 1000, step=100, key="chunk_size")
#             st.slider("Chunk overlap", 0, 400, 150, step=50, key="chunk_overlap")
#             st.slider("Retrieved chunks (k)", 2, 10, 4, key="top_k")

#         st.markdown("<p class='sidebar-section-title'>Identity</p>", unsafe_allow_html=True)
#         masked_key = f"sk-...{st.session_state.api_key[-4:]}" if len(st.session_state.api_key) > 4 else "sk-..."
#         st.markdown(f"""
#         <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.04); padding: 12px; border-radius: 10px; margin-bottom: 12px;'>
#             <span style='font-size:0.75rem; color:#64748b; font-weight:600;'>CONNECTED KEY</span><br>
#             <span style='font-family:monospace; font-size:0.85rem; color:#38bdf8; font-weight:bold;'>{masked_key}</span>
#         </div>
#         """, unsafe_allow_html=True)
#         st.button("🔓 End Session", on_click=logout, use_container_width=True)

#     # --- Main Screen ---
#     if "vectorstore" not in st.session_state:
#         st.markdown("<div style='display: flex; flex-direction: column; align-items: center; justify-content: center; height: 60vh;'>", unsafe_allow_html=True)
#         st.markdown("<h2 style='color: #888; font-weight: 600;'>Upload a PDF to get started ✨</h2>", unsafe_allow_html=True)
#         st.markdown("<p style='color: #aaa;'>Please use the sidebar to upload a document.</p></div>", unsafe_allow_html=True)
#     else:
#         # Pre-chat suggestions screen
#         if len(st.session_state.messages) == 0:
#             st.markdown("<div style='height: 12vh;'></div>", unsafe_allow_html=True)
#             st.markdown("<h1 class='welcome-header'>How can I analyze<br>this document?</h1>", unsafe_allow_html=True)
#             st.markdown("<p class='welcome-subtext'>Ask questions and extract insights directly from your PDF</p>", unsafe_allow_html=True)
            
#             col_c1, col_c2, col_c3 = st.columns(3)
#             with col_c1:
#                 if st.button("📝 Summarize Document\n\n\n\n\n\nGive me a quick overview", use_container_width=True):
#                     handle_preset_click("Please provide a comprehensive summary of this document.")
#                     st.rerun()
#             with col_c2:
#                 if st.button("💡 Key Takeaways\n\n\n\n\n\nExtract main points", use_container_width=True):
#                     handle_preset_click("What are the key takeaways from this document?")
#                     st.rerun()
#             with col_c3:
#                 if st.button("🔬 Find Details\n\n\n\n\n\nLocate specific info", use_container_width=True):
#                     handle_preset_click("What are the specific conclusions or results mentioned?")
#                     st.rerun()

#         # Render chat history
#         for msg in st.session_state.messages:
#             avatar = "👤" if msg["role"] == "user" else "✨"
#             with st.chat_message(msg["role"], avatar=avatar):
#                 st.markdown(msg["content"])

#         user_prompt = st.chat_input("Ask a question about the PDF...")
#         preset_triggered = st.session_state.pop("preset_triggered", None)
#         prompt_to_use = user_prompt or preset_triggered

#         if prompt_to_use:
#             if not preset_triggered: 
#                 st.session_state.messages.append({"role": "user", "content": prompt_to_use})
#                 with st.chat_message("user", avatar="👤"):
#                     st.markdown(prompt_to_use)

#             with st.chat_message("assistant", avatar="✨"):
#                 with st.spinner("Extracting insights..."):
#                     try:
#                         chain, retriever = get_chain(
#                             st.session_state.vectorstore, 
#                             st.session_state.selected_model, 
#                             st.session_state.top_k
#                         )
#                         answer = chain.invoke(prompt_to_use)
#                         st.markdown(answer)
                        
#                         # Add Expandable Source details
#                         with st.expander("🔍 Document Sources"):
#                             for doc in retriever.invoke(prompt_to_use):
#                                 page = doc.metadata.get("page", "?")
#                                 st.markdown(f"*Page {page + 1 if isinstance(page,int) else page}*")
#                                 st.text(doc.page_content[:400] + "...")
#                                 st.divider()
                                
#                         st.session_state.messages.append({"role": "assistant", "content": answer})
#                         if preset_triggered: st.rerun()
#                     except Exception as e:
#                         st.error(f"Error: {e}")






import os 
import tempfile
import streamlit as st
import pandas as pd
from datetime import datetime
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, CSVLoader
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Premium Multi-Doc RAG Agent", 
    page_icon="📄", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Streamlit ke default Header (Fork/GitHub) aur Footer ko hide karne ka CSS
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# ==========================================
# ADVANCED CUSTOM CSS FOR PREMIUM GLASSMORPHIC UI
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        background-color: #0b0c10 !important;
        color: #e2e8f0 !important;
    }
    .stApp {
        background: radial-gradient(circle at top right, rgba(79, 70, 229, 0.08), transparent), 
                    radial-gradient(circle at bottom left, rgba(147, 51, 234, 0.05), transparent),
                    #0c0d14 !important;
    }
    [data-testid="stSidebar"] {
        background-color: #08090d !important;
        border-right: 1px solid rgba(255, 255, 255, 0.04) !important;
        padding-top: 10px;
    }
    .brand-container {
        background: linear-gradient(135deg, rgba(37, 99, 235, 0.1), rgba(139, 92, 246, 0.1));
        padding: 16px;
        border-radius: 14px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 12px;
        border: 1px solid rgba(99, 102, 241, 0.15);
    }
    .brand-logo {
        background: linear-gradient(135deg, #2563eb, #8b5cf6);
        border-radius: 10px;
        width: 38px;
        height: 38px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0px 4px 12px rgba(37, 99, 235, 0.3);
    }
    .brand-title {
        font-size: 1.15rem;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #3b82f6, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .stTextInput > div > div > input, .stSelectbox > div > div > div {
        background-color: #0f111a !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        color: #e2e8f0 !important;
        border-radius: 8px !important;
    }
    [data-testid="chatAvatarIcon-user"] {
        background-color: #4f46e5 !important;
    }
    [data-testid="chatAvatarIcon-assistant"] {
        background: linear-gradient(135deg, #3b82f6, #a855f7) !important;
    }
    .stChatMessage {
        border-radius: 12px;
        margin-bottom: 12px;
        border: 1px solid rgba(255,255,255,0.02) !important;
    }
    .welcome-header {
        font-size: 3.8rem;
        font-weight: 800;
        letter-spacing: -1.5px;
        color: #ffffff;
        text-align: center;
        margin-bottom: 5px;
    }
    .welcome-subtext {
        color: #94a3b8;
        font-size: 1.15rem;
        text-align: center;
        margin-bottom: 30px;
    }
    .sidebar-section-title {
        font-size: 0.72rem;
        font-weight: 700;
        color: #475569;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-top: 24px;
        margin-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# UNIVERSAL RAG HELPER FUNCTIONS
# ==========================================
def build_vectorstore(file_bytes: bytes, file_name: str, size: int, overlap: int) -> FAISS:
    ext = os.path.splitext(file_name)[1].lower()
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name

    try:
        if ext == ".pdf":
            docs = PyPDFLoader(tmp_path).load()
        elif ext == ".docx":
            docs = Docx2txtLoader(tmp_path).load()
        elif ext == ".csv":
            docs = CSVLoader(tmp_path).load()
        elif ext in [".xlsx", ".xls"]:
            # Excel ko pandas ke zariye read kar ke Text Documents mein convert karte hain
            df = pd.read_excel(tmp_path)
            docs = []
            for index, row in df.iterrows():
                row_text = ", ".join([f"{col}: {val}" for col, val in row.items()])
                docs.append(Document(page_content=row_text, metadata={"source": file_name, "row": index}))
        else:
            st.error("Unsupported file format!")
            return None
    finally:
        os.unlink(tmp_path)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size = size,
        chunk_overlap = overlap,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    chunks = splitter.split_documents(docs)
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    return FAISS.from_documents(chunks, embeddings)

def format_docs(docs):
    return "\n\n".join(
        f"Segment {i+1}: {doc.page_content}"
        for i, doc in enumerate(docs)
    )

RAG_PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "You are an intelligent document assistant. Your job is to extract answers strictly from the provided context.\n"
     "Rules:\n"
     "1. Answer ONLY using the context below.\n"
     "2. If the user types a short phrase (e.g., 'my name', 'phone number'), understand it as a request to extract that detail.\n"
     "3. If the answer is not present, say: \"I couldn't find that in the document.\"\n"
     "4. Cite the source context when possible.\n\n"
     "Context:\n{context}"),
     ("human", "{question}"),
])

def get_chain(vectorstore: FAISS, model: str, k: int):
    retriever = vectorstore.as_retriever(search_kwargs={"k": k})
    llm = ChatOpenAI(model=model, temperature=0)
    
    chain = (
        {"context" : retriever | format_docs, "question": RunnablePassthrough()}
        | RAG_PROMPT
        | llm
        | StrOutputParser()
    )
    return chain, retriever

# ==========================================
# SESSION STATE
# ==========================================
if 'api_key' not in st.session_state: st.session_state.api_key = None
if 'messages' not in st.session_state: st.session_state.messages = []
if 'selected_model' not in st.session_state: st.session_state.selected_model = 'gpt-4o-mini'
if 'chunk_size' not in st.session_state: st.session_state.chunk_size = 1000
if 'chunk_overlap' not in st.session_state: st.session_state.chunk_overlap = 150
if 'top_k' not in st.session_state: st.session_state.top_k = 4

def login():
    st.session_state.api_key = st.session_state.api_key_input
    os.environ["OPENAI_API_KEY"] = st.session_state.api_key_input

def logout():
    st.session_state.api_key = None
    st.session_state.messages = []
    if "vectorstore" in st.session_state: del st.session_state.vectorstore

def handle_preset_click(preset_text):
    st.session_state.preset_triggered = preset_text

# ==========================================
# STATE 1: LOGIN PAGE
# ==========================================
if not st.session_state.api_key:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.3, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 30px;">
            <div style="display: inline-flex; align-items: center; justify-content: center; background: linear-gradient(135deg, #2563eb, #8b5cf6); border-radius: 16px; width: 60px; height: 60px; margin-bottom: 16px; box-shadow: 0 8px 24px rgba(37,99,235,0.4)">
                <span style="color: white; font-size: 32px;">📑</span>
            </div>
            <h1 style="font-size: 2.8rem; font-weight: 800; margin: 0; background: -webkit-linear-gradient(45deg, #3b82f6, #a855f7); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Docu-AI RAG</h1>
            <p style="color: #64748b; font-size: 1.1rem; margin-top: 5px;">Unlock intelligent insights directly from PDF, Word, Excel, and CSV files</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form", clear_on_submit=True):
            st.markdown("<p style='font-size:0.9rem; font-weight:600; margin-bottom:-5px; color:#94a3b8;'>OpenAI API Key</p>", unsafe_allow_html=True)
            st.text_input("API Key", type="password", key="api_key_input", placeholder="sk-proj-...", help="Your key runs strictly in your current tab.", label_visibility="collapsed")
            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
            st.form_submit_button("🔑 Unlock Assistant", use_container_width=True, on_click=login)

# ==========================================
# STATE 2: RAG CHATROOM
# ==========================================
else:
    # --- Sidebar ---
    with st.sidebar:
        st.markdown("""
        <div class="brand-container">
            <div class="brand-logo">📑</div>
            <div style="display: flex; flex-direction: column;">
                <span class="brand-title">Docu-AI</span>
                <span style="font-size: 0.72rem; color: #64748b; font-weight: 500;">Multi-Document Analyzer</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<p class='sidebar-section-title'>Upload Document</p>", unsafe_allow_html=True)
        # Naye file extensions yahan add kiye gaye hain
        uploaded_file = st.file_uploader("Upload file", type=["pdf", "docx", "csv", "xlsx", "xls"], label_visibility="collapsed")

        if uploaded_file is not None:
            file_sig = (uploaded_file.name, uploaded_file.size, st.session_state.chunk_size, st.session_state.chunk_overlap)
            if st.session_state.get("file_sig") != file_sig:
                with st.spinner(f"Indexing {uploaded_file.name}..."):
                    st.session_state.vectorstore = build_vectorstore(
                        uploaded_file.getvalue(), uploaded_file.name, st.session_state.chunk_size, st.session_state.chunk_overlap
                    )
                    st.session_state.file_sig = file_sig
                    st.session_state.messages = []
                st.success(f"Indexed *{uploaded_file.name}*")

        st.markdown("<p class='sidebar-section-title'>Settings</p>", unsafe_allow_html=True)
        with st.expander("⚙️ Parsing & Model Options"):
            st.selectbox("Chat model", ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"], key="selected_model")
            st.slider("Chunk size", 500, 2000, 1000, step=100, key="chunk_size")
            st.slider("Chunk overlap", 0, 400, 150, step=50, key="chunk_overlap")
            st.slider("Retrieved chunks (k)", 2, 10, 4, key="top_k")

        st.markdown("<p class='sidebar-section-title'>Identity</p>", unsafe_allow_html=True)
        masked_key = f"sk-...{st.session_state.api_key[-4:]}" if len(st.session_state.api_key) > 4 else "sk-..."
        st.markdown(f"""
        <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.04); padding: 12px; border-radius: 10px; margin-bottom: 12px;'>
            <span style='font-size:0.75rem; color:#64748b; font-weight:600;'>CONNECTED KEY</span><br>
            <span style='font-family:monospace; font-size:0.85rem; color:#38bdf8; font-weight:bold;'>{masked_key}</span>
        </div>
        """, unsafe_allow_html=True)
        st.button("🔓 End Session", on_click=logout, use_container_width=True)

    # --- Main Screen ---
    if "vectorstore" not in st.session_state:
        st.markdown("<div style='display: flex; flex-direction: column; align-items: center; justify-content: center; height: 60vh;'>", unsafe_allow_html=True)
        st.markdown("<h2 style='color: #888; font-weight: 600;'>Upload a Document to get started ✨</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color: #aaa;'>Supports PDF, Word (docx), Excel, and CSV files.</p></div>", unsafe_allow_html=True)
    else:
        if len(st.session_state.messages) == 0:
            st.markdown("<div style='height: 12vh;'></div>", unsafe_allow_html=True)
            st.markdown("<h1 class='welcome-header'>How can I analyze<br>this document?</h1>", unsafe_allow_html=True)
            st.markdown("<p class='welcome-subtext'>Ask questions and extract insights directly from your file</p>", unsafe_allow_html=True)
            
            col_c1, col_c2, col_c3 = st.columns(3)
            with col_c1:
                if st.button("📝 Summarize Document\n\n\n\n\n\nGive me a quick overview", use_container_width=True):
                    handle_preset_click("Please provide a comprehensive summary of this document.")
                    st.rerun()
            with col_c2:
                if st.button("💡 Key Takeaways\n\n\n\n\n\nExtract main points", use_container_width=True):
                    handle_preset_click("What are the key takeaways from this document?")
                    st.rerun()
            with col_c3:
                if st.button("🔬 Find Details\n\n\n\n\n\nLocate specific info", use_container_width=True):
                    handle_preset_click("What are the specific conclusions or results mentioned?")
                    st.rerun()

        for msg in st.session_state.messages:
            avatar = "👤" if msg["role"] == "user" else "✨"
            with st.chat_message(msg["role"], avatar=avatar):
                st.markdown(msg["content"])

        user_prompt = st.chat_input("Ask a question about the document...")
        preset_triggered = st.session_state.pop("preset_triggered", None)
        prompt_to_use = user_prompt or preset_triggered

        if prompt_to_use:
            if not preset_triggered: 
                st.session_state.messages.append({"role": "user", "content": prompt_to_use})
                with st.chat_message("user", avatar="👤"):
                    st.markdown(prompt_to_use)

            with st.chat_message("assistant", avatar="✨"):
                with st.spinner("Extracting insights..."):
                    try:
                        chain, retriever = get_chain(
                            st.session_state.vectorstore, 
                            st.session_state.selected_model, 
                            st.session_state.top_k
                        )
                        answer = chain.invoke(prompt_to_use)
                        st.markdown(answer)
                        
                        # Add Expandable Source details (Updated for non-PDFs)
                        with st.expander("🔍 Document Sources"):
                            for i, doc in enumerate(retriever.invoke(prompt_to_use)):
                                page = doc.metadata.get("page", None)
                                row = doc.metadata.get("row", None)
                                
                                if page is not None:
                                    loc = f"Page {page + 1}"
                                elif row is not None:
                                    loc = f"Excel Row {row + 1}"
                                else:
                                    loc = f"Extracted Segment {i + 1}"
                                    
                                st.markdown(f"*{loc}*")
                                st.text(doc.page_content[:400] + "...")
                                st.divider()
                                
                        st.session_state.messages.append({"role": "assistant", "content": answer})
                        if preset_triggered: st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")