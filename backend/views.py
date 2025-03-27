from flask import Blueprint, request, jsonify
from .gemini_client import GeminiClient
from .prompt_engineer import PromptBuilder
from .validation import ResponseValidator
from flask_limiter import Limiter

bp = Blueprint('main', __name__)
# limiter = Limiter(key_func=get_remote_address)

client = GeminiClient()

@bp.route('/analyze', methods=['POST'])
# @limiter.limit("10/minute")
def analyze():
    # Input validation
    data = request.get_json()
    required_fields = {
        'competitive_analysis': ['industry', 'company'],
        'trend_forecasting': ['industry', 'timeframe']
    }
    
    query_type = data.get('type')
    params = data.get('params', {})
    
    # Validate request
    if not query_type or query_type not in required_fields:
        return jsonify({"error": "Invalid query type"}), 400
        
    missing = [field for field in required_fields[query_type] if not params.get(field)]
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400

    try:
        # Build and execute prompt
        prompt = PromptBuilder.build_prompt(query_type, params)
        gemini_response = client.generate_insights(prompt)
        
        if gemini_response["error"]:
            raise RuntimeError(gemini_response["error"])
            
        # Validate and process response
        structured_data = ResponseValidator.validate_response(
            gemini_response["content"], 
            query_type
        )
        
        return jsonify({
            "data": structured_data,
            "metadata": {
                "latency": gemini_response["latency"],
                "prompt_version": "1.0"
            }
        })
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "type": "API_ERROR"
        }), 500