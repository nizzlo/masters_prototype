"""
Ollama LLM client for reasoning tasks.
"""

import ollama
from typing import Optional
from loguru import logger

from config import settings


class OllamaClient:
    """Client for interacting with Ollama LLM for reasoning tasks."""
    
    def __init__(self, model: Optional[str] = None):
        """
        Initialize the Ollama client.
        
        Args:
            model: Model name to use. Defaults to settings.reasoning_model.
        """
        self.model = model or settings.reasoning_model
        self.base_url = settings.ollama_base_url
        logger.info(f"OllamaClient initialized with model: {self.model}")
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Generate a response from the LLM.
        
        Args:
            prompt: The user prompt.
            system_prompt: Optional system prompt for context.
            
        Returns:
            Generated text response.
        """
        logger.debug(f"Generating response for prompt: {prompt[:100]}...")
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        try:
            response = ollama.chat(
                model=self.model,
                messages=messages,
            )
            result = response['message']['content']
            logger.debug(f"Generated response: {result[:100]}...")
            return result
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise
    
    def generate_with_context(
        self, 
        query: str, 
        context: str, 
        system_prompt: Optional[str] = None
    ) -> str:
        """
        Generate a response using RAG-style context.
        
        Args:
            query: The user query.
            context: Retrieved context to use.
            system_prompt: Optional system prompt.
            
        Returns:
            Generated response.
        """
        default_system = """Answer the question using ONLY the provided context.
If the answer is not in the context, say "Insufficient information in the knowledge base."
Always cite which source documents you used."""
        
        prompt = f"""Context:
{context}

Question:
{query}"""
        
        return self.generate(prompt, system_prompt or default_system)
    
    def check_connection(self) -> bool:
        """Check if Ollama server is accessible."""
        try:
            ollama.list()
            return True
        except Exception as e:
            logger.error(f"Ollama connection failed: {e}")
            return False
    
    def list_models(self) -> list[str]:
        """List available models."""
        try:
            response = ollama.list()
            return [model['name'] for model in response['models']]
        except Exception as e:
            logger.error(f"Error listing models: {e}")
            return []
