from abc import ABC, abstractmethod
from typing import Any, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.logger = logging.getLogger(f"agent.{name}")

    @abstractmethod
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process the input data and return results"""
        pass

    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate the input data before processing"""
        return True

    def log_activity(self, message: str, level: str = "info"):
        """Log agent activity"""
        log_method = getattr(self.logger, level.lower())
        log_method(f"[{self.name}] {message}")

    def format_response(self, data: Dict[str, Any], status: str = "success", message: str = "") -> Dict[str, Any]:
        """Format the agent's response"""
        return {
            "status": status,
            "message": message,
            "agent": self.name,
            "data": data
        } 