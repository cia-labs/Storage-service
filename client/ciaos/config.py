# config.py
from dataclasses import dataclass

@dataclass
class Config:
    """Configuration class for Ciaos client.
    
    Args:
        api_url (str): The server URL for API requests
        user_id (str): User identifier for authentication
        user_access_key (str): Access key for authentication
    """
    api_url: str
    user_id: str
    user_access_key: str
