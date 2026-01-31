
import sys
import os

# Add packages to path so we can import factory_core
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'packages'))

from factory_core.agent import BaseAgent

class CEOAgent(BaseAgent):
    def __init__(self):
        super().__init__("CEO", "Chief Executive Officer")

    def ceo_vision(self, payload):
        """
        Gathers business vision from the founder.
        """
        idea = payload.get("idea")
        user_id = payload.get("user_id")
        
        self.logger.info(f"Processing vision for user {user_id}: {idea}")
        
        # In a real implementation, this would call the LLM to analyze the idea
        # and generate clarifying questions.
        
        return {
            "message": "I have received your vision. It is ambitious.",
            "next_step": "clarifying_questions",
            "questions": [
                "Who is your target audience?",
                "What is your revenue model?"
            ]
        }

# Cloud Function Entry Point
def entry_point(request):
    """HTTP Cloud Function."""
    request_json = request.get_json(silent=True)
    
    if not request_json:
        return {"error": "JSON body required"}, 400
        
    command = request_json.get("command")
    payload = request_json.get("payload", {})
    
    if not command:
        return {"error": "Command required"}, 400

    agent = CEOAgent()
    result = agent.run(command, payload)
    
    return result
