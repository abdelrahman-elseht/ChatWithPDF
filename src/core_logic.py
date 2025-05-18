from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI
from src import config 

class PDFProcessor:
    def get_text_from_pdfs(self, pdf_docs):
        text = ""
        if not pdf_docs:
            return text
        for pdf in pdf_docs:
            try:
                pdf_reader = PdfReader(pdf)
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text
            except Exception as e:
                print(f"Error reading PDF {pdf.name if hasattr(pdf, 'name') else 'Unnamed PDF'}: {e}")
        return text

class TextProcessor:
    def __init__(self, chunk_size=config.TEXT_CHUNK_SIZE, chunk_overlap=config.TEXT_CHUNK_OVERLAP):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len
        )

    def get_text_chunks(self, text):
        if not text:
            return []
        return self.text_splitter.split_text(text)

class VectorStoreManager:
    def __init__(self, embedding_model_name=config.EMBEDDING_MODEL_NAME):
        self.embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)

    def create_vector_store(self, text_chunks):
        if not text_chunks:
            return None
        try:
            vectorstore = FAISS.from_texts(texts=text_chunks, embedding=self.embeddings)
            return vectorstore
        except Exception as e:
            print(f"Error creating vector store: {e}")
            return None

class ChatChainManager:
    def __init__(self, api_key, base_url=config.OPENROUTER_BASE_URL, model_name=config.LLM_MODEL_NAME, temperature=config.LLM_TEMPERATURE):
        if not api_key:
            raise ValueError(config.ERROR_MISSING_API_KEY)
        
        self.llm = ChatOpenAI(
            openai_api_key=api_key, 
            base_url=base_url,
            model=model_name,
            temperature=temperature,
        )

    def get_conversation_chain(self, vectorstore):
        if not vectorstore:
            return None
        
        memory = ConversationBufferMemory(
            memory_key='chat_history',
            return_messages=True
        )
        conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=vectorstore.as_retriever(),
            memory=memory
        )
        return conversation_chain