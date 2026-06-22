"""Shared configuration for Lab 18."""

import os
from dotenv import load_dotenv

load_dotenv()

# --- API Keys ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# --- Qdrant ---
QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
COLLECTION_NAME = "lab18_production"
NAIVE_COLLECTION = "lab18_naive"

# --- Embedding ---
_LOCAL_EMBEDDING_MODEL = os.path.abspath(os.path.join(os.path.dirname(__file__), "models", "bge-m3"))
_EMBEDDING_WEIGHTS = os.path.join(_LOCAL_EMBEDDING_MODEL, "pytorch_model.bin")
if os.path.exists(_EMBEDDING_WEIGHTS):
    EMBEDDING_MODEL = _LOCAL_EMBEDDING_MODEL
else:
    EMBEDDING_MODEL = "BAAI/bge-m3"
EMBEDDING_DIM = 1024

# --- Reranking ---
_LOCAL_RERANKER_MODEL = os.path.abspath(os.path.join(os.path.dirname(__file__), "models", "bge-reranker-v2-m3"))
_RERANKER_WEIGHTS = os.path.join(_LOCAL_RERANKER_MODEL, "model.safetensors")
if os.path.exists(_RERANKER_WEIGHTS):
    RERANKER_MODEL = _LOCAL_RERANKER_MODEL
else:
    RERANKER_MODEL = "BAAI/bge-reranker-v2-m3"

# --- Chunking ---
HIERARCHICAL_PARENT_SIZE = 2048
HIERARCHICAL_CHILD_SIZE = 256
SEMANTIC_THRESHOLD = 0.85

# --- Search ---
BM25_TOP_K = 20
DENSE_TOP_K = 20
HYBRID_TOP_K = 20
RERANK_TOP_K = 3

# --- Paths ---
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
TEST_SET_PATH = os.path.join(os.path.dirname(__file__), "test_set.json")
