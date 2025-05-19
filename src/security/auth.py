# auth utilities
"""
Authentication and API security functions.
"""
import logging
import os
import time
from typing import Dict, Optional

logger = logging.getLogger(__name__)

# In production, this would be stored securely in a database
# For demonstration, we'll use a simple dictionary
VALID_API_KEYS = {
    "demo-api-key-123456": {
        "user_id": "demo_user",
        "role": "user",
        "expires_at": int(time.time()) + 86400 * 30  # 30 days from now
    }
}

def validate_api_key(api_key: Optional[str]) -> bool:
    """
    Validate an API key.
    
    Args:
        api_key (str): API key to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not api_key:
        logger.warning("Missing API key")
        return False
    
    # Check if key exists and is not expired
    if api_key in VALID_API_KEYS:
        key_info = VALID_API_KEYS[api_key]
        current_time = int(time.time())
        
        if key_info["expires_at"] > current_time:
            return True
        else:
            logger.warning(f"Expired API key used: {api_key[:5]}...")
            return False
    else:
        # For demo purposes, accept the DEFAULT_API_KEY from environment
        default_key = os.getenv("DEFAULT_API_KEY")
        if default_key and api_key == default_key:
            return True
            
        logger.warning(f"Invalid API key used: {api_key[:5]}...")
        return False

def get_user_from_api_key(api_key: str) -> Optional[str]:
    """
    Get user ID associated with an API key.
    
    Args:
        api_key (str): API key
        
    Returns:
        str or None: User ID if valid key, None otherwise
    """
    if api_key in VALID_API_KEYS:
        return VALID_API_KEYS[api_key]["user_id"]
    return None

def create_token(user_id: str, role: str = "user", ttl_seconds: int = 3600) -> Dict[str, any]:
    """
    Create a new API token.
    
    Args:
        user_id (str): User ID
        role (str): User role
        ttl_seconds (int): Time to live in seconds
        
    Returns:
        Dict: Token information
    """
    import uuid
    
    # Generate a unique token
    token = f"api-key-{uuid.uuid4()}"
    expires_at = int(time.time()) + ttl_seconds
    
    # Store the token
    VALID_API_KEYS[token] = {
        "user_id": user_id,
        "role": role,
        "expires_at": expires_at
    }
    
    return {
        "token": token,
        "expires_at": expires_at
    }