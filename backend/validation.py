from jsonschema import validate
import json

SCHEMAS = {
    "competitive_analysis": {
        "type": "object",
        "properties": {
            "overview": {"type": "string"},
            "competitors": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "market_share": {"type": "string"},
                        "strengths": {"type": "array", "items": {"type": "string"}},
                        "weaknesses": {"type": "array", "items": {"type": "string"}}
                    }
                }
            }
        }
    }
}

class ResponseValidator:
    @staticmethod
    def validate_response(response: str, query_type: str) -> dict:
        try:
            # Clean Gemini response
            cleaned = response.replace('```json', '').replace('```', '')
            data = json.loads(cleaned)
            
            # Schema validation
            validate(instance=data, schema=SCHEMAS[query_type])
            return data
        except Exception as e:
            raise ValueError(f"Validation failed: {str(e)}")