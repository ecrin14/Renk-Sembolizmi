import streamlit as st
import os
import getpass
from langchain.chains import RetrievalQA
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.prompts import PromptTemplate 

# -------------------------------------------------------------------------
# AYARLAR VE GİZLİ ANAHTAR YÖNETİMİ
# -------------------------------------------------------------------------
PDF_DOSYA_ADI = "proje_belgem.pdf" 
CHROMA_DB_DIR = "./chroma_db"

# API Anahtarını Streamlit Secrets'tan (Ortam Değişkeni) Okuma
# Streamlit Cloud'da 'GEMINI_API_KEY' adıyla girdiğiniz anahtar buraya gelir.
API_KEY = os.environ.get('GEMINI_API_KEY') or os.environ.get('GOOGLE_API_KEY') 

if not API_KEY:
    st.error("❌ HATA: API Anahtarı (GEMINI_API_KEY) bulunamadı. Lütfen Streamlit Secrets'ı kontrol edin.")
    st.stop()
    
# -------------------------------------------------------------------------
# FONKSİYON 1: Vektör Veritabanını Kurma ve Önbellekleme
# -------------------------------------------------------------------------
@st.cache_resource
def setup_vector_store(api_key, pdf_path):
    st.info("Veri seti yükleniyor ve RAG sistemi hazırlanıyor. Lütfen bekleyin...")
    
    if not os.path.exists(pdf_path):
        st.error(f"❌ KRİTİK HATA: Veri dosyası ({pdf_path}) bulunamadı. Dosyanın GitHub'a yüklü olduğundan emin olun.")
        return None
    
    try:
        # 1. Veri Yükleme ve Parçalama (Optimize edilmiş ayarlar)
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50)
        texts = text_splitter.split_documents(documents)

        # 2. Embedding Modeli
        embedding_model = GoogleGenerativeAIEmbeddings(
            model="models/text-embedding-004", 
            google_api_key=api_key
        ) 
        
        # 3. Vektör Veritabanı Oluşturma
        vectorstore = Chroma.from_documents(
            documents=texts,
            embedding=embedding_model,
            persist_directory=CHROMA_DB_DIR
        )
        st.success(f"✅ {len(texts)} adet metin parçası ile Vektör Veritabanı başarıyla kuruldu.")
        return vectorstore
        
    except Exception as e:
        st.error(f"❌ Veri setini işlerken hata oluştu: {e}")
        return None

# -------------------------------------------------------------------------
# FONKSİYON 2: RAG Zincirini Kurma ve Önbellekleme
# -------------------------------------------------------------------------
@st.cache_resource
def setup_rag_chain(vectorstore, api_key):
    if vectorstore is None:
        return None
    
    # LLM (Sıcaklık 0.1: Daha düşük yaratıcılık)
    llm = ChatGoogleGenerativeAI(
        model="models/gemini-2.5-flash", 
        temperature=0.1, 
        google_api_key=api_key
    )

    # Prompt Template (Önceki adımda esnetilmiş ve optimize edilmiş Prompt)
    prompt_template = """Sen bir renk sembolizmi uzmanısın. Görevin, sana verilen bağlamı (renkler hakkındaki belgeyi) kullanarak kullanıcı sorularını mümkün olduğunca detaylıca cevaplamaktır. Eğer cevap bağlamda yoksa, sadece "Bu konuda elimde yeterli bilgi yok." diye cevap ver. Cevabını doğal ve açıklayıcı yap.

    Bağlam: {context}

    Soru: {question}
    Cevap:"""
    PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

    # Retriever (k=5: Daha fazla bağlam çekerek genel sorulara cevap vermeyi sağlıyor)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5}) 

    # RAG Zinciri
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": PROMPT} 
    )
    return qa_chain

# -------------------------------------------------------------------------
# STREAMLIT ARAYÜZÜ ANA KODU
# -------------------------------------------------------------------------

st.title("🎨 Renk Sembolizmi RAG Chatbot")
st.caption("Akbank GenAI Bootcamp Projesi")

# 1. Vektör Veritabanı Kurulumu
vectorstore = setup_vector_store(API_KEY, PDF_DOSYA_ADI)

# 2. RAG Zinciri Kurulumu
if vectorstore:
    qa_chain = setup_rag_chain(vectorstore, API_KEY)
    
    # Kullanıcıdan soru al
    user_query = st.text_input("Renklerin etkileri hakkında bir soru sorun:", key="input")

    if st.button("Cevapla"):
        if user_query:
            with st.spinner("Cevap aranıyor..."):
                # RAG Zincirini Çalıştır
                response = qa_chain.run(user_query)
            st.success(response)
        else:

            st.warning("Lütfen bir soru girin.")

