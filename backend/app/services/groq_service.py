"""Groq API service wrapper."""
import os
from groq import Groq
from typing import Optional, Dict, Any


class GroqService:
    """Service for interacting with Groq API."""

    def __init__(self):
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set")
        # Initialize Groq client
        # The 'proxies' error typically occurs due to httpx version conflicts
        # Ensure httpx>=0.24.0 is installed
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.2,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Generate response from Groq API.

        Args:
            system_prompt: System message for the AI
            user_prompt: User message/prompt
            temperature: Temperature for generation (default: 0.2)
            max_tokens: Maximum tokens to generate

        Returns:
            Generated text response
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        params = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature
        }

        if max_tokens:
            params["max_tokens"] = max_tokens

        try:
            response = self.client.chat.completions.create(**params)
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Groq API error: {str(e)}")

    def generate_structured(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.2
    ) -> Dict[str, Any]:
        """
        Generate structured response (JSON format).

        Args:
            system_prompt: System message
            user_prompt: User prompt with JSON format instructions
            temperature: Temperature for generation

        Returns:
            Parsed JSON response as dict
        """
        from ..utils.json_extractor import extract_json_from_text
        
        prompt = f"{user_prompt}\n\nPlease respond in valid JSON format only."
        response = self.generate(system_prompt, prompt, temperature)
        
        # Use robust JSON extractor
        extracted = extract_json_from_text(response, fallback_to_text=True)
        
        # If extraction returned a dict, use it; otherwise wrap in content
        if isinstance(extracted, dict):
            return extracted
        else:
            return {"content": extracted if isinstance(extracted, str) else str(extracted)}
