
"""
Response generation module for the Preventive Healthcare Chatbot.
"""
import os
import logging
import json
from typing import List, Dict, Any, Optional
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

logger = logging.getLogger(__name__)

class ResponseGenerator:
    """Generates responses using a language model based on retrieved documents."""
    
    def __init__(
        self,
        model_name: str = "google/flan-t5-large",  # Using a smaller model for demonstration
        max_new_tokens: int = 512,
        temperature: float = 0.7,
        model_device: str = "cpu"  # Switch to "cuda" if GPU is available
    ):
        """
        Initialize the response generator.
        
        Args:
            model_name: HuggingFace model identifier
            max_new_tokens: Maximum number of tokens to generate
            temperature: Sampling temperature (higher = more random)
            model_device: Device to run the model on ("cpu" or "cuda")
        """
        logger.info(f"Initializing response generator with model: {model_name}")
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForCausalLM.from_pretrained(model_name)
            
            # Move model to appropriate device
            self.device = model_device if torch.cuda.is_available() and model_device == "cuda" else "cpu"
            self.model.to(self.device)
            
            self.max_new_tokens = max_new_tokens
            self.temperature = temperature
            
            logger.info(f"Response generator initialized on {self.device}")
        except Exception as e:
            logger.error(f"Error initializing response generator: {str(e)}")
            raise
    
    def generate(
        self,
        query: str,
        retrieved_documents: List[Dict[str, Any]],
        chat_history: Optional[List[Dict[str, str]]] = None,
        user_profile: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Generate a response based on the query and retrieved documents.
        
        Args:
            query: The user query
            retrieved_documents: List of retrieved documents
            chat_history: Optional list of previous chat messages
            user_profile: Optional user profile information
            
        Returns:
            str: The generated response
        """
        try:
            # Prepare context from retrieved documents
            context = self._prepare_context(retrieved_documents)
            
            # Format the prompt with query and context
            prompt = self._format_prompt(query, context, chat_history, user_profile)
            
            # Generate response using the model
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
            
            with torch.no_grad():
                generated_ids = self.model.generate(
                    inputs.input_ids,
                    max_new_tokens=self.max_new_tokens,
                    temperature=self.temperature,
                    top_p=0.95,
                    do_sample=True
                )
                
            response = self.tokenizer.decode(generated_ids[0], skip_special_tokens=True)
            
            # Extract just the generated response (not the prompt)
            response = response[len(prompt):].strip()
            
            # Add disclaimer if not already present
            if "not a substitute for professional medical advice" not in response.lower():
                response += "\n\nNote: This information is not a substitute for professional medical advice. Always consult with your healthcare provider."
            
            logger.info(f"Generated response for query: {query[:50]}...")
            return response
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return "I apologize, but I'm having trouble generating a response at the moment. Please try again later."
    
    def _prepare_context(self, retrieved_documents: List[Dict[str, Any]]) -> str:
        """
        Prepare context from retrieved documents.
        
        Args:
            retrieved_documents: List of retrieved documents
            
        Returns:
            str: Formatted context string
        """
        if not retrieved_documents:
            return "No relevant documents found."
            
        context_parts = []
        for i, doc in enumerate(retrieved_documents):
            context_parts.append(f"Document {i+1} (Source: {doc['metadata'].get('source', 'Unknown')}): {doc['content']}")
            
        return "\n\n".join(context_parts)
    
    def _format_prompt(
        self,
        query: str,
        context: str,
        chat_history: Optional[List[Dict[str, str]]] = None,
        user_profile: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Format the complete prompt for the language model.
        
        Args:
            query: The user query
            context: Context from retrieved documents
            chat_history: Optional list of previous chat messages
            user_profile: Optional user profile information
            
        Returns:
            str: The formatted prompt
        """
        # Format chat history if provided
        history_text = ""
        if chat_history:
            for message in chat_history[-3:]:  # Include only the last 3 messages for context
                role = message.get("role", "")
                content = message.get("content", "")
                history_text += f"{role.capitalize()}: {content}\n"
        
        # Include relevant user profile info if available
        profile_text = ""
        if user_profile:
            age = user_profile.get("age", "")
            gender = user_profile.get("gender", "")
            conditions = user_profile.get("medical_conditions", [])
            
            if age or gender:
                profile_text = f"User Profile: {age} {gender}".strip()
                
            if conditions:
                profile_text += f", Has conditions: {', '.join(conditions)}"
        
        # Format the complete prompt
        system_prompt = """You are a helpful, accurate, and informative healthcare assistant focused on preventive healthcare. 
Your goal is to provide evidence-based information from reliable medical sources. 
Answer questions clearly and concisely, and always emphasize the importance of consulting healthcare professionals for personalized advice.
Base your responses on the provided context documents when available."""

        prompt = f"{system_prompt}\n\n"
        
        if profile_text:
            prompt += f"{profile_text}\n\n"
            
        if history_text:
            prompt += f"Previous conversation:\n{history_text}\n"
            
        prompt += f"Context information:\n{context}\n\n"
        prompt += f"User Query: {query}\n\n"
        prompt += "Assistant Response:"
        
        return prompt

def generate_response(
    user_message: str,
    retrieved_documents: List[Dict[str, Any]],
    chat_history: Optional[List[Dict[str, str]]] = None,
    user_profile: Optional[Dict[str, Any]] = None,
    generator: Optional[ResponseGenerator] = None
) -> str:
    """
    Wrapper function to generate a response for a user message.
    
    Args:
        user_message: The user's message
        retrieved_documents: List of retrieved documents
        chat_history: Optional list of previous chat messages
        user_profile: Optional user profile information
        generator: Optional pre-initialized generator (for efficiency in repeated calls)
        
    Returns:
        str: The generated response
    """
    try:
        if not generator:
            generator = ResponseGenerator()
            
        return generator.generate(
            query=user_message,
            retrieved_documents=retrieved_documents,
            chat_history=chat_history,
            user_profile=user_profile
        )
    except Exception as e:
        logger.error(f"Error in generate_response: {str(e)}")
        return "I apologize, but I'm having trouble generating a response at the moment. Please try again later."