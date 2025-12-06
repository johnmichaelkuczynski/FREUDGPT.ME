"""
Conversation Manager for tracking Q&A history and enabling contradiction detection.
"""

from datetime import datetime
from typing import List, Dict, Optional
import uuid

class ConversationManager:
    """Manages conversation history for self-contradiction detection."""
    
    def __init__(self, max_history: int = 20):
        """
        Initialize conversation manager.
        
        Args:
            max_history: Maximum number of Q&A pairs to retain per conversation
        """
        self.conversations = {}  # conversation_id -> list of exchanges
        self.max_history = max_history
    
    def get_conversation_id(self) -> str:
        """Generate a new conversation ID."""
        return str(uuid.uuid4())
    
    def add_exchange(self, conversation_id: str, question: str, answer: str, database: str):
        """
        Add a Q&A exchange to the conversation history.
        
        Args:
            conversation_id: Unique conversation identifier
            question: User's question
            answer: AI's response
            database: Which database was used (Freud, Kuczynski, etc.)
        """
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = []
        
        exchange = {
            'question': question,
            'answer': answer,
            'database': database,
            'timestamp': datetime.now().isoformat()
        }
        
        self.conversations[conversation_id].append(exchange)
        
        # Prune old exchanges if history exceeds max
        if len(self.conversations[conversation_id]) > self.max_history:
            self.conversations[conversation_id] = self.conversations[conversation_id][-self.max_history:]
    
    def get_history(self, conversation_id: str) -> List[Dict]:
        """
        Get conversation history for a given conversation ID.
        
        Args:
            conversation_id: Unique conversation identifier
            
        Returns:
            List of exchange dictionaries
        """
        return self.conversations.get(conversation_id, [])
    
    def format_history_for_prompt(self, conversation_id: str, max_recent: int = 10, current_database: Optional[str] = None) -> str:
        """
        Format conversation history for inclusion in AI prompt.
        
        Args:
            conversation_id: Unique conversation identifier
            max_recent: Maximum number of recent exchanges to include
            current_database: If provided, only include exchanges from this database
            
        Returns:
            Formatted string of previous Q&A exchanges
        """
        history = self.get_history(conversation_id)
        
        if not history:
            return ""
        
        # Filter by current database if specified (prevents cross-contamination)
        if current_database:
            history = [ex for ex in history if ex.get('database') == current_database]
        
        if not history:
            return ""
        
        # Get most recent exchanges
        recent = history[-max_recent:] if len(history) > max_recent else history
        
        formatted_parts = []
        for i, exchange in enumerate(recent, 1):
            formatted_parts.append(
                f"[Previous Exchange {i}]\n"
                f"Question: {exchange['question']}\n"
                f"Your Response: {exchange['answer'][:500]}{'...' if len(exchange['answer']) > 500 else ''}\n"
            )
        
        return "\n".join(formatted_parts)
    
    def reset_conversation(self, conversation_id: str):
        """
        Clear conversation history for a given ID.
        
        Args:
            conversation_id: Unique conversation identifier
        """
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]
    
    def cleanup_old_conversations(self, max_age_hours: int = 24):
        """
        Remove conversations older than specified hours.
        
        Args:
            max_age_hours: Maximum age in hours before cleanup
        """
        from datetime import timedelta
        cutoff = datetime.now() - timedelta(hours=max_age_hours)
        
        to_remove = []
        for conv_id, exchanges in self.conversations.items():
            if exchanges:
                last_timestamp = datetime.fromisoformat(exchanges[-1]['timestamp'])
                if last_timestamp < cutoff:
                    to_remove.append(conv_id)
        
        for conv_id in to_remove:
            del self.conversations[conv_id]


# Global conversation manager instance
conversation_manager = ConversationManager()
