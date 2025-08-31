# NL2SQL & Vector Database Demo

NL2SQL is an AI-powered project for natural language to SQL conversion and semantic search using vector databases (Milvus) and Google Gemini models. It includes PDF ingestion, embedding generation, and a Streamlit chatbot interface.

## Features

- **PDF Ingestion**: Extracts text from PDF files and splits into manageable chunks.
- **Embeddings**: Generates vector embeddings using Gemini embedding models.
- **Vector Database**: Stores and searches embeddings in Milvus.
- **Chatbot**: Streamlit-based chatbot using Gemini for conversational AI.
- **Environment Management**: Loads API keys and config from `.env` files.

## Project Structure

```
nl2sql.py                # Main script for PDF to Milvus workflow
chatbot.py               # Streamlit chatbot using Gemini
requirements.txt         # Python dependencies
docker/                  # Docker Compose files for Milvus and dependencies
input-files/             # Example PDF files
utils/                   # Utility scripts (config, model listing, Milvus tests)
nl2sqlenv/               # Python virtual environment
volumes/                 # Milvus and etcd data volumes
README.md                # Project documentation
```

## Setup

1. **Install dependencies**:
	```bash
	pip install -r requirements.txt
	```

2. **Set up environment variables**:
	- Create a `.env` file with your Gemini API key:
	  ```
	  GEMINI_API_KEY=your_gemini_api_key
	  ```

3. **Start Milvus (optional, if using Docker)**:
	```bash
	docker-compose -f docker/docker-compose.yml up -d
	```

## Usage

### PDF to Embeddings

Run the main script to extract text from a PDF, generate embeddings, and store them in Milvus:
```bash
python nl2sql.py
```

### Chatbot

Start the Streamlit chatbot:
```bash
streamlit run chatbot.py
```

## Example

- Place your PDF files in `input-files/`.
- Configure your API key in `.env`.
- Run the scripts as shown above.

## Technologies

- Python
- Milvus (Vector Database)
- Google Gemini (Generative AI & Embeddings)
- Streamlit (Web UI)
- PyPDF2 (PDF parsing)
- LangChain (for advanced workflows)

## License

MIT License

## Author

Contact: contactipraju
