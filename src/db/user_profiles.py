# user profile models
"""
User profile management module.
"""
import logging
from typing import Dict, Optional, Any

logger = logging.getLogger(__name__)

# Demo user profiles (in production, this would be in a database)
DEMO_PROFILES = {
    "demo_user": {
        "age": 42,
        "gender": "female",
        "health_conditions": ["hypertension"],
        "allergies": ["penicillin"],
        "family_history": ["diabetes", "heart disease"],
        "preferences": {
            "notification_frequency": "weekly",
            "topics_of_interest": ["nutrition", "fitness", "preventive screenings"]
        },
        "last_checkup": "2025-02-15"
    },
    "anonymous": {
        "preferences": {
            "topics_of_interest": ["general health"]
        }
    }
}

def get_user_profile(user_id: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user profile by ID.
    
    Args:
        user_id (str): User ID
        
    Returns:
        Dict or None: User profile if found, None otherwise
    """
    try:
        # In production, this would query a database
        if user_id in DEMO_PROFILES:
            logger.info(f"Retrieved profile for user: {user_id}")
            return DEMO_PROFILES[user_id]
        
        logger.info(f"No profile found for user: {user_id}")
        return None
        
    except Exception as e:
        logger.error(f"Error retrieving user profile: {str(e)}")
        return None

def update_user_profile(user_id: str, profile_data: Dict[str, Any]) -> bool:
    """
    Update a user profile.
    
    Args:
        user_id (str): User ID
        profile_data (Dict): Profile data to update
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # In production, this would update a database record
        if user_id in DEMO_PROFILES:
            # Update existing profile
            for key, value in profile_data.items():
                if key in DEMO_PROFILES[user_id] and isinstance(DEMO_PROFILES[user_id][key], dict) and isinstance(value, dict):
                    # Merge dictionaries for nested properties
                    DEMO_PROFILES[user_id][key].update(value)
                else:
                    # Replace or add non-nested properties
                    DEMO_PROFILES[user_id][key] = value
        else:
            # Create new profile
            DEMO_PROFILES[user_id] = profile_data
            
        logger.info(f"Updated profile for user: {user_id}")
        return True
        
    except Exception as e:
        logger.error(f"Error updating user profile: {str(e)}")
        return False