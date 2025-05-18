import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path='C:\projects\ChatPdf\.env')

# API Keys and Endpoints (fetched from environment variables)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# LLM Configuration
LLM_MODEL_NAME = "qwen/qwen3-30b-a3b:free" 
LLM_TEMPERATURE = 0.1

# Embedding Model Configuration
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# Text Splitter Configuration
TEXT_CHUNK_SIZE = 1000
TEXT_CHUNK_OVERLAP = 200



# Streamlit Page Configuration
PAGE_TITLE = "Chat with multiple PDFs"
PAGE_ICON = ":books:"

# Error messages
ERROR_MISSING_API_KEY = "OpenRouter API key not found. Please set it in your .env file."
ERROR_PROCESSING_PDF = "An error occurred while processing the PDFs."
ERROR_NO_PDF_PROCESSED = "Please upload and process PDF documents first."