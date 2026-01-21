import unittest
from unittest.mock import MagicMock, patch
from purrfect.infrastructure.llm_client import OllamaLLMProvider

class TestOllamaParsing(unittest.TestCase):
    def test_parsing_yes_exact(self):
        provider = OllamaLLMProvider()
        with patch('httpx.post') as mock_post:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"response": "YES"}
            mock_post.return_value = mock_response
            
            self.assertTrue(provider.check("content", "criteria"))

    def test_parsing_yes_sentence(self):
        provider = OllamaLLMProvider()
        with patch('httpx.post') as mock_post:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"response": "Answer: YES, it is toxic."}
            mock_post.return_value = mock_response
            
            self.assertTrue(provider.check("content", "criteria"))

    def test_parsing_no(self):
        provider = OllamaLLMProvider()
        with patch('httpx.post') as mock_post:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"response": "NO"}
            mock_post.return_value = mock_response
            
            self.assertFalse(provider.check("content", "criteria"))

if __name__ == '__main__':
    unittest.main()
