
## 1. Overview

This project is a "Chat with multiple PDFs" application built using Streamlit, LangChain, and various Large Language Models (LLMs) accessible via OpenRouter. Users can upload PDF documents, and the application will process them to enable a conversational Q&A interface about the content of those documents. The codebase is modularized within a `src` directory for better organization and maintainability.

## 2. Features

*   **Multiple PDF Upload:** Supports uploading and processing several PDF files simultaneously.
*   **Text Extraction:** Extracts text content from uploaded PDFs.
*   **Text Chunking:** Splits extracted text into manageable chunks for embedding.
*   **Vector Embeddings:** Generates embeddings for text chunks using Sentence Transformers.
*   **Vector Store:** Stores embeddings in a FAISS vector store for efficient similarity search.
*   **Conversational Q&A:** Utilizes LangChain's `ConversationalRetrievalChain` to answer user questions based on PDF content.
*   **LLM Integration:** Connects to LLMs via OpenRouter (e.g., Qwen models).
*   **Conversation Memory:** Remembers previous parts of the conversation.
*   **User-Friendly UI:** Interactive interface built with Streamlit.
*   **Dockerized:** Includes Dockerfile and docker-compose for easy deployment.
*   **Configuration Management:** API keys and settings managed via `.env` and `config.py`.
*   **Structured Codebase:** Python modules organized under a `src` directory.

## 3. Project Structure
Use code with caution.
Markdown
pdf_chatbot_app/
├── .env # For API keys and other secrets (GITIGNORED)
├── src/ # Main application source code
│ ├── init.py # Makes 'src' a Python package
│ ├── main.py # Entry point for Streamlit application
│ ├── ui.py # Streamlit UI management class
│ ├── core_logic.py # Classes for PDF processing, text chunking, vector store, chat chain
│ └── config.py # Application configuration (model names, URLs, etc.)
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── run_streamlit.py # Helper script to run Streamlit locally
└── README.md
## 4. Technology Stack

*   **Python 3.9+**
*   **Streamlit:** For the web UI.
*   **LangChain:** Framework for building LLM applications.
    *   `PyPDF2`: For reading PDF files.
    *   `RecursiveCharacterTextSplitter`: For text chunking.
    *   `HuggingFaceEmbeddings` (via `sentence-transformers`): For text embeddings.
    *   `FAISS`: For vector storage and similarity search.
    *   `ChatOpenAI` (adapted for OpenRouter): For LLM interaction.
    *   `ConversationalRetrievalChain`: For managing Q&A with context.
    *   `ConversationBufferMemory`: For chat history.
*   **OpenAI Python Client:** Used by `langchain-openai` for API communication.
*   **OpenRouter:** Platform to access various LLMs.
*   **python-dotenv:** For managing environment variables.
*   **Docker & Docker Compose:** For containerization.

## 5. Setup and Installation

### Prerequisites

*   **Python 3.9 or higher:** [Download Python](https://www.python.org/downloads/)
*   **pip:** Python package installer.
*   **Docker Desktop (for Docker setup):** [Install Docker](https://www.docker.com/products/docker-desktop/)
*   **Git (optional, for cloning):** [Install Git](https://git-scm.com/downloads)
*   **OpenRouter API Key:** Obtain from [OpenRouter.ai](https://openrouter.ai/).

### Configuration (.env)

1.  Navigate to the root directory of the project (`pdf_chatbot_app/`).
2.  Create a file named `.env`.
3.  Add your OpenRouter API key to it:
    ```env
    OPENROUTER_API_KEY="your_actual_openrouter_api_key_here"
    # Optional:
    # YOUR_SITE_URL="https://your.site"
    # YOUR_SITE_NAME="My PDF Chatbot"
    ```
    **Important:** Ensure `.env` is listed in your `.gitignore` file to avoid committing secrets.

### Local Setup

1.  **Clone the repository (or download files):**
    ```bash
    git clone <repository_url>
    cd pdf_chatbot_app
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## 6. Running the Application

Choose one of the following methods to run the application. Ensure you have completed the "Local Setup" steps first if running locally.

### Option 1: Locally using `run_streamlit.py` (for development)

This script handles setting up `sys.path` correctly before invoking Streamlit.

1.  Ensure you are in the project root directory (`pdf_chatbot_app/`).
2.  Ensure your virtual environment is activated.
3.  Run the script:
    ```bash
    python run_streamlit.py
    ```
    The application should be accessible at `http://localhost:8501` (or the port Streamlit chooses).

### Option 2: Locally using direct `streamlit run` command

This method relies on the `sys.path` manipulation within `src/main.py`.

1.  Ensure you are in the project root directory (`pdf_chatbot_app/`).
2.  Ensure your virtual environment is activated.
3.  Run Streamlit pointing to the main script within the `src` directory:
    ```bash
    streamlit run src/main.py
    ```
    The application should be accessible at `http://localhost:8501` (or the port Streamlit chooses).

### Option 3: Using Docker (Recommended for Deployment)

1.  Ensure Docker Desktop is running.
2.  Ensure you are in the project root directory (`pdf_chatbot_app/`).
3.  Ensure your `.env` file is created in the project root as described in the Configuration section.
4.  Build and run with Docker Compose:
    ```bash
    docker-compose up --build
    ```
    To run in detached mode (in the background):
    ```bash
    docker-compose up --build -d
    ```
5.  Access the application:
    Open your web browser and navigate to `http://localhost:8501`.
6.  To stop (if using `docker-compose up`):
    Press `Ctrl+C` in the terminal.
    If in detached mode: `docker-compose down`.

## 7. Usage

1.  Open the application in your browser using the URL provided after starting.
2.  Use the sidebar to upload one or more PDF documents.
3.  Click the "Process Documents" button. Wait for the processing to complete.
4.  Once processed, you can type your questions about the documents into the chat input field at the bottom of the page and press Enter or click the send button.
5.  The chatbot will respond based on the content of the uploaded PDFs, and the conversation history will be displayed.

## 8. Code Modules

*   **`src/config.py`**: Handles loading of environment variables (like API keys) and stores application-wide configurations such as model names, URLs, and UI text.
*   **`src/core_logic.py`**:
    *   `PDFProcessor`: Extracts raw text from PDF files.
    *   `TextProcessor`: Splits raw text into smaller, manageable chunks.
    *   `VectorStoreManager`: Creates text embeddings and builds a FAISS vector store for efficient retrieval.
    *   `ChatChainManager`: Initializes the LangChain `ConversationalRetrievalChain` with the LLM, vector store, and memory.
*   **`src/ui.py`**:
    *   `ChatbotUI`: Manages all Streamlit UI elements, handles user interactions (file uploads, chat input), and orchestrates calls to the core logic components. Manages session state for conversation and chat history.
*   **`src/main.py`**: The main entry point that instantiates `ChatbotUI` and runs the Streamlit application. Includes logic to modify `sys.path` for correct package resolution.
*   **`run_streamlit.py`**: A helper script in the project root to launch the Streamlit application, ensuring correct Python path setup for the `src` package.

## 9. Future Enhancements

*   **Support for other document types** (e.g., .txt, .docx).
*   **More sophisticated chunking strategies.**
*   **Option to choose different LLMs or embedding models via UI.**
*   **Display source chunks/pages for answers.**
*   **Ability to clear/reset conversation or uploaded documents.**
*   **Caching of processed documents/vector stores.**
*   **Improved error handling and logging.**
*   **User authentication and document persistence (for a multi-user setup).**
*   **Deployment to cloud platforms.**
*   **Unit and integration tests.**

## 10. License

This project is licensed under the MIT License. (Or specify your chosen license).

## 11. Contributing

Contributions are welcome! Please fork the repository, make your changes on a new branch, and submit a pull request. Ensure your code adheres to good coding practices and includes relevant documentation.