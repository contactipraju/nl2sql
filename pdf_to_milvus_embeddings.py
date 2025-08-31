import os
from PyPDF2 import PdfReader
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection
from pymilvus.model.dense import GeminiEmbeddingFunction

from utils.config import GEMINI_API_KEY

# CONFIGURABLE: Set your API key and collection parameters.
MILVUS_HOST = 'localhost'
MILVUS_PORT = '19530'
COLLECTION_NAME = 'pdf_embeddings'
MODEL_NAME = 'models/embedding-001'  # or latest Gemini embedding model
pdf_path = "input-files/employee_schema.pdf"  # Path to your PDF file

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def split_text(text, max_length=500):
    # Simple split on length; more advanced splitting can be used if desired
    chunks = [text[i:i + max_length] for i in range(0, len(text), max_length)]
    return [chunk.strip() for chunk in chunks if chunk.strip()]

def create_collection(dim):
    fields = [
        FieldSchema(name="pk", dtype=DataType.VARCHAR, is_primary=True, auto_id=False, max_length=100),
        FieldSchema(name="source", dtype=DataType.VARCHAR, max_length=5000),
        FieldSchema(name="embeddings", dtype=DataType.FLOAT_VECTOR, dim=dim),
    ]
    schema = CollectionSchema(fields, "PDF Text Embeddings")
    collection = Collection(COLLECTION_NAME, schema, consistency_level="Strong")
    return collection

if __name__ == '__main__':
    # 1. Extract PDF text and chunk
    all_text = extract_text_from_pdf(pdf_path)
    text_chunks = split_text(all_text)

    # 2. Connect to Milvus
    connections.connect(host=MILVUS_HOST, port=MILVUS_PORT)

    # 3. Create or load GEMINI embedding function
    embedding_func = GeminiEmbeddingFunction(
        model_name=MODEL_NAME, api_key=GEMINI_API_KEY
    )

    # 4. Generate embeddings for each chunk
    embeddings = embedding_func.encode_documents(text_chunks)
    emb_dim = len(embeddings)

    # 5. Create the collection (if it doesn't exist)
    try:
        collection = Collection(COLLECTION_NAME)
    except:
        collection = create_collection(emb_dim)

    # 6. Insert data
    pks = [f"chunk_{i}" for i in range(len(text_chunks))]
    source_col = text_chunks
    entities = [pks, source_col, embeddings]
    collection.insert(entities)
    collection.flush()

    print(f"Inserted {len(embeddings)} embeddings into Milvus collection '{COLLECTION_NAME}'.")
