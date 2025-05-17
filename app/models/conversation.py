from datetime import datetime
from uuid import uuid4
from typing import List, Dict

class Conversation:
    def __init__(self, conv_id: str = None):
        self.id = conv_id or str(uuid4())
        self.messages: List[Dict] = []
        self.created_at = datetime.now()
        self.last_modified = datetime.now()
    
    def add_message(self, role: str, content: str):
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        self.last_modified = datetime.now()
    
    @property
    def context(self):
        return [{"role": msg["role"], "content": msg["content"]} 
                for msg in self.messages[-10:]]  # Last 10 messages as context

class ConversationManager:
    def __init__(self):
        self.conversations: Dict[str, Conversation] = {}
    
    def get_conversation(self, request) -> Conversation:
        session_id = request.cookies.get("session_id") or str(uuid4())
        if session_id not in self.conversations:
            self.conversations[session_id] = Conversation()
        return self.conversations[session_id]