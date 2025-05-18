import streamlit as st
from src import config
from src.core_logic import PDFProcessor, TextProcessor, VectorStoreManager, ChatChainManager

class ChatbotUI:
    def __init__(self):
        st.set_page_config(page_title=config.PAGE_TITLE, page_icon=config.PAGE_ICON)
        self.pdf_processor = PDFProcessor()
        self.text_processor = TextProcessor()
        self.vector_store_manager = VectorStoreManager()
        
        if not config.OPENROUTER_API_KEY:
            st.error(config.ERROR_MISSING_API_KEY)
            st.stop()
        
        try:
            self.chat_chain_manager = ChatChainManager(api_key=config.OPENROUTER_API_KEY)
        except ValueError as e:
            st.error(str(e))
            st.stop()

        if "conversation" not in st.session_state:
            st.session_state.conversation = None
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        if "processed_pdfs" not in st.session_state:
            st.session_state.processed_pdfs = False

    def _display_sidebar(self):
        with st.sidebar:
            st.subheader("Your Documents")
            pdf_docs = st.file_uploader("Upload your PDFs here and click 'Process'", 
                                        accept_multiple_files=True, type="pdf")

            if st.button("Process Documents"):
                if pdf_docs:
                    with st.spinner("Processing PDFs..."):
                        try:
                            raw_text = self.pdf_processor.get_text_from_pdfs(pdf_docs)
                            if not raw_text.strip():
                                st.warning("No text could be extracted from the uploaded PDF(s). Please check the files.")
                                st.session_state.processed_pdfs = False
                                return

                            text_chunks = self.text_processor.get_text_chunks(raw_text)
                            if not text_chunks:
                                st.warning("Could not split text into chunks. The document might be too short or empty after extraction.")
                                st.session_state.processed_pdfs = False
                                return

                            vectorstore = self.vector_store_manager.create_vector_store(text_chunks)
                            if not vectorstore:
                                st.error("Failed to create vector store. Please check logs.")
                                st.session_state.processed_pdfs = False
                                return

                            st.session_state.conversation = self.chat_chain_manager.get_conversation_chain(vectorstore)
                            st.session_state.chat_history = []
                            st.session_state.processed_pdfs = True
                            st.success("PDFs processed successfully! You can now ask questions.")
                        except Exception as e:
                            st.error(f"{config.ERROR_PROCESSING_PDF}: {e}")
                            st.session_state.processed_pdfs = False
                else:
                    st.warning("Please upload PDF documents first.")

    def _display_chat_history(self):
        for i, message in enumerate(st.session_state.chat_history):
            if i % 2 == 0: 
                 with st.chat_message("user"):
                    st.markdown(message.content)
            else: 
                with st.chat_message("assistant"):
                    st.markdown(message.content)

    def _handle_user_input(self, user_question):
        if st.session_state.conversation:
            with st.spinner("Thinking..."):
                try:
                    response = st.session_state.conversation({'question': user_question})
                    st.session_state.chat_history = response['chat_history'] 
                except Exception as e:
                    st.error(f"Error during conversation: {e}")
                    from langchain_core.messages import AIMessage
                    st.session_state.chat_history.append(AIMessage(content=f"Sorry, I encountered an error: {e}"))

        else:
            st.warning(config.ERROR_NO_PDF_PROCESSED)

    def run(self):
        st.header(config.PAGE_TITLE + " " + config.PAGE_ICON)
        
        self._display_sidebar()
        self._display_chat_history()

        user_question = st.chat_input("Ask a question about your documents:")
        if user_question:
            if not st.session_state.processed_pdfs:
                st.warning(config.ERROR_NO_PDF_PROCESSED)
            else:
                self._handle_user_input(user_question)
                st.rerun()