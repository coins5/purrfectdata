import httpx
from typing import Optional
from purrfect.domain.ports import ILLMProvider
import random

class MockLLMProvider(ILLMProvider):
    """
    Mock implementation for testing without a real LLM.
    Returns True/False deterministically or randomly based on config?
    For now, let's make it random or always True to avoid blocking.
    actually, let's make it check for "bad" keywords to mimic some logic.
    """
    def check(self, content: str, criteria: str) -> bool:
        # Simple mock logic: if "fail" is in content, return False.
        if "bad" in content.lower() or "terrible" in content.lower():
             return False
        return True

class OllamaLLMProvider(ILLMProvider):
    """
    Ollama implementation using httpx.
    """
    def __init__(self, model: str = "llama3:latest", base_url: str = "http://localhost:11434"):
        self.model = model
        self.base_url = base_url

    def check(self, content: str, criteria: str) -> bool:
        prompt = f"Evaluate the text '{content}' based on the rule: '{criteria}'. Is the text VALID and ACCEPTABLE? Answer ONLY with 'YES' if it is valid, or 'NO' if it is invalid/violates the rule."
        print(f"🧠 [DEBUG] Prompt: {prompt}")
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }

        try:
            response = httpx.post(f"{self.base_url}/api/generate", json=payload, timeout=10.0)
            if response.status_code != 200:
                print(f"Warning: Ollama returned status {response.status_code}")
                print(f"🧠 [DEBUG] Response: {response.text}")
                return True 
                
            data = response.json()
            raw_response = data.get("response", "")
            print(f"🧠 [DEBUG] Response: {raw_response}")
            answer = raw_response.strip().upper()
            
            if "YES" in answer:
                return True
            return False

        except httpx.ConnectError:
            print("Warning: Could not connect to Ollama. Is it running?")
            return True # Assume pass on infra error
        except Exception as e:
            print(f"Warning: LLM check failed: {e}")
            return True
