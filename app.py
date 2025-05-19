"""
Main Flask application for the Preventive Healthcare Chatbot API.
"""
import os
import json
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from src.core.config import load_config
from src.models.retrieval import retrieve_documents
from src.models.generation import generate_response
from src.pipeline.safety_validation import validate_input, validate_output
from src.security.auth import validate_api_key
from src.db.user_profiles import get_user_profile
from src.monitoring.logging import setup_logging

# Load environment variables and configurations
load_dotenv()
app_config = load_config('config/app_config.yaml')
setup_logging()
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains on all routes

@app.route('/api/health', methods=['GET'])
def health_check():
    """Simple health check endpoint."""
    return jsonify({
        "status": "ok",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    """Main chat endpoint that processes user queries and returns AI responses."""
    try:
        # Check authentication
        api_key = request.headers.get('')
        if not validate_api_key(api_key):
            return jsonify({"error": "Invalid or missing API key"}), 401
        
        # Parse request
        data = request.json
        if not data or 'message' not in data:
            return jsonify({"error": "Message is required"}), 400
            
        user_message = data['message']
        user_id = data.get('user_id', 'anonymous')
        chat_history = data.get('chat_history', [])
        
        # Validate input for safety
        input_validation = validate_input(user_message)
        if not input_validation['valid']:
            return jsonify({
                "error": "Input validation failed",
                "reason": input_validation['reason']
            }), 400
        
        # Get user profile for personalized responses (if available)
        user_profile = get_user_profile(user_id) if user_id != 'anonymous' else None
        
        # Process the query through the pipeline
        # 1. Retrieve relevant documents
        retrieved_docs = retrieve_documents(user_message, top_k=3)
        
        # 2. Generate response
        response = generate_response(
            user_message=user_message,
            retrieved_documents=retrieved_docs,
            chat_history=chat_history,
            user_profile=user_profile
        )
        
        # 3. Validate output for safety
        output_validation = validate_output(response)
        if not output_validation['valid']:
            logger.warning(f"Output validation failed: {output_validation['reason']}")
            return jsonify({
                "error": "Output validation failed",
                "reason": output_validation['reason']
            }), 400
        
        # Log the interaction
        logger.info(f"Chat interaction - User: {user_id}, Message: {user_message[:50]}...")
        
        return jsonify({
            "response": response,
            "sources": [doc["metadata"] for doc in retrieved_docs]
        })
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    """Endpoint to collect user feedback on AI responses."""
    try:
        # Validate authentication
        api_key = request.headers.get('X-API-Key')
        if not validate_api_key(api_key):
            return jsonify({"error": "Invalid or missing API key"}), 401
        
        data = request.json
        if not data:
            return jsonify({"error": "No feedback data provided"}), 400
            
        # Log the feedback for analysis
        logger.info(f"Feedback received: {json.dumps(data)}")
        
        # Here you would typically store the feedback in a database
        # For now, we'll just acknowledge receipt
        
        return jsonify({
            "status": "success",
            "message": "Feedback received"
        })
        
    except Exception as e:
        logger.error(f"Error in feedback endpoint: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/auth/token', methods=['POST'])
def get_token():
    """Simple authentication endpoint to get an API token."""
    try:
        data = request.json
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({"error": "Username and password required"}), 400
            
        # Very basic auth for demonstration
        # In production, use a proper authentication system
        if data['username'] == 'demo' and data['password'] == 'healthbot2025':
            return jsonify({
                "token": "demo-api-key-123456",
                "expires_at": (datetime.now().timestamp() + 3600) * 1000  # 1 hour from now, in milliseconds
            })
        else:
            return jsonify({"error": "Invalid credentials"}), 401
            
    except Exception as e:
        logger.error(f"Error in token endpoint: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500
@app.route('/')
def index():
    return "Preventive Healthcare Chatbot API is running!"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)