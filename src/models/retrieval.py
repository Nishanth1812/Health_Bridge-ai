


import os
import logging
import numpy as np
import faiss
from typing import List, Dict, Any, Optional
import json

from src.models.embedding import EmbeddingModel

logger = logging.getLogger(__name__)

class DocumentRetriever:
    """Handles retrieval of relevant documents for a given query."""
    
    def __init__(
        self, 
        embedding_model: EmbeddingModel,
        index_path: str = "data/embeddings/faiss_index.index",
        id_map_path: str = "data/embeddings/id_map.json",
        content_path: str = "data/processed/document_content.json"
    ):
        """
        Initialize the document retriever.
        
        Args:
            embedding_model: Model for embedding queries
            index_path: Path to the FAISS index file
            id_map_path: Path to the document ID mapping file
            content_path: Path to the document content file
        """
        self.embedding_model = embedding_model
        
        # Load the FAISS index
        try:
            if os.path.exists(index_path):
                self.index = faiss.read_index(index_path)
                logger.info(f"Loaded FAISS index from {index_path}")
            else:
                logger.warning(f"Index file not found at {index_path}. Will initialize empty index.")
                self.index = None
        except Exception as e:
            logger.error(f"Error loading FAISS index: {str(e)}")
            self.index = None
        
        # Load the document ID mapping
        try:
            if os.path.exists(id_map_path):
                with open(id_map_path, 'r') as f:
                    self.id_map = json.load(f)
                logger.info(f"Loaded {len(self.id_map)} document IDs from {id_map_path}")
            else:
                logger.warning(f"ID map file not found at {id_map_path}. Will initialize empty map.")
                self.id_map = []
        except Exception as e:
            logger.error(f"Error loading ID map: {str(e)}")
            self.id_map = []
        
        # Load the document content
        try:
            if os.path.exists(content_path):
                with open(content_path, 'r') as f:
                    self.document_content = json.load(f)
                logger.info(f"Loaded content for {len(self.document_content)} documents from {content_path}")
            else:
                logger.warning(f"Document content file not found at {content_path}. Will initialize empty content.")
                self.document_content = {}
        except Exception as e:
            logger.error(f"Error loading document content: {str(e)}")
            self.document_content = {}
    
    def retrieve_documents(
        self, 
        query: str, 
        top_k: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Retrieve the most relevant documents for a query.
        
        Args:
            query: The user query
            top_k: Number of top documents to retrieve
            
        Returns:
            List of retrieved documents with their content and metadata
        """
        if not self.index or not self.id_map:
            logger.warning("No index or ID map available for retrieval")
            return []
        
        try:
            # Embed the query
            query_embedding = self.embedding_model.embed_text(query)
            
            # Reshape for FAISS
            query_embedding_reshaped = np.reshape(query_embedding, (1, -1)).astype('float32')
            
            # Search the index
            distances, indices = self.index.search(query_embedding_reshaped, min(top_k, len(self.id_map)))
            
            # Get the documents
            retrieved_docs = []
            for i, idx in enumerate(indices[0]):
                if idx < 0 or idx >= len(self.id_map):  # FAISS can return -1 if fewer than top_k items are found
                    continue
                    
                doc_id = self.id_map[idx]
                if doc_id in self.document_content:
                    retrieved_docs.append({
                        "id": doc_id,
                        "content": self.document_content[doc_id].get("content", ""),
                        "metadata": {
                            "source": self.document_content[doc_id].get("source", ""),
                            "score": float(distances[0][i]),
                            "date": self.document_content[doc_id].get("date", "")
                        }
                    })
            
            logger.info(f"Retrieved {len(retrieved_docs)} documents for query: {query[:50]}...")
            return retrieved_docs
            
        except Exception as e:
            logger.error(f"Error retrieving documents: {str(e)}")
            return []

def retrieve_documents(
    query: str, 
    top_k: int = 3,
    retriever: Optional[DocumentRetriever] = None
) -> List[Dict[str, Any]]:
    """
    Wrapper function to retrieve documents for a query.
    
    Args:
        query: The user query
        top_k: Number of top documents to retrieve
        retriever: Optional pre-initialized retriever (for efficiency in repeated calls)
        
    Returns:
        List of retrieved documents
    """
    try:
        if not retriever:
            # Initialize embedding model and retriever
            from backend.models.embedding import EmbeddingModel
            embedding_model = EmbeddingModel()
            retriever = DocumentRetriever(embedding_model)
        
        return retriever.retrieve_documents(query, top_k)
    except Exception as e:
        logger.error(f"Error in retrieve_documents: {str(e)}")
        return []