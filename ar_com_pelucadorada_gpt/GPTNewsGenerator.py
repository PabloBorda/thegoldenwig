from openai import OpenAI

client = OpenAI(api_key=self.api_key)
from News import News

class GPTNewsGenerator:
    def __init__(self, api_key):
        self.api_key = api_key

    def generate_merged_news(self, news_list):
        # Combine the content of each news item into a single prompt
        prompt = "Merge the following news articles into a single, well-written article:\n\n"
        for news in news_list:
            prompt += f"Title: {news.title}\n{news.body}\n\n"

        # Making the request to OpenAI GPT-3
        try:
            response = client.completions.create(engine="davinci",
            prompt=prompt,
            max_tokens=1024,  # Adjust as needed
            n=1,
            stop=None,
            temperature=0.7  # Adjust for creativity level)
            generated_news_content = response.choices[0].text.strip()
            return generated_news_content
        except Exception as e:
            print(f"Error in generating merged news: {e}")
            return None
