import pytest
from unittest.mock import patch
from GPTNewsGenerator import GPTNewsGenerator
from News import News

# Mock response for OpenAI API
@pytest.fixture
def mock_openai_response():
    class MockResponse:
        def __init__(self):
            self.choices = [type('obj', (object,), {'text' : "Generated News Content"})]

    def mock_completion_create(*args, **kwargs):
        return MockResponse()

    return mock_completion_create

# Test for GPTNewsGenerator
def test_generate_merged_news(mock_openai_response):
    with patch('openai.resources.Completions.create', new=mock_openai_response):
        # Initialize GPTNewsGenerator with a mock API key
        gpt_generator = GPTNewsGenerator(api_key="mock_api_key")

        # Create a list of News objects
        news_list = [
            News(title="Test Title 1", body="Test Body 1", picture=None),
            News(title="Test Title 2", body="Test Body 2", picture=None)
        ]

        # Test generate_merged_news
        merged_news = gpt_generator.generate_merged_news(news_list)

        # Check if the merged news content is not empty
        assert merged_news != "", "Merged news content should not be empty"
        assert merged_news == "Generated News Content", "Merged news content should match the mock response"
