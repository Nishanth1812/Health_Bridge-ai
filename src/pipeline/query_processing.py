# preprocess query
"""
Query processing module for preprocessing and enhancing user queries.
"""
import logging
import re
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class QueryProcessor:
    """
    Handles preprocessing and enhancement of user queries before retrieval.
    """
    
    def __init__(self):
        """Initialize the query processor."""
        self.medical_terms_mapping = {
            # Mapping common terms to medical terminology
            "heart attack": ["myocardial infarction", "cardiac arrest"],
            "high blood pressure": ["hypertension"],
            "sugar": ["diabetes", "glucose"],
            "stroke": ["cerebrovascular accident", "CVA"],
            "heart burn": ["acid reflux", "GERD", "gastroesophageal reflux disease"],
            "shot": ["vaccine", "vaccination", "immunization"],
            "checkup": ["screening", "examination", "health assessment"],
            "pap smear": ["cervical screening", "cervical cancer screening"],
            "mammogram": ["breast cancer screening", "breast imaging"]
        }
        
        # Common preventive healthcare categories
        self.preventive_categories = [
            "screening", "immunization", "vaccination", "lifestyle", "nutrition",
            "exercise", "prevention", "check-up", "risk factor", "monitoring"
        ]
    
    def process_query(
        self, 
        query: str, 
        user_profile: Optional[Dict[str, Any]] = None,
        chat_history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Process a user query for better retrieval and response generation.
        
        Args:
            query: The raw user query
            user_profile: Optional user profile data for personalization
            chat_history: Optional chat history for context
            
        Returns:
            Dict containing processed query and additional metadata
        """
        # Clean and normalize query
        cleaned_query = self._clean_query(query)
        
        # Expand medical terms
        expanded_query = self._expand_medical_terms(cleaned_query)
        
        # Extract key information
        extracted_info = self._extract_key_information(cleaned_query)
        
        # Personalize based on profile if available
        personalized_context = self._personalize_query(cleaned_query, user_profile)
        
        # Categorize the query
        query_categories = self._categorize_query(cleaned_query)
        
        # Detect query intent
        intent = self._detect_intent(cleaned_query, chat_history)
        
        # Build result
        result = {
            "original_query": query,
            "processed_query": expanded_query,
            "extracted_info": extracted_info,
            "personalized_context": personalized_context,
            "categories": query_categories,
            "intent": intent
        }
        
        logger.debug(f"Processed query: {result}")
        return result
    
    def _clean_query(self, query: str) -> str:
        """
        Clean and normalize the query text.
        
        Args:
            query: Raw query text
            
        Returns:
            Cleaned query text
        """
        # Convert to lowercase
        text = query.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Remove special characters but keep alphanumeric, spaces, and basic punctuation
        text = re.sub(r'[^\w\s.,?!-]', '', text)
        
        return text
    
    def _expand_medical_terms(self, query: str) -> str:
        """
        Expand common terms to include medical terminology for better retrieval.
        
        Args:
            query: The cleaned query
            
        Returns:
            Expanded query with medical terminology
        """
        expanded = query
        
        # Check for each term in our mapping
        for common_term, medical_terms in self.medical_terms_mapping.items():
            if common_term in query:
                # Add medical terms to the query
                expanded += " " + " ".join(medical_terms)
        
        return expanded
    
    def _extract_key_information(self, query: str) -> Dict[str, Any]:
        """
        Extract key information from the query such as health conditions,
        demographics, or specific preventive measures mentioned.
        
        Args:
            query: The cleaned query
            
        Returns:
            Dict of extracted information
        """
        info = {
            "health_conditions": [],
            "demographics": {},
            "preventive_measures": []
        }
        
        # Extract age information
        age_match = re.search(r'\b(\d+)\s*(?:years|year|yr|y)(?:\s*old)?\b', query)
        if age_match:
            info["demographics"]["age"] = int(age_match.group(1))
        
        # Extract gender information
        if re.search(r'\b(?:i am|i\'m)\s+(?:a\s+)?(?:male|man|boy)\b', query):
            info["demographics"]["gender"] = "male"
        elif re.search(r'\b(?:i am|i\'m)\s+(?:a\s+)?(?:female|woman|girl)\b', query):
            info["demographics"]["gender"] = "female"
        
        # Extract preventive measures
        preventive_terms = [
            "vaccine", "screening", "test", "check-up", "checkup", 
            "mammogram", "colonoscopy", "pap smear", "blood pressure"
        ]
        
        for term in preventive_terms:
            if term in query:
                info["preventive_measures"].append(term)
        
        return info
    
    def _personalize_query(
        self, 
        query: str, 
        user_profile: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Add personalization context to the query based on user profile.
        
        Args:
            query: The cleaned query
            user_profile: User profile data
            
        Returns:
            Personalization context string
        """
        if not user_profile:
            return ""
            
        context_parts = []
        
        # Add age and gender if available
        if "age" in user_profile and "gender" in user_profile:
            context_parts.append(f"{user_profile['age']} year old {user_profile['gender']}")
        
        # Add relevant medical conditions
        if "medical_conditions" in user_profile and user_profile["medical_conditions"]:
            conditions = ", ".join(user_profile["medical_conditions"])
            context_parts.append(f"with history of {conditions}")
        
        # Add risk factors
        if "risk_factors" in user_profile and user_profile["risk_factors"]:
            risk_factors = ", ".join(user_profile["risk_factors"])
            context_parts.append(f"with risk factors: {risk_factors}")
        
        return " ".join(context_parts)
    
    def _categorize_query(self, query: str) -> List[str]:
        """
        Categorize the query into preventive healthcare categories.
        
        Args:
            query: The cleaned query
            
        Returns:
            List of applicable categories
        """
        categories = []
        
        for category in self.preventive_categories:
            if category in query:
                categories.append(category)
        
        # Specific category detection based on content
        if re.search(r'\b(?:vaccine|vaccination|immunization|shot|booster)\b', query):
            categories.append("immunization")
            
        if re.search(r'\b(?:screening|check|test|exam|mammogram|colonoscopy|pap)\b', query):
            categories.append("screening")
            
        if re.search(r'\b(?:exercise|workout|fitness|physical activity)\b', query):
            categories.append("exercise")
            
        if re.search(r'\b(?:diet|nutrition|food|eating|meal)\b', query):
            categories.append("nutrition")
            
        return list(set(categories))  # Remove duplicates
    
    def _detect_intent(
        self, 
        query: str, 
        chat_history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """
        Detect the intent of the user query.
        
        Args:
            query: The cleaned query
            chat_history: Optional chat history for context
            
        Returns:
            Detected intent string
        """
        # Check for question patterns
        if re.search(r'^(?:what|how|when|where|why|who|can|should|is|are|do|does|did|will)\b', query) or '?' in query:
            return "question"
            
        # Check for information seeking
        if re.search(r'\b(?:tell|explain|describe|information|know|learn|understand)\b', query):
            return "information"
            
        # Check for scheduling or recommendation requests
        if re.search(r'\b(?:schedule|appointment|recommend|suggest|advice|advise|should I)\b', query):
            return "recommendation"
            
        # Check for symptom checking
        if re.search(r'\b(?:symptom|feel|feeling|pain|ache|hurt|suffering)\b', query):
            return "symptom_check"
            
        # Default intent
        return "general"

def preprocess_query(
    query: str,
    user_profile: Optional[Dict[str, Any]] = None,
    chat_history: Optional[List[Dict[str, str]]] = None
) -> Dict[str, Any]:
    """
    Wrapper function to preprocess a user query.
    
    Args:
        query: The user query
        user_profile: Optional user profile data
        chat_history: Optional chat history
        
    Returns:
        Processed query result
    """
    try:
        processor = QueryProcessor()
        return processor.process_query(query, user_profile, chat_history)
    except Exception as e:
        logger.error(f"Error preprocessing query: {str(e)}")
        # Return minimal processed result on error
        return {
            "original_query": query,
            "processed_query": query,
            "extracted_info": {},
            "personalized_context": "",
            "categories": [],
            "intent": "general"
        }