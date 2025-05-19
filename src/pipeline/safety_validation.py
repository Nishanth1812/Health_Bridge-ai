# safety validation
"""
Input and output validation functions for ensuring safe and reliable responses.
"""
import logging
import re
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

# Sample harmful content patterns (simplified for demonstration)
HARMFUL_PATTERNS = [
    r'\b(hack|exploit|bypass|steal)\b',
    r'\b(illegal|unlawful)\b.*\b(drugs?|substances?)\b',
    r'\b(suicide|self-harm)\b',
    r'\b(instructions|how to).*\b(weapons?|bombs?|explosives?)\b',
    r'\b(child|minor).*\b(explicit|pornography|sexual)\b'
]

# Medical disclaimer patterns to check in output
MEDICAL_DISCLAIMERS = [
    r'not (a|an).*substitute for.*medical.*advice',
    r'consult.*healthcare.*provider',
    r'for educational purposes'
]

def validate_input(text: str) -> Dict[str, Any]:
    """
    Validate user input for harmful content.
    
    Args:
        text (str): User input text
        
    Returns:
        Dict: Validation result with keys 'valid' and optionally 'reason'
    """
    if not text or not text.strip():
        return {"valid": False, "reason": "Empty input"}
        
    # Check for harmful patterns
    for pattern in HARMFUL_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            logger.warning(f"Harmful content detected in input: {text[:50]}...")
            return {
                "valid": False,
                "reason": "Input contains potentially harmful content"
            }
    
    return {"valid": True}

def validate_output(text: str) -> Dict[str, Any]:
    """
    Validate output for appropriate healthcare content.
    
    Args:
        text (str): Generated response text
        
    Returns:
        Dict: Validation result with keys 'valid' and optionally 'reason'
    """
    if not text or not text.strip():
        return {"valid": False, "reason": "Empty output"}
    
    # Check for appropriate medical disclaimer
    has_disclaimer = False
    for pattern in MEDICAL_DISCLAIMERS:
        if re.search(pattern, text, re.IGNORECASE):
            has_disclaimer = True
            break
    
    if not has_disclaimer and len(text) > 200:  # Only require disclaimers for substantive responses
        logger.warning("Response missing appropriate medical disclaimer")
        return {
            "valid": False,
            "reason": "Response missing appropriate medical disclaimer"
        }
    
    # Check for harmful content patterns
    for pattern in HARMFUL_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            logger.warning(f"Harmful content detected in output: {text[:50]}...")
            return {
                "valid": False,
                "reason": "Output contains potentially harmful content"
            }
    
    return {"valid": True}