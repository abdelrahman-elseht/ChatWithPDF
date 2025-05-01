import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from langchain_huggingface import HuggingFaceEmbeddings
from openai import OpenAI
from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI

# client = OpenAI(
#   base_url="https://openrouter.ai/api/v1",
#   api_key="<OPENROUTER_API_KEY>",
# )

# completion = client.chat.completions.create(
#   extra_headers={
#     "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
#     "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
#   },
#   extra_body={},
#   model="qwen/qwen3-30b-a3b:free",
#   messages=[
#     {
#       "role": "user",
#       "content": "What is the meaning of life?"
#     }
#   ]
# )
# print(completion.choices[0].message.content)


def get_vector_store(text_chunks):
    # embeddings=SentenceTransformer(
    #     "all-MiniLM-L6-v2",
    # )

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


def get_pdf_texxt(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks 

def get_conversation_chain(vectorstore):
    memory = ConversationBufferMemory(
        memory_key='chat_history',
        return_messages=True
    )
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(
            base_url="https://openrouter.ai/api/v1",
            model="qwen/qwen3-30b-a3b:free",
            temperature=0.1
            ),
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']
    st.write(response['answer'])

def main():
    load_dotenv()
    st.set_page_config(page_title='Chat with multiple PDFs', page_icon=':books:')

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    st.header("Chat with multiple PDFs")

    user_question = st.text_input('ask your question')
    if user_question:
        handle_userinput(user_question)

    with st.sidebar:
        st.subheader('Your documents')
        pdf_docs = st.file_uploader("Upload your PDFs", accept_multiple_files=True)
        if st.button('Process'):
            with st.spinner('Processing'):
                raw_text = get_pdf_texxt(pdf_docs)
                st.write(raw_text)

                text_chunks = get_text_chunks(raw_text)
                st.write(text_chunks)

                vectorstore = get_vector_store(text_chunks)

                st.session_state.conversation = get_conversation_chain(vectorstore)

if __name__ == '__main__':
    main()
                
